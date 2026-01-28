"""Template service for insightful blog post generation."""
from datetime import datetime
from typing import Dict, Any, Optional, List


class TemplateService:
    """Service for generating insightful blog post templates."""

    CATEGORY_META = {
        "politics": {
            "name": "정치",
            "emoji": "🏛️",
            "section_title": "정치",
        },
        "economy": {
            "name": "경제",
            "emoji": "💰",
            "section_title": "경제",
        },
        "society": {
            "name": "사회",
            "emoji": "👥",
            "section_title": "사회",
        },
        "life": {
            "name": "생활/문화",
            "emoji": "🌸",
            "section_title": "생활/문화",
        },
        "world": {
            "name": "세계",
            "emoji": "🌍",
            "section_title": "세계",
        },
        "it": {
            "name": "IT/과학",
            "emoji": "💻",
            "section_title": "IT / 과학",
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

        if published_at and isinstance(published_at, str):
            try:
                published_at = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            except ValueError:
                published_at = None

        date_str = published_at.strftime("%Y-%m-%d") if published_at else datetime.now().strftime("%Y-%m-%d")
        meta = self.CATEGORY_META.get(category, {"name": category})

        template = f"""## [{meta['name']}] {title}

📅 {date_str} | 📰 {source}

{summary.strip() if summary else '_요약 정보 없음_'}

**[원문 보기]({url})**

---
"""
        return template

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
        template = f"""# {date_str} ({weekday}) 뉴스 정리

오늘 하루 주요 뉴스들을 분야별로 정리했습니다.
단순 나열이 아니라, **왜 이게 중요한지** 그리고 **앞으로 어떤 의미가 있는지** 중심으로 살펴봅니다.

---

"""
        category_order = ["politics", "economy", "it", "society", "world", "life"]
        category_insights = []

        for cat in category_order:
            if cat not in by_category:
                continue

            cat_articles = by_category[cat]
            meta = self.CATEGORY_META.get(cat, {"emoji": "📰", "section_title": cat})

            template += f"## {meta['emoji']} {meta['section_title']}\n\n"

            # Generate insightful content
            insight = self._generate_category_insight(cat, cat_articles)
            template += insight["content"]
            if insight["key_message"]:
                category_insights.append(insight["key_message"])

            template += "\n---\n\n"

        # Add closing summary - 오늘의 흐름 한 줄 정리
        template += self._generate_daily_closing(category_insights, by_category)

        # References
        template += "\n---\n\n"
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

    def _generate_category_insight(self, category: str, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insightful analysis for a category."""
        if not articles:
            return {"content": "오늘은 특별한 이슈가 없었습니다.\n", "key_message": None}

        if category == "politics":
            return self._insight_politics(articles)
        elif category == "economy":
            return self._insight_economy(articles)
        elif category == "it":
            return self._insight_tech(articles)
        elif category == "world":
            return self._insight_world(articles)
        elif category == "society":
            return self._insight_society(articles)
        else:
            return self._insight_general(articles)

    def _insight_politics(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """정치 뉴스 인사이트."""
        lines = []
        main = articles[0]
        title = main.get("title", "")
        summary = main.get("summary", "") or title

        lines.append(f"{summary}\n")
        lines.append("")
        lines.append("단순히 '이런 발언이 있었다' 수준이 아니라,")
        lines.append("이 흐름이 **정책으로 이어질 가능성**이 있는지를 봐야 한다.")
        lines.append("정치 뉴스는 당장 체감되지 않지만, 몇 달 뒤 규제나 제도로 돌아온다.")
        lines.append("")

        if len(articles) > 1:
            lines.append("한편, 다른 움직임도 있었다.")
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        lines.append("> \"정책은 뉴스에서 시작해서, 내 지갑에서 끝난다.\"")
        lines.append("")

        return {
            "content": "\n".join(lines),
            "key_message": "정책 변화 신호"
        }

    def _insight_economy(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """경제 뉴스 인사이트."""
        lines = []
        main = articles[0]
        summary = main.get("summary", "") or main.get("title", "")

        lines.append(f"{summary}\n")
        lines.append("")
        lines.append("경제 지표는 숫자 자체보다 **방향성**이 중요하다.")
        lines.append("한 번의 등락보다, 연속된 흐름이 어디를 향하는지 봐야 한다.")
        lines.append("")

        if len(articles) > 1:
            lines.append("관련해서 같이 볼 만한 뉴스:")
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        lines.append("단기 이슈에 휘둘리기보다, 큰 그림에서 내 자산과 커리어에 어떤 영향이 있을지 생각해볼 필요가 있다.")
        lines.append("")
        lines.append("> \"시장은 예측하는 게 아니라, 대응하는 것이다.\"")
        lines.append("")

        return {
            "content": "\n".join(lines),
            "key_message": "시장 흐름 변화"
        }

    def _insight_tech(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """IT/과학 뉴스 인사이트."""
        lines = []
        main = articles[0]
        summary = main.get("summary", "") or main.get("title", "")

        lines.append(f"{summary}\n")
        lines.append("")
        lines.append("기술 뉴스를 볼 때 항상 던지는 질문이 있다.")
        lines.append("**\"왜 지금 이게 나왔을까?\"**")
        lines.append("")
        lines.append("기업들의 발표에는 이유가 있고,")
        lines.append("그 방향성을 읽으면 다음에 뭐가 올지 어느 정도 예측할 수 있다.")
        lines.append("")

        if len(articles) > 1:
            lines.append("함께 눈여겨볼 뉴스:")
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        lines.append("개발자나 IT 업계 종사자라면, 이런 변화가 내 업무에 어떤 영향을 줄지 생각해볼 타이밍이다.")
        lines.append("새 기술이 나왔을 때, 기회가 될지 위협이 될지는 준비 여부에 달려 있다.")
        lines.append("")
        lines.append("> \"직접 손으로 하던 일보다, 자동화 구조를 설계하는 사람이 더 중요해진다.\"")
        lines.append("")

        return {
            "content": "\n".join(lines),
            "key_message": "기술 트렌드 전환"
        }

    def _insight_world(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """세계 뉴스 인사이트."""
        lines = []
        main = articles[0]
        summary = main.get("summary", "") or main.get("title", "")

        lines.append(f"{summary}\n")
        lines.append("")
        lines.append("국제 뉴스는 '남의 나라 일'처럼 보이지만,")
        lines.append("공급망, 환율, 수출입에 직접 영향을 준다.")
        lines.append("")

        if len(articles) > 1:
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        lines.append("글로벌 흐름을 읽는 건 교양이 아니라 실무다.")
        lines.append("")

        return {
            "content": "\n".join(lines),
            "key_message": "글로벌 변수"
        }

    def _insight_society(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """사회 뉴스 인사이트."""
        lines = []
        main = articles[0]
        summary = main.get("summary", "") or main.get("title", "")

        lines.append(f"{summary}\n")
        lines.append("")
        lines.append("사회 이슈는 단순한 사건 사고가 아니라,")
        lines.append("우리 사회가 어디로 가고 있는지 보여주는 신호다.")
        lines.append("")

        if len(articles) > 1:
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        return {
            "content": "\n".join(lines),
            "key_message": "사회 변화 신호"
        }

    def _insight_general(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """일반 카테고리 인사이트."""
        lines = []
        for art in articles[:3]:
            title = art.get("title", "")
            summary = art.get("summary", "") or title
            lines.append(f"**{title}**")
            lines.append(f"{self._shorten(summary, 200)}")
            lines.append("")

        return {"content": "\n".join(lines), "key_message": None}

    def _generate_daily_closing(self, insights: List[str], by_category: Dict) -> str:
        """오늘의 흐름 한 줄 정리."""
        lines = []
        lines.append("## 📌 오늘의 흐름 한 줄 정리\n")
        lines.append("")

        # Create a cohesive closing based on what categories were present
        has_politics = "politics" in by_category
        has_economy = "economy" in by_category
        has_tech = "it" in by_category

        if has_politics and has_economy:
            lines.append("오늘 뉴스를 종합해보면,")
            lines.append("정책과 경제는 여전히 조심스러운 태도를 유지하고 있지만")
        elif has_economy:
            lines.append("오늘 경제 뉴스를 보면,")
            lines.append("시장은 방향을 탐색하는 중이다.")
        else:
            lines.append("오늘 뉴스들을 종합해보면,")

        if has_tech:
            lines.append("기술과 산업 현장에서는 이미 다음 단계로 빠르게 이동하고 있다는 인상이 강하다.")

        lines.append("")
        lines.append("변화는 조용히 진행되고 있지만,")
        lines.append("**준비하지 않은 쪽이 더 크게 흔들릴 가능성**은 점점 커지고 있다.")
        lines.append("")
        lines.append("내일도 주요 흐름 정리해서 올리겠습니다.")
        lines.append("")

        return "\n".join(lines)

    def _shorten(self, text: str, max_len: int) -> str:
        """Shorten text."""
        if not text:
            return ""
        text = text.strip()
        return text if len(text) <= max_len else text[:max_len] + "..."

    def generate_category_blog_post(
        self, articles: List[Dict[str, Any]], category: str, date: Optional[datetime] = None
    ) -> str:
        """Generate a detailed blog post for a single category."""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y년 %m월 %d일")
        weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
        meta = self.CATEGORY_META.get(category, {"emoji": "📰", "section_title": category, "name": category})

        template = f"""# {meta['emoji']} {date_str} ({weekday}) {meta['section_title']} 정리

오늘 {meta['name']} 분야 주요 뉴스를 정리합니다.

---

"""
        insight = self._generate_category_insight(category, articles)
        template += insight["content"]

        template += """
---

## 정리하며

오늘 다룬 내용이 당장은 와닿지 않을 수도 있다.
하지만 이런 뉴스들이 쌓이면서 큰 흐름을 만들고,
어느 순간 우리 일상에 직접적인 영향을 주게 된다.

꾸준히 관심 갖고 지켜보는 게 중요하다.

---

"""
        template += "<details>\n<summary>📚 참고 기사</summary>\n\n"
        for article in articles[:10]:
            title = article.get("title", "제목 없음")
            url = article.get("url", "#")
            source = article.get("source", "")
            template += f"- [{title}]({url}) ({source})\n"
        template += "\n</details>\n\n"

        template += f"*{date.strftime('%Y-%m-%d %H:%M')} 작성*\n"
        return template
