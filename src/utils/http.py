"""HTTP client utilities for crawling."""
import asyncio
import random
from typing import Optional

import httpx


class HttpClient:
    """Async HTTP client with retry and rate limiting."""

    def __init__(
        self,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        timeout: float = 30.0,
        max_retries: int = 3,
        request_delay: float = 1.0,
    ):
        self.user_agent = user_agent
        self.timeout = timeout
        self.max_retries = max_retries
        self.request_delay = request_delay
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "HttpClient":
        self._client = httpx.AsyncClient(
            headers={
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
            },
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get(self, url: str) -> Optional[str]:
        """
        Fetch URL content with retry logic.

        Args:
            url: URL to fetch

        Returns:
            HTML content as string, or None if failed
        """
        if not self._client:
            raise RuntimeError("HttpClient must be used as async context manager")

        for attempt in range(self.max_retries):
            try:
                # Add random delay to avoid detection
                if attempt > 0:
                    delay = self.request_delay * (1 + random.uniform(0, 0.5))
                    await asyncio.sleep(delay)

                response = await self._client.get(url)
                response.raise_for_status()
                return response.text

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Too Many Requests
                    wait_time = (attempt + 1) * 5
                    await asyncio.sleep(wait_time)
                elif e.response.status_code >= 500:
                    await asyncio.sleep(self.request_delay)
                else:
                    return None

            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.request_delay * (attempt + 1))
                continue

            except Exception:
                return None

        return None

    async def get_with_delay(self, url: str) -> Optional[str]:
        """Fetch URL with delay before request."""
        delay = self.request_delay * (1 + random.uniform(0, 0.3))
        await asyncio.sleep(delay)
        return await self.get(url)
