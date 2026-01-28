import { NewsCard } from './NewsCard';
import { LoadingSkeleton } from './LoadingSkeleton';
import type { Article } from '../types/news';

interface NewsListProps {
  articles: Article[];
  loading: boolean;
  error: Error | null;
}

export function NewsList({ articles, loading, error }: NewsListProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <LoadingSkeleton key={i} />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">😢</div>
        <h3 className="text-xl font-semibold text-secondary-700 mb-2">
          오류가 발생했습니다
        </h3>
        <p className="text-secondary-500">{error.message}</p>
      </div>
    );
  }

  if (articles.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">📭</div>
        <h3 className="text-xl font-semibold text-secondary-700 mb-2">
          뉴스가 없습니다
        </h3>
        <p className="text-secondary-500">
          아직 크롤링된 뉴스가 없거나 선택한 카테고리에 기사가 없습니다.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {articles.map((article) => (
        <NewsCard key={article.id} article={article} />
      ))}
    </div>
  );
}
