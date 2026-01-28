"""Blog post formatter for news articles."""
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models.article import Article, Category, DailyDigest


class BlogFormatter:
    """Format articles into blog-ready markdown."""

    def __init__(
        self,
        title_template: str = "[{date}] 오늘의 {category} 뉴스 모음",
        output_dir: Optional[Path] = None,
    ):
        self.title_template = title_template
        self.output_dir = output_dir or Path("./output")

    def format_single_article(self, article: Article, index: int = 1) -> str:
        """Format a single article as markdown."""
        lines = []

        # Title with link
        lines.append(f"### {index}. {article.title}")
        lines.append("")

        # Summary if available
        if article.summary:
            summary = article.summary.strip()
            if len(summary) > 300:
                summary = summary[:300] + "..."
            lines.append(summary)
            lines.append("")

        # Source link
        source_name = article.source or "원문"
        lines.append(f"> 출처: [{source_name}]({article.url})")
        lines.append("")

        return "\n".join(lines)

    def format_category_section(
        self,
        category: Category | str,
        articles: list[Article],
    ) -> str:
        """Format all articles in a category as a section."""
        if not articles:
            return ""

        lines = []

        # Category header
        if isinstance(category, Category):
            category_name = category.korean_name
        else:
            # Try to get Korean name from string
            try:
                category_name = Category(category).korean_name
            except ValueError:
                category_name = category

        lines.append(f"## {category_name}")
        lines.append("")

        # Articles
        for idx, article in enumerate(articles, 1):
            lines.append(self.format_single_article(article, idx))

        return "\n".join(lines)

    def format_daily_digest(
        self,
        digest: DailyDigest,
        categories_order: Optional[list[str]] = None,
    ) -> str:
        """Format a full daily digest as markdown."""
        lines = []

        # Title
        date_str = digest.date.strftime("%Y.%m.%d")
        lines.append(f"# [{date_str}] 오늘의 뉴스 모음")
        lines.append("")

        # Intro
        lines.append("오늘의 주요 뉴스를 카테고리별로 정리했습니다.")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Categories
        if categories_order is None:
            categories_order = list(digest.categories.keys())

        for category in categories_order:
            articles = digest.get_articles_by_category(category)
            if articles:
                section = self.format_category_section(category, articles)
                lines.append(section)
                lines.append("---")
                lines.append("")

        # Outro
        lines.append("")
        lines.append(f"*총 {digest.total_count}개의 기사가 수집되었습니다.*")
        lines.append("")
        lines.append("*이 포스트는 자동으로 생성되었습니다.*")

        return "\n".join(lines)

    def format_category_articles(
        self,
        category: Category | str,
        articles: list[Article],
        date: Optional[datetime] = None,
    ) -> str:
        """Format articles for a single category blog post."""
        lines = []

        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y.%m.%d")

        # Get category name
        if isinstance(category, Category):
            category_name = category.korean_name
        else:
            try:
                category_name = Category(category).korean_name
            except ValueError:
                category_name = category

        # Title
        lines.append(f"# [{date_str}] 오늘의 {category_name} 뉴스 모음")
        lines.append("")

        # Intro
        lines.append(f"오늘의 주요 {category_name} 뉴스를 정리했습니다.")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Articles
        for idx, article in enumerate(articles, 1):
            lines.append(self.format_single_article(article, idx))

        # Outro
        lines.append("---")
        lines.append("")
        lines.append(f"*총 {len(articles)}개의 기사가 수집되었습니다.*")
        lines.append("")
        lines.append("*이 포스트는 자동으로 생성되었습니다.*")

        return "\n".join(lines)

    def save_to_file(
        self,
        content: str,
        filename: Optional[str] = None,
    ) -> Path:
        """Save formatted content to a file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if filename is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"{date_str}-daily-news.md"

        filepath = self.output_dir / filename
        filepath.write_text(content, encoding="utf-8")

        return filepath

    def format_simple_list(self, articles: list[Article]) -> str:
        """Format articles as a simple numbered list."""
        lines = []

        for idx, article in enumerate(articles, 1):
            source = f" ({article.source})" if article.source else ""
            lines.append(f"{idx}. [{article.title}]({article.url}){source}")

        return "\n".join(lines)
