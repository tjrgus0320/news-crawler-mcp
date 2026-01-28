"""Template service for blog post generation."""
from datetime import datetime
from typing import Dict, Any, Optional, List


class TemplateService:
    """Service for generating insightful blog post templates."""

    # Category metadata with analysis prompts
    CATEGORY_META = {
        "politics": {
            "name": "정치",
            "emoji": "🏛️",
            "section_title": "정치 동향 분석",
            "perspective": "정책 변화와 그 파급효과",
        },
        "economy": {
            "name": "경제",
            "emoji": "💰",
            "section_title": "경제 흐름 읽기",
            "perspective": "시장과 일상에 미치는 영향",
        },
        "society": {
            "name": "사회",
            "emoji": "👥",
            "section_title": "사회 이슈 톺아보기",
            "perspective": "우리 삶에 던지는 질문",
        },
        "life": {
            "name": "생활/문화",
            "emoji": "🌸",
            "section_title": "생활 트렌드 체크",
            "perspective": "변화하는 라이프스타일",
        },
        "world": {
            "name": "세계",
            "emoji": "🌍",
            "section_title": "글로벌 시선",
            "perspective": "국제 정세가 우리에게 미치는 영향",
        },
        "it": {
            "name": "IT/과학",
            "emoji": "💻",
            "section_title": "테크 인사이트",
            "perspective": "기술이 만드는 변화의 방향",
        },
    }

    def generate_template(self, article: Dict[str, Any]) -> str:
        """Generate a blog post template from a single article."""
        title = article.get("title", "제목 없음")
        category = article.get("category", "기타")
        source = article.get("source", "알 수 없음")
        url = article.get("url", "#")
        summary = article.get("summary", "")
        published_at = article.get("published_at")

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

        meta = self.CATEGORY_META.get(category, {"name": category, "emoji": "📰"})
        category_kr = meta["name"]

        summary_text = self._format_summary(summary)

        template = f"""## [{category_kr}] {title}

📅 {date_str} | 📰 {source}

{summary_text}

**[원문 보기]({url})**

---
"""
        return template

    def _format_summary(self, summary: str) -> str:
        """Format summary into readable paragraphs."""
        if not summary:
            return "_요약 정보가 없습니다._"
        return summary.strip()

    def generate_daily_digest_template(
        self, articles: list[Dict[str, Any]], date: Optional[datetime] = None
    ) -> str:
        """Generate a comprehensive daily news analysis blog post."""
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
        template = f"""# {date_str} ({weekday}) 뉴스 브리핑

오늘 하루, 눈여겨볼 뉴스들을 정리해봤습니다.

단순히 "이런 일이 있었다"가 아니라, **왜 이게 중요한지**, 그리고 **앞으로 어떤 영향을 줄 수 있는지** 위주로 살펴봅니다.

---

"""
        # Generate each category section
        category_order = ["politics", "economy", "it", "society", "world", "life"]

        for cat in category_order:
            if cat not in by_category:
                continue

            cat_articles = by_category[cat]
            meta = self.CATEGORY_META.get(cat, {"name": cat, "emoji": "📰", "section_title": cat})

            template += f"## {meta['emoji']} {meta['section_title']}\n\n"

            # Generate insightful content for this category
            template += self._generate_insightful_analysis(cat, cat_articles)
            template += "\n---\n\n"

        # Closing thoughts
        template += """## 마무리하며

오늘 뉴스를 보면서 느낀 건, 변화의 속도가 점점 빨라지고 있다는 점입니다.
당장은 체감되지 않더라도, 이런 흐름들이 쌓이면 어느 순간 우리 일상에 직접적인 영향을 주게 됩니다.

내일도 주요 이슈들 정리해서 올리겠습니다.

"""
        # Add references
        template += "---\n\n"
        template += "<details>\n<summary>📚 참고 기사 목록</summary>\n\n"
        for cat in category_order:
            if cat not in by_category:
                continue
            meta = self.CATEGORY_META.get(cat, {"name": cat})
            template += f"**{meta['name']}**\n"
            for article in by_category[cat][:5]:
                title = article.get("title", "제목 없음")
                url = article.get("url", "#")
                source = article.get("source", "")
                template += f"- [{title}]({url}) ({source})\n"
            template += "\n"
        template += "</details>\n\n"

        template += f"*{date.strftime('%Y-%m-%d %H:%M')} 작성*\n"
        return template

    def _generate_insightful_analysis(self, category: str, articles: List[Dict[str, Any]]) -> str:
        """Generate insightful analysis content for a category."""
        if not articles:
            return "오늘은 특별한 이슈가 없었습니다.\n"

        content_parts = []
        top_articles = articles[:5]

        # Opening context based on category
        if category == "politics":
            content_parts.append(self._analyze_politics(top_articles))
        elif category == "economy":
            content_parts.append(self._analyze_economy(top_articles))
        elif category == "it":
            content_parts.append(self._analyze_tech(top_articles))
        else:
            content_parts.append(self._analyze_general(category, top_articles))

        return "\n".join(content_parts)

    def _analyze_politics(self, articles: List[Dict[str, Any]]) -> str:
        """Generate political analysis."""
        content = []

        for i, article in enumerate(articles[:3]):
            title = article.get("title", "")
            summary = article.get("summary", "") or title

            if i == 0:
                content.append(f"**{title}**\n")
                content.append(f"{summary}\n")
                content.append("")
                content.append("이 이슈가 중요한 이유는, 단순히 오늘의 뉴스로 끝나지 않기 때문입니다. ")
                content.append("정책 방향이 바뀌면 그 여파는 몇 달 뒤, 혹은 몇 년 뒤에 체감되기 마련입니다.")
                content.append("")
            else:
                content.append(f"한편, **{title}** 소식도 있었습니다.")
                content.append(f"{self._shorten(summary, 150)}")
                content.append("")

        content.append("정치 뉴스는 당장 피부에 와닿지 않아도, 결국 정책으로 이어지고 우리 생활에 영향을 줍니다. ")
        content.append("이런 흐름을 꾸준히 지켜보는 게 중요합니다.")
        content.append("")

        return "\n".join(content)

    def _analyze_economy(self, articles: List[Dict[str, Any]]) -> str:
        """Generate economic analysis."""
        content = []

        for i, article in enumerate(articles[:3]):
            title = article.get("title", "")
            summary = article.get("summary", "") or title

            if i == 0:
                content.append(f"**{title}**\n")
                content.append(f"{summary}\n")
                content.append("")
                content.append("경제 지표나 시장 움직임은 개인에게 직접적인 영향을 줍니다. ")
                content.append("금리, 환율, 물가 - 이런 숫자들이 결국 우리 지갑 사정을 결정하니까요.")
                content.append("")
            else:
                content.append(f"또한, **{title}**")
                content.append(f"{self._shorten(summary, 150)}")
                content.append("")

        content.append("단기적인 등락에 일희일비하기보다는, 전체적인 흐름이 어디로 향하는지 보는 게 중요합니다.")
        content.append("")

        return "\n".join(content)

    def _analyze_tech(self, articles: List[Dict[str, Any]]) -> str:
        """Generate tech/IT analysis."""
        content = []

        for i, article in enumerate(articles[:3]):
            title = article.get("title", "")
            summary = article.get("summary", "") or title

            if i == 0:
                content.append(f"**{title}**\n")
                content.append(f"{summary}\n")
                content.append("")
                content.append("기술 뉴스를 볼 때 항상 생각하는 건, '왜 지금 이게 나왔을까?'입니다. ")
                content.append("기업들의 움직임에는 이유가 있고, 그 방향성을 읽으면 다음 변화를 예측할 수 있습니다.")
                content.append("")
            else:
                content.append(f"**{title}**도 눈여겨볼 만합니다.")
                content.append(f"{self._shorten(summary, 150)}")
                content.append("")

        content.append("개발자나 IT 업계 종사자라면, 이런 변화가 내 업무에 어떤 영향을 줄지 한 번쯤 생각해볼 필요가 있습니다. ")
        content.append("새로운 기술이 나왔을 때, 그게 기회가 될지 위협이 될지는 준비 여부에 달려 있으니까요.")
        content.append("")

        return "\n".join(content)

    def _analyze_general(self, category: str, articles: List[Dict[str, Any]]) -> str:
        """Generate general category analysis."""
        meta = self.CATEGORY_META.get(category, {"perspective": ""})
        content = []

        for i, article in enumerate(articles[:3]):
            title = article.get("title", "")
            summary = article.get("summary", "") or title

            if i == 0:
                content.append(f"**{title}**\n")
                content.append(f"{summary}\n")
                content.append("")
            else:
                content.append(f"**{title}**")
                content.append(f"{self._shorten(summary, 150)}")
                content.append("")

        return "\n".join(content)

    def _shorten(self, text: str, max_len: int) -> str:
        """Shorten text to max length."""
        if not text:
            return ""
        text = text.strip()
        if len(text) <= max_len:
            return text
        return text[:max_len] + "..."

    def generate_category_blog_post(
        self, articles: List[Dict[str, Any]], category: str, date: Optional[datetime] = None
    ) -> str:
        """Generate a detailed blog post for a single category."""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y년 %m월 %d일")
        weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
        meta = self.CATEGORY_META.get(category, {"name": category, "emoji": "📰", "section_title": category})

        template = f"""# {meta['emoji']} {date_str} ({weekday}) {meta['section_title']}

오늘 {meta['name']} 분야에서 있었던 주요 이슈들을 정리합니다.

---

"""
        # Main analysis content
        template += self._generate_insightful_analysis(category, articles)

        # Closing
        template += """
---

## 정리하며

오늘 다룬 내용들이 당장은 크게 와닿지 않을 수도 있습니다.
하지만 이런 뉴스들이 쌓이면서 큰 흐름을 만들고, 어느 순간 우리 일상에 직접적인 영향을 주게 됩니다.

꾸준히 관심 갖고 지켜보는 게 중요합니다.

---

"""
        # References
        template += "<details>\n<summary>📚 참고 기사</summary>\n\n"
        for article in articles[:10]:
            title = article.get("title", "제목 없음")
            url = article.get("url", "#")
            source = article.get("source", "")
            template += f"- [{title}]({url}) ({source})\n"
        template += "\n</details>\n\n"

        template += f"*{date.strftime('%Y-%m-%d %H:%M')} 작성*\n"
        return template
