"""Template service for human-like blog post generation.

AI 티 제거 기법:
- 문단 길이 불균형
- 애매한 문장 섞기
- 생각 정리 멈춤
- 구어체 표현
- 열린 클로징
"""
from datetime import datetime
from typing import Dict, Any, Optional, List
import random


class TemplateService:
    """뉴스를 읽고 생각을 정리하는 블로거 스타일 템플릿."""

    CATEGORY_META = {
        "politics": {"name": "정치", "emoji": "🏛️"},
        "economy": {"name": "경제", "emoji": "💰"},
        "society": {"name": "사회", "emoji": "🚔"},
        "life": {"name": "생활/문화", "emoji": "🌸"},
        "world": {"name": "세계", "emoji": "🌍"},
        "it": {"name": "IT/과학", "emoji": "🤖"},
    }

    # 애매한 문장들 (의도적 여지)
    UNCERTAIN_PHRASES = [
        "아직 명확한 결론을 내리긴 어렵다.",
        "조금 더 지켜봐야 할 지점이다.",
        "이 부분은 해석이 갈릴 수 있다.",
        "확신하긴 이르지만, 방향성은 읽힌다.",
        "단정 짓기엔 변수가 많다.",
    ]

    # 생각 멈춤 문장들
    PAUSE_PHRASES = [
        "여기서 한 번 짚고 넘어갈 필요가 있다.",
        "이 부분이 좀 걸린다.",
        "잠깐, 이건 좀 다른 얘기다.",
        "근데 생각해보면,",
    ]

    def generate_template(self, article: Dict[str, Any]) -> str:
        """단일 기사 템플릿."""
        title = article.get("title", "제목 없음")
        source = article.get("source", "")
        url = article.get("url", "#")
        summary = article.get("summary", "")

        return f"""### 🔹 {title}

{summary.strip() if summary else '_요약 정보 없음_'}

**출처**: [{source}]({url})

---
"""

    def generate_daily_digest_template(
        self, articles: list[Dict[str, Any]], date: Optional[datetime] = None
    ) -> str:
        """전체 카테고리 일일 다이제스트."""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y년 %m월 %d일")
        weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]

        by_category: Dict[str, List[Dict[str, Any]]] = {}
        for article in articles:
            cat = article.get("category", "기타")
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(article)

        template = f"""# 📰 오늘의 뉴스, 오늘의 흐름 ({date_str} {weekday})

오늘 하루 쏟아진 뉴스 중,
흐름이 느껴지는 이슈만 정리했습니다.

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

        template += self._generate_closing(by_category)
        template += self._generate_references(by_category, category_order)
        template += f"\n*{date.strftime('%Y-%m-%d %H:%M')} 작성*\n"

        return template

    def _generate_category_content(self, category: str, articles: List[Dict[str, Any]]) -> str:
        """카테고리별 콘텐츠 - AI 티 제거 적용."""
        if not articles:
            return "오늘은 특별한 이슈 없었습니다.\n"

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
        """경제 - 문단 불균형 + 애매한 문장."""
        lines = []
        main = articles[0]
        title = main.get("title", "")
        summary = main.get("summary", "") or title

        # 짧은 문단
        lines.append(f"### 🔹 {title}\n")
        lines.append(f"{summary}")
        lines.append("")

        # 긴 문단 (4-5줄)
        lines.append("이번 소식을 어떻게 볼 것이냐.")
        lines.append("숫자 자체보다 **시장이 이걸 어떤 신호로 받아들이느냐**가 더 중요하다.")
        lines.append("당장 반응이 크지 않더라도,")
        lines.append("방향이 바뀌는 초기 신호일 수 있다.")
        lines.append("")

        # 생각 멈춤
        lines.append("여기서 한 번 짚고 넘어갈 게 있다.")
        lines.append("")

        # 짧은 문단 (1-2줄)
        lines.append("단기 반응에 휘둘릴 필요는 없다.")
        lines.append("다만, 이 방향이 계속되는지는 체크해둘 필요가 있다.")
        lines.append("")

        # 애매한 문장
        lines.append(random.choice(self.UNCERTAIN_PHRASES))
        lines.append("")

        if len(articles) > 1:
            lines.append("같이 볼 만한 뉴스:")
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        return "\n".join(lines)

    def _content_politics(self, articles: List[Dict[str, Any]]) -> str:
        """정치 - 구어체 + 열린 해석."""
        lines = []
        main = articles[0]
        title = main.get("title", "")
        summary = main.get("summary", "") or title

        lines.append(f"### 🔹 {title}\n")
        lines.append(f"{summary}")
        lines.append("")

        # 구어체 톤
        lines.append("이걸 단순히 '이런 말이 나왔다' 정도로 보면 안 된다.")
        lines.append("")

        # 긴 문단
        lines.append("정치 뉴스의 특징이 뭐냐면,")
        lines.append("지금 당장은 아무 일도 안 일어난 것 같은데")
        lines.append("몇 달 지나면 규제나 제도로 슬쩍 돌아온다는 거다.")
        lines.append("그래서 이런 발언이 나왔을 때")
        lines.append("**'결국 어디로 가려는 건지'** 방향을 읽어두는 게 낫다.")
        lines.append("")

        # 애매한 문장
        lines.append("물론, 말만 하고 흐지부지될 수도 있다.")
        lines.append("그건 좀 더 봐야 안다.")
        lines.append("")

        if len(articles) > 1:
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        return "\n".join(lines)

    def _content_tech(self, articles: List[Dict[str, Any]]) -> str:
        """IT/과학 - 실무자 시선 + 선택 강요."""
        lines = []
        main = articles[0]
        title = main.get("title", "")
        summary = main.get("summary", "") or title

        lines.append(f"### 🔹 {title}\n")
        lines.append(f"{summary}")
        lines.append("")

        # 생각 멈춤
        lines.append("잠깐.")
        lines.append("")

        lines.append("기술 뉴스 볼 때 항상 던지는 질문이 있다.")
        lines.append("**\"왜 하필 지금 이게 나왔을까?\"**")
        lines.append("")

        # 긴 문단
        lines.append("기업들이 뭔가 발표할 땐 이유가 있다.")
        lines.append("경쟁사 움직임, 시장 타이밍, 내부 로드맵...")
        lines.append("그 맥락을 읽으면 다음에 뭐가 올지 어느 정도 감이 온다.")
        lines.append("")

        # 실무자 관점
        lines.append("개발자나 IT 쪽에서 일하는 사람이라면,")
        lines.append("이게 **내 업무에 어떤 영향 주는지** 한 번쯤 생각해볼 타이밍이다.")
        lines.append("")

        # 짧은 문단 + 인사이트
        lines.append("기술을 '얼마나 아느냐'보다")
        lines.append("**'어디에 어떻게 쓰느냐'**가 더 중요해지는 흐름이다.")
        lines.append("")

        lines.append(random.choice(self.UNCERTAIN_PHRASES))
        lines.append("")

        if len(articles) > 1:
            lines.append("함께 볼 뉴스:")
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        return "\n".join(lines)

    def _content_society(self, articles: List[Dict[str, Any]]) -> str:
        """사회 - 구조적 문제 + 체감 포인트."""
        lines = []
        main = articles[0]
        title = main.get("title", "")
        summary = main.get("summary", "") or title

        lines.append(f"### 🔹 {title}\n")
        lines.append(f"{summary}")
        lines.append("")

        lines.append("이 이슈,")
        lines.append("그냥 개별 사건으로 보면 안 된다.")
        lines.append("")

        lines.append("비슷한 뉴스가 반복해서 나온다는 건")
        lines.append("**구조적으로 뭔가 막혀 있다**는 신호다.")
        lines.append("당장 내 일 아닌 것 같아도,")
        lines.append("결국 생활비나 정책으로 연결되는 경우가 많다.")
        lines.append("")

        lines.append("이 부분은 해석이 갈릴 수 있다.")
        lines.append("좀 더 지켜봐야 할 것 같다.")
        lines.append("")

        if len(articles) > 1:
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        return "\n".join(lines)

    def _content_world(self, articles: List[Dict[str, Any]]) -> str:
        """세계 - 국내 영향 연결."""
        lines = []
        main = articles[0]
        title = main.get("title", "")
        summary = main.get("summary", "") or title

        lines.append(f"### 🔹 {title}\n")
        lines.append(f"{summary}")
        lines.append("")

        lines.append("남의 나라 일 같지만,")
        lines.append("**환율, 수출, 공급망**으로 연결되면 우리 일이 된다.")
        lines.append("")

        lines.append("글로벌 뉴스는 교양으로 보는 게 아니라")
        lines.append("실무적으로 체크하는 게 맞다.")
        lines.append("")

        lines.append(random.choice(self.UNCERTAIN_PHRASES))
        lines.append("")

        if len(articles) > 1:
            for art in articles[1:3]:
                lines.append(f"- {art.get('title', '')}")
            lines.append("")

        return "\n".join(lines)

    def _content_general(self, articles: List[Dict[str, Any]]) -> str:
        """일반."""
        lines = []
        for art in articles[:3]:
            title = art.get("title", "")
            summary = art.get("summary", "") or title
            lines.append(f"### 🔹 {title}\n")
            lines.append(f"{summary}")
            lines.append("")
        return "\n".join(lines)

    def _generate_closing(self, by_category: Dict) -> str:
        """클로징 - 시리즈 시그니처."""
        lines = []
        lines.append("## 📌 오늘의 흐름\n")

        # 흐름 요약
        lines.append("오늘 뉴스들 종합해보면,")
        lines.append("큰 변화보다는 **조용한 이동**이 더 눈에 띈 하루였다.")
        lines.append("")

        lines.append("당장은 체감하기 어렵지만,")
        lines.append("이런 신호들이 쌓일 때 방향은 어느 순간 분명해진다.")
        lines.append("")

        # 다음 관찰 포인트
        lines.append("당분간은 이 포인트들을 지켜보려 한다.")
        lines.append("")

        if "politics" in by_category or "economy" in by_category:
            lines.append("- 정책은 언제 결론이 나는지")
        if "economy" in by_category:
            lines.append("- 시장은 어디서 먼저 반응하는지")
        if "it" in by_category:
            lines.append("- 기술은 실제 현장에 어떻게 스며드는지")

        lines.append("")

        # 개인 시선
        lines.append("개인적으로는,")
        lines.append("오늘 뉴스 중 몇 개는 생각보다 더 길게 영향 줄 것 같다.")
        lines.append("")

        # 시리즈 시그니처
        lines.append("---\n")
        lines.append("오늘의 뉴스는 여기까지입니다.")
        lines.append("내일은 또 어떤 흐름이 이어질지,")
        lines.append("기록해두겠습니다.")
        lines.append("")

        return "\n".join(lines)

    def _generate_references(self, by_category: Dict, category_order: List[str]) -> str:
        """참고 기사."""
        lines = []
        lines.append("---\n")
        lines.append("<details>")
        lines.append("<summary>📚 참고 기사</summary>\n")

        for cat in category_order:
            if cat not in by_category:
                continue
            meta = self.CATEGORY_META.get(cat, {"name": cat})
            lines.append(f"**{meta['name']}**")
            for art in by_category[cat][:5]:
                title = art.get("title", "")
                url = art.get("url", "#")
                source = art.get("source", "")
                lines.append(f"- [{title}]({url}) ({source})")
            lines.append("")

        lines.append("</details>\n")
        return "\n".join(lines)

    def generate_category_blog_post(
        self, articles: List[Dict[str, Any]], category: str, date: Optional[datetime] = None
    ) -> str:
        """단일 카테고리 블로그."""
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y년 %m월 %d일")
        weekday = ["월", "화", "수", "목", "금", "토", "일"][date.weekday()]
        meta = self.CATEGORY_META.get(category, {"emoji": "📰", "name": category})

        template = f"""# {meta['emoji']} 오늘의 {meta['name']}, 오늘의 흐름 ({date_str} {weekday})

오늘 하루 {meta['name']} 분야에서
흐름이 느껴지는 이슈만 정리했습니다.

---

"""
        template += self._generate_category_content(category, articles)

        # 시리즈 시그니처
        template += "\n---\n\n"

        template += "오늘 다룬 내용,\n"
        template += "당장 와닿지 않을 수도 있다.\n\n"

        template += "근데 이런 게 쌓이면서 흐름이 만들어지고,\n"
        template += "어느 순간 직접 영향 받는 시점이 온다.\n\n"

        template += "---\n\n"
        template += "오늘의 뉴스는 여기까지입니다.\n"
        template += "내일은 또 어떤 흐름이 이어질지,\n"
        template += "기록해두겠습니다.\n\n"

        # 참고 기사
        template += "---\n\n"
        template += "<details>\n<summary>📚 참고 기사</summary>\n\n"
        for art in articles[:10]:
            title = art.get("title", "")
            url = art.get("url", "#")
            source = art.get("source", "")
            template += f"- [{title}]({url}) ({source})\n"
        template += "\n</details>\n\n"

        template += f"*{date.strftime('%Y-%m-%d %H:%M')} 작성*\n"
        return template
