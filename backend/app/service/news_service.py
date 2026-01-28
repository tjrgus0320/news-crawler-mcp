"""News service for crawling and business logic."""
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

# Add parent project to path to import existing crawlers
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.crawlers.naver import NaverNewsCrawler
from src.models.article import Category as SrcCategory, Article as SrcArticle
from src.utils.http import HttpClient

from ..repository.news_repository import NewsRepository
from ..schema.news_schema import ArticleCreate, CategoryEnum, ArticleResponse

logger = logging.getLogger(__name__)


class NewsService:
    """Service for news crawling and management."""

    def __init__(self, repository: Optional[NewsRepository] = None):
        """Initialize service with repository."""
        self.repository = repository or NewsRepository()

    def _map_category(self, category: CategoryEnum) -> SrcCategory:
        """Map API category enum to source category enum."""
        mapping = {
            CategoryEnum.POLITICS: SrcCategory.POLITICS,
            CategoryEnum.ECONOMY: SrcCategory.ECONOMY,
            CategoryEnum.SOCIETY: SrcCategory.SOCIETY,
            CategoryEnum.LIFE: SrcCategory.LIFE,
            CategoryEnum.WORLD: SrcCategory.WORLD,
            CategoryEnum.IT: SrcCategory.IT,
        }
        return mapping[category]

    def _article_to_create(self, article: SrcArticle) -> ArticleCreate:
        """Convert source article to create schema."""
        # article.category가 이미 문자열일 수 있음 (use_enum_values=True)
        category_value = article.category if isinstance(article.category, str) else article.category.value
        return ArticleCreate(
            title=article.title,
            url=article.url,
            summary=article.summary,
            content=article.content,
            category=CategoryEnum(category_value),
            source=article.source,
            author=article.author,
            image_url=article.image_url,
            published_at=article.published_at,
        )

    async def crawl_category(
        self,
        category: CategoryEnum,
        max_articles: int = 30,
        include_content: bool = False,
    ) -> List[Dict[str, Any]]:
        """Crawl news for a specific category and save to database."""
        src_category = self._map_category(category)

        async with HttpClient() as http:
            crawler = NaverNewsCrawler(http)
            articles = await crawler.crawl_category(
                src_category,
                max_articles,
                include_content,
            )

        # Convert and save to database
        created_articles = []
        for article in articles:
            article_create = self._article_to_create(article)
            result = await self.repository.upsert_article(article_create)
            created_articles.append(result)

        logger.info(
            f"Crawled {len(created_articles)} articles for category {category.value}"
        )
        return created_articles

    async def crawl_all_categories(
        self,
        categories: Optional[List[CategoryEnum]] = None,
        max_per_category: int = 30,
        include_content: bool = False,
    ) -> Dict[str, int]:
        """Crawl all categories and return count per category."""
        if categories is None:
            categories = list(CategoryEnum)

        # Create crawl log
        log = await self.repository.create_crawl_log()
        log_id = log.get("id")

        total_count = 0
        results = {}

        try:
            src_categories = [self._map_category(c) for c in categories]

            async with HttpClient() as http:
                crawler = NaverNewsCrawler(http)
                articles_by_category = await crawler.crawl_all_categories(
                    src_categories,
                    max_per_category,
                    include_content,
                )

            # Save all articles to database
            for cat_str, articles in articles_by_category.items():
                article_creates = [self._article_to_create(a) for a in articles]
                await self.repository.bulk_upsert_articles(article_creates)
                results[cat_str] = len(articles)
                total_count += len(articles)

            # Update crawl log
            if log_id:
                await self.repository.update_crawl_log(
                    log_id, total_count, status="success"
                )

            logger.info(f"Crawled total {total_count} articles")

        except Exception as e:
            logger.error(f"Crawl failed: {e}")
            if log_id:
                await self.repository.update_crawl_log(
                    log_id, total_count, status="failed", error_message=str(e)
                )
            raise

        return results

    async def get_articles(
        self,
        category: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[List[Dict[str, Any]], int]:
        """Get articles with optional filtering."""
        return await self.repository.get_articles(category, page, size)

    async def get_article_by_id(self, article_id: str) -> Optional[Dict[str, Any]]:
        """Get a single article by ID."""
        return await self.repository.get_article_by_id(article_id)

    async def get_categories_with_count(self) -> List[Dict[str, Any]]:
        """Get all categories with article counts."""
        return await self.repository.get_category_counts()

    async def get_crawl_status(self) -> Dict[str, Any]:
        """Get last crawl status."""
        last_log = await self.repository.get_last_crawl_log()
        total = await self.repository.get_total_count()

        return {
            "last_crawled_at": last_log.get("finished_at") if last_log else None,
            "total_articles": total,
            "status": last_log.get("status", "unknown") if last_log else "unknown",
        }
