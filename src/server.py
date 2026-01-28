"""MCP Server for news article crawling."""
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .crawlers.naver import NaverNewsCrawler
from .formatters.blog import BlogFormatter
from .models.article import Article, Category, DailyDigest
from .utils.http import HttpClient

# Initialize MCP server
server = Server("news-crawler")


def get_category_list() -> list[dict]:
    """Get list of available categories."""
    return [
        {"id": cat.value, "name": cat.korean_name}
        for cat in Category
    ]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="list_categories",
            description="사용 가능한 뉴스 카테고리 목록을 반환합니다.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="crawl_news_by_category",
            description="특정 카테고리의 뉴스 기사를 크롤링합니다. 블로그 포스팅용 마크다운 형식으로 반환합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "뉴스 카테고리 (politics, economy, society, life, world, it)",
                        "enum": ["politics", "economy", "society", "life", "world", "it"],
                    },
                    "max_articles": {
                        "type": "integer",
                        "description": "크롤링할 최대 기사 수 (기본값: 5)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20,
                    },
                    "include_content": {
                        "type": "boolean",
                        "description": "기사 본문 포함 여부 (기본값: false, true시 속도 느려짐)",
                        "default": False,
                    },
                },
                "required": ["category"],
            },
        ),
        Tool(
            name="crawl_daily_news",
            description="오늘의 주요 뉴스를 모든 카테고리에서 크롤링하여 블로그 포스팅용 마크다운으로 반환합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "categories": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["politics", "economy", "society", "life", "world", "it"],
                        },
                        "description": "크롤링할 카테고리 목록 (지정하지 않으면 전체)",
                    },
                    "max_per_category": {
                        "type": "integer",
                        "description": "카테고리당 최대 기사 수 (기본값: 3)",
                        "default": 3,
                        "minimum": 1,
                        "maximum": 10,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="get_article_detail",
            description="특정 기사 URL의 상세 내용을 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "기사 URL",
                    },
                    "category": {
                        "type": "string",
                        "description": "기사 카테고리",
                        "enum": ["politics", "economy", "society", "life", "world", "it"],
                    },
                },
                "required": ["url"],
            },
        ),
        Tool(
            name="save_to_file",
            description="마크다운 내용을 파일로 저장합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "저장할 마크다운 내용",
                    },
                    "filename": {
                        "type": "string",
                        "description": "파일명 (지정하지 않으면 날짜 기반 자동 생성)",
                    },
                },
                "required": ["content"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""

    if name == "list_categories":
        categories = get_category_list()
        result = "## 사용 가능한 뉴스 카테고리\n\n"
        for cat in categories:
            result += f"- `{cat['id']}`: {cat['name']}\n"
        return [TextContent(type="text", text=result)]

    elif name == "crawl_news_by_category":
        category_str = arguments.get("category", "it")
        max_articles = arguments.get("max_articles", 5)
        include_content = arguments.get("include_content", False)

        try:
            category = Category(category_str)
        except ValueError:
            return [TextContent(
                type="text",
                text=f"오류: 알 수 없는 카테고리 '{category_str}'. 사용 가능: {[c.value for c in Category]}"
            )]

        async with HttpClient() as http:
            crawler = NaverNewsCrawler(http)
            articles = await crawler.crawl_category(
                category,
                max_articles,
                include_content,
            )

        if not articles:
            return [TextContent(
                type="text",
                text=f"'{category.korean_name}' 카테고리에서 기사를 찾을 수 없습니다."
            )]

        formatter = BlogFormatter()
        result = formatter.format_category_articles(category, articles)

        return [TextContent(type="text", text=result)]

    elif name == "crawl_daily_news":
        categories_str = arguments.get("categories")
        max_per_category = arguments.get("max_per_category", 3)

        if categories_str:
            try:
                categories = [Category(c) for c in categories_str]
            except ValueError as e:
                return [TextContent(
                    type="text",
                    text=f"오류: 알 수 없는 카테고리. 사용 가능: {[c.value for c in Category]}"
                )]
        else:
            categories = list(Category)

        async with HttpClient() as http:
            crawler = NaverNewsCrawler(http)
            articles_by_category = await crawler.crawl_all_categories(
                categories,
                max_per_category,
                include_content=False,
            )

        digest = DailyDigest()
        for cat_str, articles in articles_by_category.items():
            for article in articles:
                digest.add_article(article)

        if digest.total_count == 0:
            return [TextContent(
                type="text",
                text="기사를 찾을 수 없습니다. 잠시 후 다시 시도해주세요."
            )]

        formatter = BlogFormatter()
        result = formatter.format_daily_digest(digest)

        return [TextContent(type="text", text=result)]

    elif name == "get_article_detail":
        url = arguments.get("url", "")
        category_str = arguments.get("category", "it")

        if not url:
            return [TextContent(type="text", text="오류: URL이 필요합니다.")]

        try:
            category = Category(category_str)
        except ValueError:
            category = Category.IT

        async with HttpClient() as http:
            crawler = NaverNewsCrawler(http)
            article = await crawler.get_article_detail(url, category)

        if not article:
            return [TextContent(
                type="text",
                text=f"기사를 가져올 수 없습니다: {url}"
            )]

        result = f"# {article.title}\n\n"
        result += f"**출처**: {article.source}\n"
        result += f"**기자**: {article.author}\n"
        if article.published_at:
            result += f"**발행**: {article.published_at.strftime('%Y-%m-%d %H:%M')}\n"
        result += f"\n---\n\n{article.content}\n"
        result += f"\n---\n\n> 원문: {article.url}"

        return [TextContent(type="text", text=result)]

    elif name == "save_to_file":
        content = arguments.get("content", "")
        filename = arguments.get("filename")

        if not content:
            return [TextContent(type="text", text="오류: 저장할 내용이 없습니다.")]

        formatter = BlogFormatter(output_dir=Path("./output"))
        filepath = formatter.save_to_file(content, filename)

        return [TextContent(
            type="text",
            text=f"파일이 저장되었습니다: {filepath.absolute()}"
        )]

    else:
        return [TextContent(
            type="text",
            text=f"알 수 없는 도구: {name}"
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
