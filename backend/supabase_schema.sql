-- =============================================
-- News Crawler Supabase Schema
-- =============================================

-- 뉴스 기사 테이블
CREATE TABLE IF NOT EXISTS news_articles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    summary TEXT,
    content TEXT,
    category TEXT NOT NULL,
    source TEXT,
    author TEXT,
    image_url TEXT,
    published_at TIMESTAMPTZ,
    crawled_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_news_category ON news_articles(category);
CREATE INDEX IF NOT EXISTS idx_news_crawled_at ON news_articles(crawled_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_published_at ON news_articles(published_at DESC);

-- 크롤링 로그 테이블
CREATE TABLE IF NOT EXISTS crawl_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    total_articles INT DEFAULT 0,
    status TEXT DEFAULT 'running',
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS (Row Level Security) 정책
-- 뉴스 테이블: 읽기 전용 공개
ALTER TABLE news_articles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public read access" ON news_articles;
CREATE POLICY "Public read access" ON news_articles
    FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Service write access" ON news_articles;
CREATE POLICY "Service write access" ON news_articles
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- 크롤링 로그 테이블: 읽기 전용 공개
ALTER TABLE crawl_logs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public read access" ON crawl_logs;
CREATE POLICY "Public read access" ON crawl_logs
    FOR SELECT
    USING (true);

DROP POLICY IF EXISTS "Service write access" ON crawl_logs;
CREATE POLICY "Service write access" ON crawl_logs
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- =============================================
-- 테스트용 샘플 데이터 (선택사항)
-- =============================================
/*
INSERT INTO news_articles (title, url, summary, category, source, published_at) VALUES
('테스트 정치 뉴스', 'https://example.com/politics/1', '정치 관련 테스트 뉴스입니다.', 'politics', '테스트 언론사', NOW()),
('테스트 경제 뉴스', 'https://example.com/economy/1', '경제 관련 테스트 뉴스입니다.', 'economy', '테스트 언론사', NOW()),
('테스트 IT 뉴스', 'https://example.com/it/1', 'IT 관련 테스트 뉴스입니다.', 'it', '테스트 언론사', NOW());
*/
