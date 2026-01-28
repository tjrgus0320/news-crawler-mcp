"""Template service for blog post generation."""
from datetime import datetime
from typing import Dict, Any, Optional


class TemplateService:
    """Service for generating blog post templates."""

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
        category_names = {
            "politics": "정치",
            "economy": "경제",
            "society": "사회",
            "life": "생활/문화",
            "world": "세계",
            "it": "IT/과학",
        }
        category_kr = category_names.get(category, category)

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
        """Generate a daily digest template."""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y년 %m월 %d일")

        template = f"""# 📰 {date_str} 오늘의 뉴스

> 자동 생성된 뉴스 다이제스트입니다.

---

"""
        # Group by category
        by_category: Dict[str, list] = {}
        for article in articles:
            cat = article.get("category", "기타")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(article)

        category_names = {
            "politics": "🏛️ 정치",
            "economy": "💰 경제",
            "society": "👥 사회",
            "life": "🌸 생활/문화",
            "world": "🌍 세계",
            "it": "💻 IT/과학",
        }

        for cat, cat_articles in by_category.items():
            cat_name = category_names.get(cat, cat)
            template += f"\n## {cat_name}\n\n"

            for article in cat_articles:
                title = article.get("title", "제목 없음")
                source = article.get("source", "")
                url = article.get("url", "#")
                template += f"- [{title}]({url}) ({source})\n"

        template += f"\n---\n\n*생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"

        return template
