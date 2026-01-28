import { useCrawlStatus } from '../hooks/useNews';

export function Header() {
  const { status } = useCrawlStatus();

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
          </div>
        </div>
      </div>
    </header>
  );
}
