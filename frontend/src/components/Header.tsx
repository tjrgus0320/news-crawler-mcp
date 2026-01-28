import { useState } from 'react';
import toast from 'react-hot-toast';
import { useCrawlStatus } from '../hooks/useNews';
import { newsApi } from '../api/newsApi';

export function Header() {
  const { status, refetch } = useCrawlStatus();
  const [isCrawling, setIsCrawling] = useState(false);

  const handleCrawl = async () => {
    if (isCrawling) return;

    setIsCrawling(true);
    try {
      await newsApi.triggerCrawl({ max_per_category: 30 });
      toast.success('크롤링이 시작되었습니다! 잠시 후 새로고침 해주세요.');

      // 10초 후 상태 갱신
      setTimeout(() => {
        refetch();
        setIsCrawling(false);
      }, 10000);
    } catch (error) {
      toast.error('크롤링 시작에 실패했습니다.');
      setIsCrawling(false);
    }
  };

  const formatLastUpdate = () => {
    if (!status?.last_crawled_at) return '정보 없음';

    // Supabase timestamptz는 ISO 형식으로 오므로 직접 파싱
    let dateStr = status.last_crawled_at;

    // UTC 표시가 없으면 추가 (Supabase는 UTC로 저장)
    if (!dateStr.endsWith('Z') && !dateStr.includes('+')) {
      dateStr += 'Z';
    }

    const date = new Date(dateStr);
    return date.toLocaleString('ko-KR', {
      timeZone: 'Asia/Seoul',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <span className="text-2xl">📰</span>
            <h1 className="text-xl font-bold text-secondary-800">
              뉴스 크롤러
            </h1>
          </div>

          {/* Status */}
          <div className="flex items-center gap-4">
            <div className="text-sm text-secondary-500">
              <span className="hidden sm:inline">마지막 업데이트: </span>
              <span className="font-medium text-secondary-700">
                {formatLastUpdate()}
              </span>
            </div>

            {status && (
              <div className="flex items-center gap-1.5">
                <span
                  className={`w-2 h-2 rounded-full ${
                    status.status === 'success'
                      ? 'bg-accent-500'
                      : status.status === 'running'
                      ? 'bg-yellow-500 animate-pulse'
                      : 'bg-secondary-400'
                  }`}
                />
                <span className="text-xs text-secondary-500 hidden sm:inline">
                  {status.total_articles}개 기사
                </span>
              </div>
            )}

            {/* 크롤링 버튼 */}
            <button
              onClick={handleCrawl}
              disabled={isCrawling}
              className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-colors ${
                isCrawling
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-500 text-white hover:bg-primary-600'
              }`}
              title="뉴스 수동 업데이트"
            >
              {isCrawling ? (
                <span className="flex items-center gap-1.5">
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                    />
                  </svg>
                  <span className="hidden sm:inline">크롤링 중...</span>
                </span>
              ) : (
                <span className="flex items-center gap-1.5">
                  🔄
                  <span className="hidden sm:inline">업데이트</span>
                </span>
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
