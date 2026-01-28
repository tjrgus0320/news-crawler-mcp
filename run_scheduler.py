"""
스케줄러용 뉴스 크롤링 스크립트
매일 실행하여 오늘의 뉴스를 마크다운 파일로 저장합니다.
"""
import asyncio
import sys
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(Path(__file__).parent))

from src.crawlers.naver import NaverNewsCrawler
from src.formatters.blog import BlogFormatter
from src.models.article import Category, DailyDigest
from src.utils.http import HttpClient


async def crawl_and_save():
    """전체 카테고리 뉴스를 크롤링하고 파일로 저장"""
    print(f"[{datetime.now()}] 뉴스 크롤링 시작...")

    # 크롤링
    async with HttpClient() as http:
        crawler = NaverNewsCrawler(http)
        articles_by_category = await crawler.crawl_all_categories(
            categories=list(Category),
            max_per_category=30,  # 카테고리당 30개
            include_content=False,
        )

    # DailyDigest 생성
    digest = DailyDigest()
    for cat_str, articles in articles_by_category.items():
        for article in articles:
            digest.add_article(article)

    print(f"총 {digest.total_count}개 기사 수집 완료")

    # 마크다운 포맷팅
    output_dir = Path(__file__).parent / "output"
    formatter = BlogFormatter(output_dir=output_dir)
    content = formatter.format_daily_digest(digest)

    # 파일 저장
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-daily-news.md"
    filepath = formatter.save_to_file(content, filename)

    print(f"파일 저장 완료: {filepath}")
    return filepath


def main():
    """메인 함수"""
    try:
        filepath = asyncio.run(crawl_and_save())
        print(f"\n[완료] 크롤링 성공!")
        print(f"[저장] {filepath}")
    except Exception as e:
        print(f"\n[오류] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
