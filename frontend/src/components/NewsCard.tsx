import { useState } from 'react';
import { CATEGORY_INFO, type Article } from '../types/news';
import { BlogTemplateModal } from './BlogTemplateModal';

interface NewsCardProps {
  article: Article;
}

export function NewsCard({ article }: NewsCardProps) {
  const [showModal, setShowModal] = useState(false);

  const categoryInfo = CATEGORY_INFO[article.category];

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '';

    // UTC 표시가 없으면 추가
    let str = dateStr;
    if (!str.endsWith('Z') && !str.includes('+')) {
      str += 'Z';
    }

    const date = new Date(str);
    return date.toLocaleDateString('ko-KR', {
      timeZone: 'Asia/Seoul',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <>
      <article className="card p-5 flex flex-col h-full">
        {/* Category badge */}
        <div className="flex items-center justify-between mb-3">
          <span className={`badge ${categoryInfo.color}`}>
            {categoryInfo.emoji} {categoryInfo.name}
          </span>
          <span className="text-xs text-secondary-400">
            {formatDate(article.published_at || article.crawled_at)}
          </span>
        </div>

        {/* Title */}
        <h3 className="text-lg font-semibold text-secondary-800 line-clamp-2 mb-2">
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-primary-500 transition-colors"
          >
            {article.title}
          </a>
        </h3>

        {/* Summary */}
        {article.summary && (
          <p className="text-sm text-secondary-500 line-clamp-3 mb-4 flex-grow">
            {article.summary}
          </p>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-100">
          <span className="text-xs text-secondary-400">
            {article.source || '출처 미상'}
          </span>

          <button
            onClick={() => setShowModal(true)}
            className="btn-secondary text-xs py-1.5 px-3"
          >
            📋 템플릿 복사
          </button>
        </div>
      </article>

      {/* Blog Template Modal */}
      {showModal && (
        <BlogTemplateModal
          articleId={article.id}
          articleTitle={article.title}
          onClose={() => setShowModal(false)}
        />
      )}
    </>
  );
}
