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

    # 기사 선별 신호 키워드 (구조/방향성 판단)
    SIGNAL_KEYWORDS = [
        "전망", "가능성", "논의", "확대", "전환",
        "우려", "변화", "가속", "장기", "영향",
        "추진", "검토", "계획", "본격", "착수",
    ]

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

    # Short Day 문구 (뉴스 한산한 날)
    SHORT_DAY_PHRASES = [
        "오늘은 상대적으로 조용한 하루였다.",
        "큰 이슈 없이 지나간 날은, 되려 준비하는 날이다.",
        "오늘 같은 날은 어제와 내일 사이를 연결하는 시간이다.",
    ]

    def score_article(self, article: Dict[str, Any]) -> int:
        """기사 점수 산정 - 좋은 기사 선별 로직.

        점수 기준:
        - 제목 길이 (20-60자) → +2
        - 신호 키워드 포함 → +1 per keyword
        - 요약 존재 및 충분한 길이 → +2
        - 자극적 표현 → -2
        """
        score = 0
        title = article.get("title", "")
        summary = article.get("summary", "")

        # 1. 제목 길이 (너무 짧으면 정보 부족, 너무 길면 낚시성)
        if 20 <= len(title) <= 60:
            score += 2
        elif len(title) > 60:
            score -= 1  # 너무 긴 제목 감점

        # 2. 키워드 신호 (구조/방향성 있는 기사)
        score += sum(1 for k in self.SIGNAL_KEYWORDS if k in title)

        # 3. 요약 존재 및 품질
        if summary and len(summary) > 50:
            score += 2
        elif summary and len(summary) > 20:
            score += 1

        # 4. 자극적 표현 감점
        if "!" in title:
            score -= 2
        if "단독" in title:
            score -= 1
        if "속보" in title:
            score -= 1
        if "충격" in title or "경악" in title:
            score -= 2

        # 5. 숫자/데이터 포함 가점 (구체적 정보)
        if any(c.isdigit() for c in title):
            score += 1

        return score

    def select_main_article(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """점수 기반 메인 기사 선택."""
        if not articles:
            return {}

        scored = [(self.score_article(a), a) for a in articles]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    def select_top_articles(
        self, articles: List[Dict[str, Any]], count: int = 3
    ) -> List[Dict[str, Any]]:
        """점수 기반 상위 기사 선택."""
        if not articles:
            return []

        scored = [(self.score_article(a), a) for a in articles]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [a for _, a in scored[:count]]

    def is_short_day(self, articles: List[Dict[str, Any]], threshold: int = 3) -> bool:
        """뉴스 한산한 날 판단.

        기준: 전체 기사 수가 threshold 이하이거나,
        상위 기사 점수가 낮으면 Short Day로 판단.
        """
        if len(articles) <= threshold:
            return True

        # 최고 점수가 2점 이하면 한산한 날
        if articles:
            top_score = max(self.score_article(a) for a in articles)
            if top_score <= 2:
                return True

        return False

    def _generate_short_day_content(self, category: str) -> str:
        """Short Day 콘텐츠 생성."""
        lines = []
        meta = self.CATEGORY_META.get(category, {"name": category})

        lines.append(random.choice(self.SHORT_DAY_PHRASES))
        lines.append("")
        lines.append(f"오늘 {meta['name']} 분야에서는")
        lines.append("눈에 띄는 변화나 이슈가 없었다.")
        lines.append("")
        lines.append("이럴 때 굳이 뭔가 의미를 만들어내는 건")
        lines.append("오히려 노이즈가 된다.")
        lines.append("")
        lines.append("조용한 날은 조용한 대로 기록해두고,")
        lines.append("**다음 움직임이 어디서 나올지** 지켜보는 게 낫다.")
        lines.append("")

        return "\n".join(lines)

    def generate_template(self, article: Dict[str, Any]) -> str:
        """단일 기사 블로그 템플릿 - 분석형 콘텐츠 생성."""
        title = article.get("title", "제목 없음")
        source = article.get("source", "")
        url = article.get("url", "#")
        summary = article.get("summary", "")
        category = article.get("category", "general")

        meta = self.CATEGORY_META.get(category, {"emoji": "📰", "name": "뉴스"})
        date = datetime.now()
        date_str = date.strftime("%Y년 %m월 %d일")

        lines = []

        # 헤더
        lines.append(f"# {meta['emoji']} {title}")
        lines.append("")
        lines.append(f"> {date_str} | {source}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 팩트 요약
        lines.append("## 📌 핵심 내용")
        lines.append("")
        if summary:
            lines.append(summary)
        else:
            lines.append(f"[{source}]({url})에서 보도한 내용입니다.")
        lines.append("")

        # 카테고리별 분석 코멘트
        lines.append("## 💡 왜 주목해야 하나")
        lines.append("")
        lines.append(self._get_single_article_analysis(category))
        lines.append("")

        # 생각 포인트
        lines.append("## 🤔 생각해볼 점")
        lines.append("")
        lines.append(self._get_thinking_points(category))
        lines.append("")

        # 애매한 문장 추가 (AI 티 제거)
        lines.append(random.choice(self.UNCERTAIN_PHRASES))
        lines.append("")

        # 출처
        lines.append("---")
        lines.append("")
        lines.append(f"**원문**: [{title}]({url}) ({source})")
        lines.append("")
        lines.append(f"*{date.strftime('%Y-%m-%d %H:%M')} 작성*")

        return "\n".join(lines)

    def _get_single_article_analysis(self, category: str) -> str:
        """카테고리별 단일 기사 분석 코멘트."""
        analysis = {
            "economy": [
                "경제 뉴스에서 중요한 건 숫자 자체가 아니라, **시장이 이걸 어떻게 받아들이느냐**다.",
                "단기 반응에 휘둘리기보다, 이 흐름이 어디로 향하는지 방향을 읽는 게 낫다.",
                "당장 체감하긴 어려워도, 몇 달 뒤 생활비나 금리로 돌아올 수 있는 신호다.",
            ],
            "politics": [
                "정치 뉴스의 특징은, 지금은 말뿐인 것 같아도 몇 달 뒤 정책으로 슬쩍 돌아온다는 점이다.",
                "발언 자체보다 **'결국 어디로 가려는 건지'** 방향을 읽어두는 게 중요하다.",
                "당장 큰 변화는 없어 보여도, 이런 신호가 쌓이면 흐름이 바뀌는 시점이 온다.",
            ],
            "it": [
                "기술 뉴스를 볼 때 항상 던지는 질문이 있다. **\"왜 하필 지금 이게 나왔을까?\"**",
                "발표 타이밍에는 이유가 있다. 경쟁사 움직임, 시장 상황, 내부 로드맵.",
                "개발자나 IT 업계 종사자라면, 이게 **내 업무에 어떤 영향 주는지** 생각해볼 타이밍이다.",
            ],
            "society": [
                "개별 사건으로 보면 안 된다. 비슷한 뉴스가 반복된다는 건 **구조적으로 뭔가 막혀 있다**는 신호.",
                "당장 내 일 아닌 것 같아도, 결국 생활비나 정책으로 연결되는 경우가 많다.",
                "사회 이슈는 '왜 지금 이게 터졌나'를 보면 흐름이 읽힌다.",
            ],
            "world": [
                "남의 나라 일 같지만, **환율, 수출, 공급망**으로 연결되면 우리 일이 된다.",
                "글로벌 뉴스는 교양으로 보는 게 아니라 실무적으로 체크하는 게 맞다.",
                "지정학적 변화는 느리게 오지만, 한 번 오면 오래 간다.",
            ],
            "life": [
                "트렌드는 결국 소비 패턴과 연결된다. **사람들이 어디에 돈을 쓰려 하는지** 읽는 게 포인트.",
                "문화 뉴스는 가볍게 보이지만, 시대의 분위기를 반영하는 경우가 많다.",
                "생활 트렌드 변화는 새로운 기회가 될 수도 있다.",
            ],
        }

        category_lines = analysis.get(category, [
            "이 뉴스가 의미하는 바를 한 번 짚어볼 필요가 있다.",
            "표면적인 내용 너머에 어떤 흐름이 있는지 생각해보자.",
        ])

        return random.choice(category_lines)

    def _get_thinking_points(self, category: str) -> str:
        """카테고리별 생각 포인트."""
        points = {
            "economy": "- 이 흐름이 계속되면 내 자산/소비에 어떤 영향이 있을까?\n- 관련 업종이나 기업은 어디일까?",
            "politics": "- 이 발언/정책이 실현되면 누가 영향을 받을까?\n- 비슷한 사례가 과거에 있었나?",
            "it": "- 이 기술/서비스가 내 업무에 적용될 여지가 있을까?\n- 경쟁 서비스나 대안은 뭐가 있을까?",
            "society": "- 이 문제의 근본 원인은 뭘까?\n- 개인적으로 대비하거나 준비할 게 있을까?",
            "world": "- 국내에는 어떤 영향이 있을까?\n- 관련 산업이나 기업은 어디일까?",
            "life": "- 이 트렌드가 내 생활에 적용될 부분이 있을까?\n- 관련된 새로운 기회가 있을까?",
        }

        return points.get(category, "- 이 뉴스가 나에게 의미하는 바는?\n- 앞으로 어떤 변화가 있을까?")

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
        """카테고리별 콘텐츠 - AI 티 제거 + 스코어링 적용."""
        if not articles:
            return "오늘은 특별한 이슈 없었습니다.\n"

        # Short Day 체크
        if self.is_short_day(articles, threshold=2):
            return self._generate_short_day_content(category)

        # 점수 기반 정렬
        sorted_articles = self.select_top_articles(articles, count=5)

        if category == "economy":
            return self._content_economy(sorted_articles)
        elif category == "politics":
            return self._content_politics(sorted_articles)
        elif category == "it":
            return self._content_tech(sorted_articles)
        elif category == "society":
            return self._content_society(sorted_articles)
        elif category == "world":
            return self._content_world(sorted_articles)
        else:
            return self._content_general(sorted_articles)

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
