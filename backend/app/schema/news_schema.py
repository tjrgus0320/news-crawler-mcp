"""Pydantic schemas for news API."""
from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class CategoryEnum(str, Enum):
    """News category enumeration."""

    POLITICS = "politics"
    ECONOMY = "economy"
    SOCIETY = "society"
    LIFE = "life"
    WORLD = "world"
    IT = "it"

    @property
    def korean_name(self) -> str:
        """Get Korean name for category."""
        names = {
            "politics": "정치",
            "economy": "경제",
            "society": "사회",
            "life": "생활/문화",
            "world": "세계",
            "it": "IT/과학",
        }
        return names.get(self.value, self.value)


class ArticleBase(BaseModel):
    """Base article schema."""

    title: str = Field(..., description="기사 제목")
    url: str = Field(..., description="기사 URL")
    summary: Optional[str] = Field(None, description="기사 요약")
    category: CategoryEnum = Field(..., description="카테고리")
    source: Optional[str] = Field(None, description="출처")
    author: Optional[str] = Field(None, description="기자")
    image_url: Optional[str] = Field(None, description="이미지 URL")
    published_at: Optional[datetime] = Field(None, description="발행일")


class ArticleCreate(ArticleBase):
    """Schema for creating an article."""

    content: Optional[str] = Field(None, description="기사 본문")


class ArticleResponse(ArticleBase):
    """Schema for article response."""

    id: str = Field(..., description="기사 ID")
    content: Optional[str] = Field(None, description="기사 본문")
    crawled_at: datetime = Field(..., description="크롤링 시간")
    created_at: datetime = Field(..., description="생성 시간")

    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """Schema for article list response."""

    items: List[ArticleResponse]
    total: int = Field(..., description="전체 기사 수")
    page: int = Field(1, description="현재 페이지")
    size: int = Field(20, description="페이지 크기")
    has_next: bool = Field(False, description="다음 페이지 존재 여부")


class CategoryResponse(BaseModel):
    """Schema for category response."""

    id: str = Field(..., description="카테고리 ID")
    name: str = Field(..., description="카테고리 한글명")
    count: int = Field(0, description="기사 수")


class CrawlStatusResponse(BaseModel):
    """Schema for crawl status response."""

    last_crawled_at: Optional[datetime] = Field(None, description="마지막 크롤링 시간")
    total_articles: int = Field(0, description="전체 기사 수")
    status: str = Field("unknown", description="상태")
    next_crawl_at: Optional[datetime] = Field(None, description="다음 크롤링 예정 시간")


class BlogTemplateResponse(BaseModel):
    """Schema for blog template response."""

    article_id: str = Field(..., description="기사 ID")
    template: str = Field(..., description="블로그 템플릿 마크다운")
