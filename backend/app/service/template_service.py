"""Template service for insightful blog post generation.

4-Stage Pipeline:
1. 제목/맥락 이해
2. 핵심 문장 추출 (Fact)
3. 의미 해석 (Insight)
4. 방향성 제시 (So What)
"""
from datetime import datetime
from typing import Dict, Any, Optional, List


class TemplateService:
    """뉴스를 읽고 생각을 정리하는 블로거 스타일 템플릿 생성."""

    CATEGORY_META = {
        "politics": {"name": "정치", "emoji": "🏛️"},
        "economy": {"name": "경제", "emoji": "💰"},
        "society": {"name": "사회", "emoji": "🚔"},
        "life": {"name": "생활/문화", "emoji": "🌸"},
        "world": {"name": "세계", "emoji": "🌍"},
        "it": {"name": "IT/과학", "emoji": "🤖"},
    }

    def generate_template(self, article: Dict[str, Any]) -> str:
        """단일 기사 템플릿."""
        title = article.get("title", "제목 없음")
        category = article.get("category", "기타")
        source = article.get("source", "")
        url = article.get("url", "#")
        summary = article.get("summary", "")

        meta = self.CATEGORY_META.get(category, {"name": category, "emoji": "📰"})

        template = f"""### 🔹 {title}

{summary.strip() if summary else '_요약 정보 없음_'}

**출처**: [{source}]({url})

---
"""
        return template

    def generate_daily_digest_template(
        self, articles: list[Dict[str, Any]], date: Optional[datetime] = None
    ) -> str:
        """전체 카테고리 일일 다이제스트."""
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

        template = f"""# {date_str} ({weekday}) 뉴스 정리

오늘 주요 뉴스를 분야별로 정리했습니다.
단순 요약이 아니라, **왜 이게 중요한지**와 **앞으로 어떤 의미가 있는지** 중심으로 살펴봅니다.

---

"""
        category_order = ["economy", "politics", "it", "society", "world", "life"]

        for cat in category_order:
            if cat not in by_category:
                continue

            cat_articles = by_category[cat]
            meta = self.CATEGORY_META.get(cat, {"emoji": "📰", "name": cat})

            template += f"## {meta['emoji']} {meta['name']}\n\n"
            template += self._generate_category_content(cat, cat_articles)
            template += "\n---\n\n"

        # 오늘의 흐름 정리
        template += self._generate_closing(by_category)

        # 참고 기사
        template += self._generate_references(by_category, category_order)

        template += f"\n*{date.strftime('%Y-%m-%d %H:%M')} 작성*\n"
        return template

    def _generate_category_content(self, category: str, articles: List[Dict[str, Any]]) -> str:
        """카테고리별 4단계 파이프라인 적용."""
        if not articles:
            return "오늘은 특별한 이슈가 없었습니다.\n"

        if category == "economy":
            return self._content_economy(articles)
        elif category == "politics":
            return self._content_politics(articles)
        elif category == "it":
            return self._content_tech(articles)
        elif category == "society":
            return self._content_society(articles)
        elif category == "world":
            return self._content_world(articles)
        else:
            return self._content_general(articles)

    def _content_economy(self, articles: List[Dict[str, Any]]) -> str:
        """경제: 사실 + 예측 / 시장심리·자산·기업 영향."""
        lines = []

        for i, art in enumerate(articles[:3]):
            title = art.get("title", "")
            summary = art.get("summary", "") or title

            lines.append(f"### 🔹 {title}\n")

            # ① 핵심 사실
            lines.append(f"{summary}\n")

            if i == 0:
                # ② 인사이트 해석
                lines.append("")
                lines.append("이번 소식의 핵심은 수치 자체보다,")
                lines.append("**시장이 이를 어떤 신호로 받아들이느냐**에 있다.")
                lines.append("단기 반응에 휘둘리기보다, 방향성 확인 차원에서 볼 필요가 있다.")
                lines.append("")

                # ③ 향후 방향성
                lines.append("단기적으로는 큰 변동성이 없을 가능성이 높지만,")
                lines.append("중장기적으로는 자금 조달 비용과 투자 심리에 영향을 줄 수 있다.")
                lines.append("향후 정책 변화 가능성은 계속해서 체크할 필요가 있다.")
                lines.append("")

        return "\n".join(lines)

    def _content_politics(self, articles: List[Dict[str, Any]]) -> str:
        """정치: 정책 방향 + 파급효과."""
        lines = []

        for i, art in enumerate(articles[:3]):
            title = art.get("title", "")
            summary = art.get("summary", "") or title

            lines.append(f"### 🔹 {title}\n")
            lines.append(f"{summary}\n")

            if i == 0:
                lines.append("")
                lines.append("단순히 '이런 발언이 있었다' 수준이 아니라,")
                lines.append("이 흐름이 **실제 정책으로 이어질 가능성**이 있는지가 핵심이다.")
                lines.append("")
                lines.append("정치 뉴스는 당장 체감되지 않지만,")
                lines.append("몇 달 뒤 규제나 제도 변화로 돌아오는 경우가 많다.")
                lines.append("지금의 발언이 나중에 어떤 형태로 구체화될지 지켜볼 필요가 있다.")
                lines.append("")

        return "\n".join(lines)

    def _content_tech(self, articles: List[Dict[str, Any]]) -> str:
        """IT/과학: 기술 변화 + 실무 활용."""
        lines = []

        for i, art in enumerate(articles[:3]):
            title = art.get("title", "")
            summary = art.get("summary", "") or title

            lines.append(f"### 🔹 {title}\n")
            lines.append(f"{summary}\n")

            if i == 0:
                lines.append("")
                lines.append("이 흐름이 의미 있는 이유는")
                lines.append("해당 기술이 더 이상 '특별한 것'이 아니라")
                lines.append("**기본적인 업무 도구로 자리 잡기 시작했기 때문**이다.")
                lines.append("")
                lines.append("개발자나 실무자 입장에서는")
                lines.append("'직접 처리하는 역할'보다")
                lines.append("'자동화 구조를 설계하는 역할'의 중요성이 커지고 있다.")
                lines.append("")
                lines.append("앞으로는 기술을 얼마나 잘 아느냐보다,")
                lines.append("**어디에 어떻게 쓰느냐**가 더 중요한 판단 기준이 될 가능성이 크다.")
                lines.append("")

        return "\n".join(lines)

    def _content_society(self, articles: List[Dict[str, Any]]) -> str:
        """사회: 영향 + 맥락 / 누구에게, 왜 지금, 구조적 문제."""
        lines = []

        for i, art in enumerate(articles[:3]):
            title = art.get("title", "")
            summary = art.get("summary", "") or title

            lines.append(f"### 🔹 {title}\n")
            lines.append(f"{summary}\n")

            if i == 0:
                lines.append("")
                lines.append("이 이슈는 단순히 개별 사건을 넘어서,")
                lines.append("**생활비 전반과 연결된 구조적 문제**와 맞닿아 있다.")
                lines.append("")
                lines.append("지금 이 논의가 나오는 이유는")
                lines.append("누적된 비용 구조가 한계에 다다랐기 때문이다.")
                lines.append("단기 결론보다,")
                lines.append("향후 다른 영역으로 확산될 가능성도 함께 살펴볼 필요가 있다.")
                lines.append("")

        return "\n".join(lines)

    def _content_world(self, articles: List[Dict[str, Any]]) -> str:
        """세계: 글로벌 흐름 + 국내 영향."""
        lines = []

        for i, art in enumerate(articles[:3]):
            title = art.get("title", "")
            summary = art.get("summary", "") or title

            lines.append(f"### 🔹 {title}\n")
            lines.append(f"{summary}\n")

            if i == 0:
                lines.append("")
                lines.append("국제 뉴스는 '남의 나라 일'처럼 보이지만,")
                lines.append("**공급망, 환율, 수출입에 직접 영향**을 준다.")
                lines.append("")
                lines.append("글로벌 흐름을 읽는 건 교양이 아니라 실무다.")
                lines.append("특히 수출 의존도가 높은 업종이라면 주의 깊게 볼 필요가 있다.")
                lines.append("")

        return "\n".join(lines)

    def _content_general(self, articles: List[Dict[str, Any]]) -> str:
        """일반 카테고리."""
        lines = []
        for art in articles[:3]:
            title = art.get("title", "")
            summary = art.get("summary", "") or title
            lines.append(f"### 🔹 {title}\n")
            lines.append(f"{summary}\n")
            lines.append("")
        return "\n".join(lines)

    def _generate_closing(self, by_category: Dict) -> str:
        """오늘의 흐름 한 줄 정리."""
        lines = []
        lines.append("## 📌 오늘의 흐름\n")

        has_economy = "economy" in by_category
        has_politics = "politics" in by_category
        has_tech = "it" in by_category

        lines.append("오늘 뉴스들을 종합해보면,")

        if has_economy and has_politics:
            lines.append("정책과 경제는 여전히 조심스러운 태도를 유지하고 있지만")
        if has_tech:
            lines.append("기술과 산업 현장에서는 이미 다음 단계로 빠르게 이동하고 있다는 인상이 강하다.")

        lines.append("")
        lines.append("변화는 조용히 진행되고 있지만,")
        lines.append("**준비하지 않은 쪽이 더 크게 흔들릴 가능성**은 점점 커지고 있다.")
        lines.append("")
        lines.append("내일도 주요 흐름 정리해서 올리겠습니다.")
        lines.append("")

        return "\n".join(lines)

    def _generate_references(self, by_category: Dict, category_order: List[str]) -> str:
        """참고 기사 목록."""
        lines = []
        lines.append("---\n")
        lines.append("<details>")
        lines.append("<summary>📚 참고 기사 목록</summary>\n")

        for cat in category_order:
            if cat not in by_category:
                continue
            meta = self.CATEGORY_META.get(cat, {"name": cat})
            lines.append(f"**{meta['name']}**")
            for art in by_category[cat][:5]:
                title = art.get("title", "제목 없음")
                url = art.get("url", "#")
                source = art.get("source", "")
                lines.append(f"- [{title}]({url}) ({source})")
            lines.append("")

        lines.append("</details>\n")
        return "\n".join(lines)

    def generate_category_blog_post(
        self, articles: List[Dict[str, Any]], category: str, date: Optional[datetime] = None
    ) -> str:
        """단일 카테고리 상세 블로그."""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y년 %m월 %d일")
        weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
        meta = self.CATEGORY_META.get(category, {"emoji": "📰", "name": category})

        template = f"""# {meta['emoji']} {date_str} ({weekday}) {meta['name']} 정리

오늘 {meta['name']} 분야 주요 뉴스를 정리합니다.

---

"""
        template += self._generate_category_content(category, articles)

        template += """
---

## 정리하며

오늘 다룬 내용이 당장은 와닿지 않을 수도 있다.
하지만 이런 뉴스들이 쌓이면서 큰 흐름을 만들고,
어느 순간 우리 일상에 직접적인 영향을 주게 된다.

꾸준히 관심 갖고 지켜보는 게 중요하다.

---

<details>
<summary>📚 참고 기사</summary>

"""
        for art in articles[:10]:
            title = art.get("title", "제목 없음")
            url = art.get("url", "#")
            source = art.get("source", "")
            template += f"- [{title}]({url}) ({source})\n"

        template += "\n</details>\n\n"
        template += f"*{date.strftime('%Y-%m-%d %H:%M')} 작성*\n"

        return template
