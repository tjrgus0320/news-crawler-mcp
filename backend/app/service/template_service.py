"""Template service for blog post generation."""
from datetime import datetime
from typing import Dict, Any, Optional, List


class TemplateService:
    """Service for generating blog post templates."""

    # Category metadata
    CATEGORY_META = {
        "politics": {
            "name": "정치",
            "emoji": "🏛️",
            "intro": "오늘 정치권에서는 다음과 같은 주요 이슈들이 있었습니다.",
        },
        "economy": {
            "name": "경제",
            "emoji": "💰",
            "intro": "경제 분야에서 주목할 만한 소식들을 정리했습니다.",
        },
        "society": {
            "name": "사회",
            "emoji": "👥",
            "intro": "오늘 사회면을 장식한 주요 뉴스들입니다.",
        },
        "life": {
            "name": "생활/문화",
            "emoji": "🌸",
            "intro": "생활과 문화 관련 흥미로운 소식들을 모았습니다.",
        },
        "world": {
            "name": "세계",
            "emoji": "🌍",
            "intro": "국제 뉴스에서 눈여겨볼 소식들입니다.",
        },
        "it": {
            "name": "IT/과학",
            "emoji": "💻",
            "intro": "기술과 과학 분야의 최신 동향을 살펴봅니다.",
        },
    }

    def generate_template(self, article: Dict[str, Any]) -> str:
        """Generate a blog post template from an article."""
        title = article.get("title", "제목 없음")
        category = article.get("category", "기타")
        source = article.get("source", "알 수 없음")
        url = article.get("url", "#")
        summary = article.get("summary", "")
        published_at = article.get("published_at")

        # Format date
        if published_at:
            if isinstance(published_at, str):
                try:
                    published_at = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                except ValueError:
                    published_at = None

        date_str = (
            published_at.strftime("%Y-%m-%d")
            if published_at
            else datetime.now().strftime("%Y-%m-%d")
        )

        # Get Korean category name
        meta = self.CATEGORY_META.get(category, {"name": category, "emoji": "📰"})
        category_kr = meta["name"]

        # Generate summary points
        summary_points = self._extract_summary_points(summary)

        template = f"""## [{category_kr}] {title}

📅 작성일: {date_str}
📰 출처: {source}

### 핵심 요약
{summary_points}

### 원문 링크
[기사 원문 보기]({url})

---
"""
        return template

    def _extract_summary_points(self, summary: str) -> str:
        """Extract key points from summary text."""
        if not summary:
            return "- 요약 정보 없음"

        # Split by sentences and create bullet points
        sentences = summary.replace(".", ".\n").split("\n")
        points = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Filter out very short fragments
                points.append(f"- {sentence}")
                if len(points) >= 3:  # Max 3 points
                    break

        if not points:
            return f"- {summary[:200]}"

        return "\n".join(points)

    def generate_daily_digest_template(
        self, articles: list[Dict[str, Any]], date: Optional[datetime] = None
    ) -> str:
        """Generate a comprehensive blog post analyzing today's news."""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y년 %m월 %d일")
        weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]

        # Group by category
        by_category: Dict[str, List[Dict[str, Any]]] = {}
        for article in articles:
            cat = article.get("category", "기타")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(article)

        # Build blog post
        template = f"""# 📰 {date_str} ({weekday}요일) 오늘의 뉴스 브리핑

안녕하세요! 오늘 하루 동안 있었던 주요 뉴스들을 분야별로 정리해드립니다.

---

"""
        # Generate each category section
        category_order = ["politics", "economy", "society", "world", "it", "life"]

        for cat in category_order:
            if cat not in by_category:
                continue

            cat_articles = by_category[cat]
            meta = self.CATEGORY_META.get(cat, {"name": cat, "emoji": "📰", "intro": ""})

            template += f"## {meta['emoji']} {meta['name']}\n\n"
            template += f"{meta['intro']}\n\n"

            # Generate analytical content for this category
            template += self._generate_category_analysis(cat_articles)
            template += "\n---\n\n"

        # Add references section
        template += "## 📚 참고 기사\n\n"
        for cat in category_order:
            if cat not in by_category:
                continue
            meta = self.CATEGORY_META.get(cat, {"name": cat})
            template += f"**{meta['name']}**\n"
            for article in by_category[cat][:5]:  # Max 5 per category
                title = article.get("title", "제목 없음")
                url = article.get("url", "#")
                source = article.get("source", "")
                template += f"- [{title}]({url}) - {source}\n"
            template += "\n"

        template += f"""---

*본 글은 {date.strftime('%Y-%m-%d %H:%M')}에 자동 생성되었습니다.*
"""
        return template

    def _generate_category_analysis(self, articles: List[Dict[str, Any]]) -> str:
        """Generate analytical content for a category from multiple articles."""
        if not articles:
            return "이 분야의 주요 뉴스가 없습니다.\n"

        content_parts = []

        # Process top articles (up to 5)
        top_articles = articles[:5]

        for i, article in enumerate(top_articles):
            title = article.get("title", "")
            summary = article.get("summary", "")
            source = article.get("source", "")

            if not summary:
                summary = title

            # Clean up summary
            summary = summary.strip()
            if summary and not summary.endswith(('.', '다', '요')):
                summary += "."

            # Format each article's content
            if i == 0:
                # Lead article - more prominent
                content_parts.append(f"### 📌 {title}\n")
                content_parts.append(f"{summary}\n")
                if source:
                    content_parts.append(f"({source} 보도)\n")
            else:
                # Supporting articles
                content_parts.append(f"### {title}\n")
                content_parts.append(f"{summary}\n")

        return "\n".join(content_parts)

    def generate_category_blog_post(
        self, articles: List[Dict[str, Any]], category: str, date: Optional[datetime] = None
    ) -> str:
        """Generate a detailed blog post for a single category."""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y년 %m월 %d일")
        meta = self.CATEGORY_META.get(category, {"name": category, "emoji": "📰", "intro": ""})

        template = f"""# {meta['emoji']} {date_str} {meta['name']} 뉴스 정리

{meta['intro']}

---

"""
        # Main content
        template += self._generate_category_analysis(articles)

        # References
        template += "\n---\n\n## 📚 원문 기사\n\n"
        for article in articles[:10]:
            title = article.get("title", "제목 없음")
            url = article.get("url", "#")
            source = article.get("source", "")
            template += f"- [{title}]({url}) - {source}\n"

        template += f"""
---

*{date.strftime('%Y-%m-%d %H:%M')} 생성*
"""
        return template
