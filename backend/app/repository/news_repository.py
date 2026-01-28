"""News repository for Supabase operations."""
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from supabase import Client

from ..config import get_supabase_client
from ..schema.news_schema import ArticleCreate, CategoryEnum


def get_utc_now() -> str:
    """Get current UTC time as ISO string with timezone."""
    return datetime.now(timezone.utc).isoformat()


class NewsRepository:
    """Repository for news article CRUD operations."""

    TABLE_NAME = "news_articles"
    LOG_TABLE_NAME = "crawl_logs"

    def __init__(self, client: Optional[Client] = None):
        """Initialize repository with Supabase client."""
        self._client = client

    @property
    def client(self) -> Client:
        """Get Supabase client (lazy initialization)."""
        if self._client is None:
            self._client = get_supabase_client()
        return self._client

    async def get_articles(
        self,
        category: Optional[str] = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[List[Dict[str, Any]], int]:
        """Get articles with optional filtering and pagination."""
        query = self.client.table(self.TABLE_NAME).select("*", count="exact")

        if category:
            query = query.eq("category", category)

        # Order by crawled_at descending
        query = query.order("crawled_at", desc=True)

        # Pagination
        start = (page - 1) * size
        end = start + size - 1
        query = query.range(start, end)

        response = query.execute()
        total = response.count or 0
        return response.data, total

    async def get_article_by_id(self, article_id: str) -> Optional[Dict[str, Any]]:
        """Get a single article by ID."""
        response = (
            self.client.table(self.TABLE_NAME)
            .select("*")
            .eq("id", article_id)
            .single()
            .execute()
        )
        return response.data

    async def get_article_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Get a single article by URL."""
        response = (
            self.client.table(self.TABLE_NAME)
            .select("*")
            .eq("url", url)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    async def create_article(self, article: ArticleCreate) -> Dict[str, Any]:
        """Create a new article."""
        data = article.model_dump()
        data["category"] = data["category"].value if isinstance(data["category"], CategoryEnum) else data["category"]
        data["crawled_at"] = get_utc_now()

        # Convert datetime to ISO string
        if data.get("published_at"):
            data["published_at"] = data["published_at"].isoformat()

        response = self.client.table(self.TABLE_NAME).insert(data).execute()
        return response.data[0] if response.data else {}

    async def upsert_article(self, article: ArticleCreate) -> Dict[str, Any]:
        """Upsert article (insert or update based on URL)."""
        data = article.model_dump()
        data["category"] = data["category"].value if isinstance(data["category"], CategoryEnum) else data["category"]
        data["crawled_at"] = get_utc_now()

        # Convert datetime to ISO string
        if data.get("published_at"):
            data["published_at"] = data["published_at"].isoformat()

        response = (
            self.client.table(self.TABLE_NAME)
            .upsert(data, on_conflict="url")
            .execute()
        )
        return response.data[0] if response.data else {}

    async def bulk_upsert_articles(
        self, articles: List[ArticleCreate]
    ) -> List[Dict[str, Any]]:
        """Bulk upsert multiple articles."""
        if not articles:
            return []

        data_list = []
        for article in articles:
            data = article.model_dump()
            data["category"] = data["category"].value if isinstance(data["category"], CategoryEnum) else data["category"]
            data["crawled_at"] = get_utc_now()
            if data.get("published_at"):
                data["published_at"] = data["published_at"].isoformat()
            data_list.append(data)

        response = (
            self.client.table(self.TABLE_NAME)
            .upsert(data_list, on_conflict="url")
            .execute()
        )
        return response.data

    async def get_category_counts(self) -> List[Dict[str, Any]]:
        """Get article count per category."""
        results = []
        for category in CategoryEnum:
            response = (
                self.client.table(self.TABLE_NAME)
                .select("id", count="exact")
                .eq("category", category.value)
                .execute()
            )
            results.append({
                "id": category.value,
                "name": category.korean_name,
                "count": response.count or 0,
            })
        return results

    async def get_total_count(self) -> int:
        """Get total article count."""
        response = (
            self.client.table(self.TABLE_NAME)
            .select("id", count="exact")
            .execute()
        )
        return response.count or 0

    # Crawl log methods
    async def create_crawl_log(self) -> Dict[str, Any]:
        """Create a new crawl log entry."""
        data = {
            "started_at": get_utc_now(),
            "status": "running",
        }
        response = self.client.table(self.LOG_TABLE_NAME).insert(data).execute()
        return response.data[0] if response.data else {}

    async def update_crawl_log(
        self,
        log_id: str,
        total_articles: int,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update crawl log with results."""
        data = {
            "finished_at": get_utc_now(),
            "total_articles": total_articles,
            "status": status,
        }
        if error_message:
            data["error_message"] = error_message

        response = (
            self.client.table(self.LOG_TABLE_NAME)
            .update(data)
            .eq("id", log_id)
            .execute()
        )
        return response.data[0] if response.data else {}

    async def get_last_crawl_log(self) -> Optional[Dict[str, Any]]:
        """Get the most recent crawl log."""
        response = (
            self.client.table(self.LOG_TABLE_NAME)
            .select("*")
            .order("created_at", desc=True)  # created_at은 Supabase가 자동 생성하므로 항상 정확
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None
