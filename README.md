# News Crawler MCP Server

뉴스 기사를 크롤링하여 블로그 포스팅용 마크다운을 자동 생성하는 MCP 서버입니다.

## 주요 기능

- **카테고리별 뉴스 크롤링**: 정치, 경제, 사회, 생활/문화, 세계, IT/과학
- **블로그 포맷 출력**: 복사하여 바로 사용 가능한 마크다운 형식
- **일일 뉴스 다이제스트**: 모든 카테고리의 주요 뉴스 한번에 수집
- **자동 스케줄링**: Windows Task Scheduler로 매일 자동 실행

## 빠른 시작

### 1. 저장소 클론

```bash
git clone <repository-url>
cd news-crawler-mcp
```

### 2. 가상환경 생성 및 의존성 설치

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 테스트 실행

```bash
python run_scheduler.py
```

실행 후 `output/` 폴더에 마크다운 파일이 생성됩니다.

## Claude Desktop 연동

`%APPDATA%\Claude\claude_desktop_config.json` (Windows) 또는 `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) 파일에 추가:

```json
{
  "mcpServers": {
    "news-crawler": {
      "command": "절대경로/venv/Scripts/python.exe",
      "args": ["-m", "src.server"],
      "cwd": "절대경로/news-crawler-mcp"
    }
  }
}
```

> **Windows 경로 예시**: `D:\\repository\\news-crawler-mcp`

## Claude Code 연동

프로젝트 폴더에서 Claude Code 실행 시 `mcp.json`이 자동 인식됩니다.

## 사용 가능한 MCP Tools

| Tool | 설명 | 주요 매개변수 |
|------|------|---------------|
| `list_categories` | 카테고리 목록 조회 | - |
| `crawl_news_by_category` | 특정 카테고리 크롤링 | `category`, `max_articles` |
| `crawl_daily_news` | 전체 카테고리 일일 뉴스 | `categories`, `max_per_category` |
| `get_article_detail` | 기사 상세 조회 | `url` |
| `save_to_file` | 마크다운 파일 저장 | `content`, `filename` |

### 카테고리 ID

| ID | 이름 |
|----|------|
| `politics` | 정치 |
| `economy` | 경제 |
| `society` | 사회 |
| `life` | 생활/문화 |
| `world` | 세계 |
| `it` | IT/과학 |

## 프롬프트 예시

```
"오늘의 IT 뉴스 5개 크롤링해서 블로그용으로 정리해줘"

"경제 카테고리 주요 기사 요약해줘"

"오늘 하루 뉴스 전체 카테고리별로 정리해줘"
```

## 자동 스케줄링 (Windows)

매일 정해진 시간에 자동으로 뉴스를 크롤링하고 파일로 저장합니다.

### Task Scheduler 등록

관리자 권한 PowerShell에서 실행:

```powershell
# 매일 오전 9시 실행
schtasks /create /tn "NewsCrawler" /tr "경로\run_crawler.bat" /sc daily /st 09:00 /f
```

### 시간 변경

```powershell
schtasks /change /tn "NewsCrawler" /st 18:00
```

### 등록 확인

```powershell
schtasks /query /tn "NewsCrawler"
```

### 삭제

```powershell
schtasks /delete /tn "NewsCrawler" /f
```

## 프로젝트 구조

```
news-crawler-mcp/
├── src/
│   ├── server.py           # MCP 서버 메인
│   ├── crawlers/
│   │   └── naver.py        # 네이버 뉴스 크롤러
│   ├── models/
│   │   └── article.py      # Article, Category 데이터 모델
│   ├── formatters/
│   │   └── blog.py         # 마크다운 블로그 포맷터
│   └── utils/
│       └── http.py         # 비동기 HTTP 클라이언트
├── config/
│   └── settings.yaml       # 크롤링 설정
├── output/                  # 생성된 마크다운 저장
├── run_scheduler.py         # 스케줄러 실행 스크립트
├── run_crawler.bat          # Windows 배치 파일
├── mcp.json                 # Claude Code 설정
├── requirements.txt
└── pyproject.toml
```

## 의존성

- Python 3.10+
- mcp >= 1.0.0
- httpx >= 0.27.0
- beautifulsoup4 >= 4.12.0
- lxml >= 5.0.0
- pydantic >= 2.0.0
- pyyaml >= 6.0.0

## 출력 예시

```markdown
# [2025.01.27] 오늘의 뉴스 모음

오늘의 주요 뉴스를 카테고리별로 정리했습니다.

---

## IT/과학

### 1. 삼성전자, 갤럭시 S25 시리즈 공개

> 출처: [원문](https://news.naver.com/...)

### 2. AI 스타트업 투자 급증

> 출처: [원문](https://news.naver.com/...)

---

*총 30개의 기사가 수집되었습니다.*
```

---

## 🌐 웹 애플리케이션

뉴스 크롤링 결과를 웹에서 조회하고 블로그 템플릿을 생성할 수 있는 웹 애플리케이션입니다.

### 기술 스택

- **Backend**: FastAPI, Supabase, APScheduler
- **Frontend**: React 18, TypeScript, Tailwind CSS, Vite

### 사전 요구사항

1. **Supabase 프로젝트 생성**: [supabase.com](https://supabase.com)에서 무료 프로젝트 생성
2. **테이블 생성**: `backend/supabase_schema.sql` 실행

### Backend 실행

```bash
cd backend

# 가상환경 생성
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
copy .env.example .env
# .env 파일에 Supabase URL과 Key 입력

# 서버 실행
uvicorn main:app --reload --port 8000
```

### Frontend 실행

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 접속

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

### API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/news` | 뉴스 목록 (페이지네이션, 필터) |
| GET | `/api/news/{id}` | 뉴스 상세 |
| GET | `/api/news/{id}/template` | 블로그 템플릿 |
| GET | `/api/categories` | 카테고리 목록 |
| GET | `/api/status` | 마지막 크롤링 상태 |
| POST | `/api/news/crawl` | 수동 크롤링 실행 |

### 스케줄러

APScheduler가 매일 오전 9시에 자동으로 모든 카테고리의 뉴스를 크롤링합니다.

```
# .env에서 설정 변경 가능
SCHEDULER_ENABLED=true
CRAWL_HOUR=9
CRAWL_MINUTE=0
```

---

## 라이선스

MIT License
