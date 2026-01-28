"""Vercel Serverless Function entry point for FastAPI."""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from backend
from backend.app.api.news_router import router as news_router

app = FastAPI(
    title="뉴스 크롤러 API",
    description="네이버 뉴스 크롤링 및 블로그 템플릿 생성 API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(news_router)


@app.get("/")
async def root():
    return {"message": "뉴스 크롤러 API", "docs": "/docs"}


# Vercel handler
handler = app
