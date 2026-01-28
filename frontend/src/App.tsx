import { useState } from 'react';
import { Header, CategoryFilter, NewsList, BlogGenerator } from './components';
import { useNews } from './hooks/useNews';
import type { CategoryId } from './types/news';

type PageView = 'news' | 'blog-generator';

function App() {
  const [currentView, setCurrentView] = useState<PageView>('news');
  const [selectedCategory, setSelectedCategory] = useState<CategoryId | null>(null);
  const [page, setPage] = useState(1);

  const { articles, loading, error, total, hasNext } = useNews({
    category: selectedCategory,
    page,
    size: 21, // 3열 * 7행
  });

  const handleCategoryChange = (category: CategoryId | null) => {
    setSelectedCategory(category);
    setPage(1); // Reset to first page
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />

      {/* Tab Navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex gap-8">
            <button
              onClick={() => setCurrentView('news')}
              className={`py-4 text-sm font-medium border-b-2 transition-colors ${
                currentView === 'news'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-secondary-500 hover:text-secondary-700 hover:border-gray-300'
              }`}
            >
              📰 뉴스 피드
            </button>
            <button
              onClick={() => setCurrentView('blog-generator')}
              className={`py-4 text-sm font-medium border-b-2 transition-colors ${
                currentView === 'blog-generator'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-secondary-500 hover:text-secondary-700 hover:border-gray-300'
              }`}
            >
              📝 블로그 생성기
            </button>
          </nav>
        </div>
      </div>

      {/* Page Content */}
      {currentView === 'news' ? (
        <>
          {/* Category Filter */}
          <CategoryFilter selected={selectedCategory} onSelect={handleCategoryChange} />

          {/* Main Content */}
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Results count */}
            <div className="flex items-center justify-between mb-6">
              <p className="text-sm text-secondary-500">
                {loading ? (
                  '로딩 중...'
                ) : (
                  <>
                    총 <span className="font-semibold text-secondary-700">{total}</span>개의
                    기사
                  </>
                )}
              </p>
            </div>

            {/* News List */}
            <NewsList articles={articles} loading={loading} error={error} />

            {/* Pagination */}
            {!loading && !error && total > 0 && (
              <div className="flex items-center justify-center gap-4 mt-8">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  ← 이전
                </button>

                <span className="text-sm text-secondary-600">
                  {page} 페이지
                </span>

                <button
                  onClick={() => setPage((p) => p + 1)}
                  disabled={!hasNext}
                  className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  다음 →
                </button>
              </div>
            )}
          </main>
        </>
      ) : (
        <main className="py-8">
          <BlogGenerator />
        </main>
      )}

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-secondary-400">
            © 2026 News Crawler. Built with FastAPI & React.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
