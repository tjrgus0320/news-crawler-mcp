"""APScheduler configuration for news crawling."""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..config.settings import settings
from ..service.news_service import NewsService

logger = logging.getLogger(__name__)

# Create scheduler instance
scheduler = AsyncIOScheduler(timezone=settings.timezone)


async def scheduled_crawl():
    """Scheduled task to crawl all news categories."""
    logger.info("Starting scheduled news crawl...")

    try:
        service = NewsService()
        results = await service.crawl_all_categories(
            max_per_category=settings.max_articles_per_category
        )

        total = sum(results.values())
        logger.info(f"Scheduled crawl completed: {total} articles collected")

    except Exception as e:
        logger.error(f"Scheduled crawl failed: {e}")


def start_scheduler():
    """Start the scheduler with configured jobs."""
    if not settings.scheduler_enabled:
        logger.info("Scheduler is disabled")
        return

    # Add daily crawl job
    scheduler.add_job(
        scheduled_crawl,
        CronTrigger(
            hour=settings.crawl_hour,
            minute=settings.crawl_minute,
            timezone=settings.timezone,
        ),
        id="daily_news_crawl",
        replace_existing=True,
        name="Daily News Crawl",
    )

    scheduler.start()
    logger.info(
        f"Scheduler started. Next crawl at {settings.crawl_hour:02d}:{settings.crawl_minute:02d} {settings.timezone}"
    )


def shutdown_scheduler():
    """Shutdown the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler shutdown complete")
