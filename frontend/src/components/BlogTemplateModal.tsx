import { useEffect, useRef } from 'react';
import toast from 'react-hot-toast';
import { useBlogTemplate } from '../hooks/useNews';

interface BlogTemplateModalProps {
  articleId: string;
  articleTitle: string;
  onClose: () => void;
}

export function BlogTemplateModal({
  articleId,
  articleTitle,
  onClose,
}: BlogTemplateModalProps) {
  const { template, loading, error } = useBlogTemplate(articleId);
  const modalRef = useRef<HTMLDivElement>(null);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  // Close on outside click
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) onClose();
  };

  const handleCopy = async () => {
    if (!template) return;

    try {
      await navigator.clipboard.writeText(template);
      toast.success('템플릿이 클립보드에 복사되었습니다!');
    } catch {
      toast.error('복사에 실패했습니다.');
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      onClick={handleBackdropClick}
    >
      <div
        ref={modalRef}
        className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[80vh] flex flex-col"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-secondary-800 truncate pr-4">
            📝 {articleTitle}
          </h2>
          <button
            onClick={onClose}
            className="text-secondary-400 hover:text-secondary-600 transition-colors"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500" />
            </div>
          ) : error ? (
            <div className="text-center py-12 text-secondary-500">
              템플릿을 불러오는데 실패했습니다.
            </div>
          ) : (
            <pre className="text-sm text-secondary-700 whitespace-pre-wrap font-mono bg-gray-50 rounded-lg p-4 overflow-x-auto">
              {template}
            </pre>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-200">
          <button onClick={onClose} className="btn-secondary">
            닫기
          </button>
          <button
            onClick={handleCopy}
            disabled={loading || !!error || !template}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            📋 복사하기
          </button>
        </div>
      </div>
    </div>
  );
}
