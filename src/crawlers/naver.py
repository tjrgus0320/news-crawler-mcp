"""Naver News crawler implementation."""
import re
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..models.article import Article, Category
from ..utils.http import HttpClient


class NaverNewsCrawler:
    """Crawler for Naver News."""

    BASE_URL = "https://news.naver.com"

    # Section IDs for each category
    CATEGORY_SECTIONS = {
        Category.POLITICS: "100",
        Category.ECONOMY: "101",
        Category.SOCIETY: "102",
        Category.LIFE: "103",
        Category.WORLD: "104",
        Category.IT: "105",
    }

    def __init__(self, http_client: HttpClient):
        self.http = http_client

    def _get_section_url(self, category: Category) -> str:
        """Get section URL for a category."""
        section_id = self.CATEGORY_SECTIONS.get(category, "100")
        return f"{self.BASE_URL}/section/{section_id}"

    def _parse_article_list(self, html: str, category: Category) -> list[dict]:
        """
        Parse article list from section page.

        Returns list of dicts with 'title' and 'url' keys.
        """
        soup = BeautifulSoup(html, "lxml")
        articles = []

        # Naver News section page structure
        # Look for headline news area
        headline_area = soup.select(".sa_list, .section_headline, .cluster_group")

        for area in headline_area:
            # Find article links
            links = area.select("a.sa_text_title, a.cluster_text_headline, a[class*='title']")

            for link in links:
                href = link.get("href", "")
                title = link.get_text(strip=True)

                if not href or not title:
                    continue

                # Ensure full URL
                if href.startswith("/"):
                    href = urljoin(self.BASE_URL, href)

                # Only include Naver news articles
                if "news.naver.com" in href:
                    articles.append({
                        "title": title,
                        "url": href,
                        "category": category,
                    })

        # Also try the main list items
        list_items = soup.select(".sa_item, .cluster_item, li[class*='news']")
        for item in list_items:
            link = item.select_one("a[class*='title'], a[class*='headline']")
            if not link:
                continue

            href = link.get("href", "")
            title = link.get_text(strip=True)

            if not href or not title:
                continue

            if href.startswith("/"):
                href = urljoin(self.BASE_URL, href)

            if "news.naver.com" in href and href not in [a["url"] for a in articles]:
                articles.append({
                    "title": title,
                    "url": href,
                    "category": category,
                })

        return articles[:20]  # Limit to top 20

    def _parse_article_detail(self, html: str, url: str, category: Category) -> Optional[Article]:
        """Parse article detail page."""
        soup = BeautifulSoup(html, "lxml")

        # Title
        title_elem = soup.select_one(
            "#title_area, .media_end_head_headline, h2.end_tit, #articleTitle"
        )
        title = title_elem.get_text(strip=True) if title_elem else ""

        if not title:
            return None

        # Content - article body
        content_elem = soup.select_one(
            "#dic_area, .newsct_article, #articleBodyContents, .article_body"
        )

        content = ""
        if content_elem:
            # Remove scripts and styles
            for tag in content_elem.select("script, style, .reporter_area"):
                tag.decompose()
            content = content_elem.get_text(strip=True)

        # Summary - first paragraph or first 200 chars
        summary = content[:300] + "..." if len(content) > 300 else content

        # Source (media name)
        source_elem = soup.select_one(
            ".media_end_head_top_logo img, .press_logo img, .media_name"
        )
        source = ""
        if source_elem:
            source = source_elem.get("alt", "") or source_elem.get("title", "") or source_elem.get_text(strip=True)

        # Author
        author_elem = soup.select_one(
            ".media_end_head_journalist_name, .byline, .reporter"
        )
        author = author_elem.get_text(strip=True) if author_elem else ""

        # Published time
        time_elem = soup.select_one(
            ".media_end_head_info_datestamp_time, .article_info .date, time"
        )
        published_at = None
        if time_elem:
            time_str = time_elem.get("data-date-time") or time_elem.get("datetime") or time_elem.get_text(strip=True)
            published_at = self._parse_datetime(time_str)

        # Image URL
        image_elem = soup.select_one(
            "#img1, .end_photo_org img, .article_img img"
        )
        image_url = image_elem.get("src") if image_elem else None

        return Article(
            title=title,
            url=url,
            summary=summary,
            content=content,
            category=category,
            source=source,
            author=author,
            published_at=published_at,
            image_url=image_url,
        )

    def _parse_datetime(self, time_str: str) -> Optional[datetime]:
        """Parse datetime from various formats."""
        if not time_str:
            return None

        # Try various formats
        patterns = [
            r"(\d{4})[.-](\d{2})[.-](\d{2})\s*(\d{2}):(\d{2})",  # 2025-01-27 14:30
            r"(\d{4})[.-](\d{2})[.-](\d{2})",  # 2025-01-27
        ]

        for pattern in patterns:
            match = re.search(pattern, time_str)
            if match:
                groups = match.groups()
                try:
                    if len(groups) >= 5:
                        return datetime(
                            int(groups[0]), int(groups[1]), int(groups[2]),
                            int(groups[3]), int(groups[4])
                        )
                    elif len(groups) >= 3:
                        return datetime(
                            int(groups[0]), int(groups[1]), int(groups[2])
                        )
                except ValueError:
                    continue

        return None

    def _is_today(self, dt: Optional[datetime]) -> bool:
        """Check if datetime is today."""
        if not dt:
            return True  # Assume today if unknown

        today = datetime.now().date()
        return dt.date() == today

    async def get_article_list(
        self,
        category: Category,
        max_count: int = 10,
        today_only: bool = True,
    ) -> list[dict]:
        """
        Get list of articles for a category.

        Args:
            category: News category
            max_count: Maximum number of articles
            today_only: Only include today's articles

        Returns:
            List of article dicts with title and url
        """
        url = self._get_section_url(category)
        html = await self.http.get(url)

        if not html:
            return []

        articles = self._parse_article_list(html, category)
        return articles[:max_count]

    async def get_article_detail(self, url: str, category: Category) -> Optional[Article]:
        """
        Get full article details.

        Args:
            url: Article URL
            category: News category

        Returns:
            Article object or None if failed
        """
        html = await self.http.get_with_delay(url)

        if not html:
            return None

        return self._parse_article_detail(html, url, category)

    async def crawl_category(
        self,
        category: Category,
        max_articles: int = 10,
        include_content: bool = False,
    ) -> list[Article]:
        """
        Crawl all articles for a category.

        Args:
            category: News category to crawl
            max_articles: Maximum number of articles
            include_content: Whether to fetch full content

        Returns:
            List of Article objects
        """
        article_list = await self.get_article_list(category, max_articles)
        articles = []

        for item in article_list:
            if include_content:
                article = await self.get_article_detail(item["url"], category)
                if article:
                    articles.append(article)
            else:
                # Create basic article without full content
                articles.append(Article(
                    title=item["title"],
                    url=item["url"],
                    category=category,
                    summary="",
                ))

        return articles

    async def crawl_all_categories(
        self,
        categories: Optional[list[Category]] = None,
        max_per_category: int = 5,
        include_content: bool = False,
    ) -> dict[str, list[Article]]:
        """
        Crawl articles from multiple categories.

        Args:
            categories: List of categories (all if None)
            max_per_category: Max articles per category
            include_content: Whether to fetch full content

        Returns:
            Dict mapping category name to article list
        """
        if categories is None:
            categories = list(Category)

        result = {}

        for category in categories:
            articles = await self.crawl_category(
                category,
                max_per_category,
                include_content,
            )
            result[category.value] = articles

        return result
