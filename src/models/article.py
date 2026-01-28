"""Data models for news articles."""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class Category(str, Enum):
    """News categories."""
    POLITICS = "politics"
    ECONOMY = "economy"
    SOCIETY = "society"
    LIFE = "life"
    WORLD = "world"
    IT = "it"

    @property
    def korean_name(self) -> str:
        """Get Korean name for the category."""
        names = {
            "politics": "정치",
            "economy": "경제",
            "society": "사회",
            "life": "생활/문화",
            "world": "세계",
            "it": "IT/과학",
        }
        return names.get(self.value, self.value)


class Article(BaseModel):
    """Single news article model."""
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Article URL")
    summary: str = Field(default="", description="Article summary or first paragraph")
    content: str = Field(default="", description="Full article content")
    category: Category = Field(..., description="Article category")
    source: str = Field(default="", description="News source/publisher")
    author: str = Field(default="", description="Author name")
    published_at: Optional[datetime] = Field(default=None, description="Publication time")
    image_url: Optional[str] = Field(default=None, description="Main image URL")
    crawled_at: datetime = Field(default_factory=datetime.now, description="Crawl timestamp")

    class Config:
        use_enum_values = True


class DailyDigest(BaseModel):
    """Collection of articles for a day."""
    date: datetime = Field(default_factory=datetime.now, description="Digest date")
    categories: dict[str, list[Article]] = Field(
        default_factory=dict,
        description="Articles grouped by category"
    )
    total_count: int = Field(default=0, description="Total article count")

    def add_article(self, article: Article) -> None:
        """Add an article to the digest."""
        category = article.category
        if isinstance(category, Category):
            category = category.value

        if category not in self.categories:
            self.categories[category] = []

        self.categories[category].append(article)
        self.total_count = sum(len(articles) for articles in self.categories.values())

    def get_articles_by_category(self, category: str | Category) -> list[Article]:
        """Get articles for a specific category."""
        if isinstance(category, Category):
            category = category.value
        return self.categories.get(category, [])
