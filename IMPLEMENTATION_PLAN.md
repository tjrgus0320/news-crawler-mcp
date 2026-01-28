# 뉴스 크롤링 웹 애플리케이션 구현 계획서

## 개요

기존 `news-crawler-mcp` 프로젝트를 확장하여 FastAPI 백엔드 + React 프론트엔드 웹 애플리케이션 구축

---

## 1. 프로젝트 구조 (확장)

```
news-crawler-mcp/
├── src/                          # 기존 MCP 서버 (유지)
│   ├── crawlers/naver.py         # ✅ 재사용
│   ├── formatters/blog.py        # ✅ 재사용
│   ├── models/article.py         # ✅ 재사용 + 확장
│   ├── utils/http.py             # ✅ 재사용
│   └── server.py                 # ✅ 유지 (MCP 서버)
│
├── backend/                      # 🆕 FastAPI 백엔드
│   ├── main.py                   # FastAPI 앱 엔트리포인트
│   ├── requirements.txt
│   ├── .env
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── news_router.py    # REST API 엔드포인트
│   │   ├── service/
│   │   │   ├── __init__.py
│   │   │   ├── news_service.py   # 크롤링 + 비즈니스 로직
│   │   │   └── template_service.py
│   │   ├── repository/
│   │   │   ├── __init__.py
│   │   │   └── news_repository.py  # Supabase CRUD
│   │   ├── schema/
│   │   │   ├── __init__.py
│   │   │   └── news_schema.py    # Pydantic 스키마
│   │   ├── scheduler/
│   │   │   ├── __init__.py
│   │   │   └── news_scheduler.py # APScheduler
│   │   └── config/
│   │       ├── __init__.py
│   │       ├── settings.py       # 환경변수 설정
│   │       └── supabase.py       # Supabase 클라이언트
│   └── alembic/                  # (선택) DB 마이그레이션
│
├── frontend/                     # 🆕 React 프론트엔드
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── components/
│       │   ├── Header.tsx
│       │   ├── NewsList.tsx
│       │   ├── NewsCard.tsx
│       │   ├── CategoryFilter.tsx
│       │   ├── BlogTemplateModal.tsx
│       │   ├── LoadingSkeleton.tsx
│       │   └── Toast.tsx
│       ├── hooks/
│       │   └── useNews.ts
│       ├── types/
│       │   └── news.ts
│       ├── api/
│       │   └── newsApi.ts
│       └── styles/
│           └── index.css
│
├── output/                       # 크롤링 결과 저장
├── run_scheduler.py              # 기존 스케줄러 (유지)
└── README.md                     # 업데이트
```

---

## 2. 데이터베이스 설계 (Supabase)

### 테이블: `news_articles`

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `id` | uuid | PK, 자동생성 |
| `title` | text | 기사 제목 |
| `url` | text | 기사 URL (unique) |
| `summary` | text | 요약 (300자) |
| `content` | text | 본문 (nullable) |
| `category` | text | 카테고리 (politics, economy, ...) |
| `source` | text | 출처 (언론사) |
| `author` | text | 기자명 |
| `image_url` | text | 이미지 URL (nullable) |
| `published_at` | timestamptz | 발행일 |
| `crawled_at` | timestamptz | 크롤링 시간 |
| `created_at` | timestamptz | 생성일 (default: now()) |

### 테이블: `crawl_logs`

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `id` | uuid | PK |
| `started_at` | timestamptz | 크롤링 시작 시간 |
| `finished_at` | timestamptz | 크롤링 완료 시간 |
| `total_articles` | int | 수집된 기사 수 |
| `status` | text | success / failed |
| `error_message` | text | 에러 메시지 (nullable) |

### Supabase SQL

```sql
-- 뉴스 테이블
CREATE TABLE news_articles (
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

-- 인덱스
CREATE INDEX idx_news_category ON news_articles(category);
CREATE INDEX idx_news_crawled_at ON news_articles(crawled_at DESC);
CREATE INDEX idx_news_published_at ON news_articles(published_at DESC);

-- 크롤링 로그 테이블
CREATE TABLE crawl_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    total_articles INT DEFAULT 0,
    status TEXT DEFAULT 'running',
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS 정책 (읽기 전용 공개)
ALTER TABLE news_articles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON news_articles FOR SELECT USING (true);

ALTER TABLE crawl_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON crawl_logs FOR SELECT USING (true);
```

---

## 3. Backend 구현 상세

### Phase 1: 기본 설정

1. **backend/requirements.txt**
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
supabase>=2.3.0
python-dotenv>=1.0.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
apscheduler>=3.10.0
httpx>=0.27.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
```

2. **backend/.env**
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-anon-key
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
SCHEDULER_ENABLED=true
CRAWL_HOUR=9
CRAWL_MINUTE=0
TIMEZONE=Asia/Seoul
```

### Phase 2: API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/news` | 뉴스 목록 (페이지네이션, 필터) |
| GET | `/api/news/{id}` | 뉴스 상세 |
| GET | `/api/news/{id}/template` | 블로그 템플릿 |
| GET | `/api/categories` | 카테고리 목록 |
| GET | `/api/status` | 마지막 크롤링 상태 |
| POST | `/api/news/crawl` | 수동 크롤링 실행 |

### Phase 3: 서비스 로직

**news_service.py**:
- 기존 `NaverNewsCrawler` import하여 재사용
- 크롤링 결과를 Supabase에 저장
- 중복 체크 (URL 기준 upsert)

**template_service.py**:
- 기존 `BlogFormatter` 재사용
- 단일 기사 → 블로그 템플릿 변환

### Phase 4: 스케줄러

**APScheduler 설정**:
```python
scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
scheduler.add_job(
    crawl_all_news,
    CronTrigger(hour=9, minute=0),
    id="daily_news_crawl",
    replace_existing=True
)
```

---

## 4. Frontend 구현 상세

### Phase 1: 프로젝트 설정

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install axios react-hot-toast
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Phase 2: 컴포넌트 구조

```
App.tsx
├── Header.tsx              # 로고 + 마지막 업데이트 시간
├── CategoryFilter.tsx      # 카테고리 탭 (가로 스크롤)
├── NewsList.tsx            # 뉴스 카드 그리드
│   └── NewsCard.tsx        # 개별 뉴스 카드
│       └── BlogTemplateModal.tsx  # 템플릿 모달
└── LoadingSkeleton.tsx     # 로딩 상태
```

### Phase 3: 디자인 시스템

**색상 (Tailwind)**:
```js
// tailwind.config.js
colors: {
  primary: '#2563EB',
  secondary: '#64748B',
  accent: '#10B981',
}
```

**반응형**:
- Mobile: 1열 (< 640px)
- Tablet: 2열 (640-1024px)
- Desktop: 3열 (> 1024px)

### Phase 4: 주요 기능

1. **카테고리 필터링**: 탭 클릭 → API 재호출
2. **무한 스크롤 또는 페이지네이션**: 대량 기사 처리
3. **템플릿 복사**: 클립보드 복사 + 토스트 알림
4. **자동 새로고침**: 5분마다 상태 확인

---

## 5. 구현 순서

### Step 1: Backend 기초 (1단계)
- [ ] `backend/` 폴더 구조 생성
- [ ] `settings.py` 환경변수 설정
- [ ] `supabase.py` 클라이언트 연결
- [ ] Supabase 테이블 생성 (SQL 실행)

### Step 2: Backend API (2단계)
- [ ] `news_schema.py` Pydantic 스키마
- [ ] `news_repository.py` Supabase CRUD
- [ ] `news_service.py` 크롤링 + 저장 로직
- [ ] `news_router.py` API 엔드포인트
- [ ] `main.py` FastAPI 앱 설정

### Step 3: Backend 스케줄러 (3단계)
- [ ] `news_scheduler.py` APScheduler 설정
- [ ] 스케줄러 FastAPI lifespan 통합

### Step 4: Frontend 기초 (4단계)
- [ ] Vite + React + TypeScript 설정
- [ ] Tailwind CSS 설정
- [ ] API 클라이언트 (`newsApi.ts`)
- [ ] 타입 정의 (`news.ts`)

### Step 5: Frontend 컴포넌트 (5단계)
- [ ] `Header.tsx`
- [ ] `CategoryFilter.tsx`
- [ ] `NewsCard.tsx`
- [ ] `NewsList.tsx`
- [ ] `BlogTemplateModal.tsx`
- [ ] `LoadingSkeleton.tsx`

### Step 6: 통합 및 테스트 (6단계)
- [ ] CORS 설정 확인
- [ ] 수동 크롤링 테스트
- [ ] 스케줄러 테스트
- [ ] 프론트엔드 ↔ 백엔드 통합 테스트

---

## 6. 실행 방법 (완료 후)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### 접속
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 7. 예상 파일 수

| 영역 | 파일 수 |
|------|---------|
| Backend | ~15개 |
| Frontend | ~12개 |
| 설정 파일 | ~5개 |
| **총계** | **~32개** |

---

## 8. 주의사항

1. **Supabase 키 보안**: `.env`는 `.gitignore`에 추가
2. **CORS 설정**: 개발/프로덕션 환경 분리
3. **Rate Limiting**: 크롤링 시 1초 딜레이 유지
4. **에러 핸들링**: 모든 API에 try-catch 적용
5. **기존 코드 유지**: `src/` 폴더는 수정 최소화

---

이 계획대로 진행할까요?
