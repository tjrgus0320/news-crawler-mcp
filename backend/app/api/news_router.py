"""News API router."""
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks

from ..schema.news_schema import (
    ArticleResponse,
    ArticleListResponse,
    CategoryResponse,
    CrawlStatusResponse,
    BlogTemplateResponse,
    CategoryEnum,
)
from ..service.news_service import NewsService
from ..service.template_service import TemplateService

router = APIRouter(prefix="/api", tags=["news"])

# Service instances
news_service = NewsService()
template_service = TemplateService()


@router.get("/news", response_model=ArticleListResponse)
async def get_news(
    category: Optional[str] = Query(None, description="카테고리 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
):
    """Get news articles with optional category filter and pagination."""
    # Validate category if provided
    if category:
        try:
            CategoryEnum(category)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category: {category}. Valid options: {[c.value for c in CategoryEnum]}",
            )

    articles, total = await news_service.get_articles(category, page, size)

    return ArticleListResponse(
        items=[ArticleResponse(**article) for article in articles],
        total=total,
        page=page,
        size=size,
        has_next=(page * size) < total,
    )


@router.get("/news/{article_id}", response_model=ArticleResponse)
async def get_news_detail(article_id: str):
    """Get a single news article by ID."""
    article = await news_service.get_article_by_id(article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return ArticleResponse(**article)


@router.get("/news/{article_id}/template", response_model=BlogTemplateResponse)
async def get_blog_template(article_id: str):
    """Get blog post template for an article."""
    article = await news_service.get_article_by_id(article_id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    template = template_service.generate_template(article)

    return BlogTemplateResponse(article_id=article_id, template=template)


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories():
    """Get all categories with article counts."""
    categories = await news_service.get_categories_with_count()
    return [CategoryResponse(**cat) for cat in categories]


@router.get("/status", response_model=CrawlStatusResponse)
async def get_crawl_status():
    """Get the last crawl status and statistics."""
    status = await news_service.get_crawl_status()
    return CrawlStatusResponse(**status)


@router.post("/news/crawl")
async def trigger_crawl(
    background_tasks: BackgroundTasks,
    categories: Optional[List[str]] = Query(None, description="크롤링할 카테고리"),
    max_per_category: int = Query(30, ge=1, le=50, description="카테고리당 최대 기사 수"),
):
    """Manually trigger a news crawl. Runs in background."""
    # Validate categories
    category_enums = None
    if categories:
        try:
            category_enums = [CategoryEnum(c) for c in categories]
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category. Valid options: {[c.value for c in CategoryEnum]}",
            )

    # Run crawl in background
    async def run_crawl():
        await news_service.crawl_all_categories(
            categories=category_enums,
            max_per_category=max_per_category,
        )

    background_tasks.add_task(run_crawl)

    return {
        "message": "Crawl started in background",
        "categories": categories or [c.value for c in CategoryEnum],
        "max_per_category": max_per_category,
    }
