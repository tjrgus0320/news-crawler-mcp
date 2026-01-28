import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { newsApi } from '../api/newsApi';
import { CATEGORY_INFO, type CategoryId } from '../types/news';

export function BlogGenerator() {
  const [selectedCategory, setSelectedCategory] = useState<CategoryId | null>(null);
  const [template, setTemplate] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDigest = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await newsApi.getDailyDigest(selectedCategory || undefined);
      setTemplate(response.template);
    } catch (err) {
      setError('다이제스트를 불러오는데 실패했습니다.');
      setTemplate('');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDigest();
  }, [selectedCategory]);

  const handleCopy = async () => {
    if (!template) return;
    try {
      await navigator.clipboard.writeText(template);
      toast.success('클립보드에 복사되었습니다!');
    } catch {
      toast.error('복사에 실패했습니다.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-secondary-800 mb-2">
          📝 블로그 포스트 생성기
        </h1>
        <p className="text-secondary-500">
          카테고리별 뉴스를 취합하여 블로그에 바로 붙여넣을 수 있는 형태로 생성합니다.
        </p>
      </div>

      {/* Category Filter */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-secondary-700 mb-2">
          카테고리 선택
        </label>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              selectedCategory === null
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-secondary-600 hover:bg-gray-200'
            }`}
          >
            전체 카테고리
          </button>
          {(Object.keys(CATEGORY_INFO) as CategoryId[]).map((catId) => {
            const info = CATEGORY_INFO[catId];
            return (
              <button
                key={catId}
                onClick={() => setSelectedCategory(catId)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  selectedCategory === catId
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-100 text-secondary-600 hover:bg-gray-200'
                }`}
              >
                <span className="mr-1">{info.emoji}</span>
                {info.name}
              </button>
            );
          })}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3 mb-6">
        <button
          onClick={fetchDigest}
          disabled={loading}
          className="btn-secondary disabled:opacity-50"
        >
          🔄 새로고침
        </button>
        <button
          onClick={handleCopy}
          disabled={loading || !template}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          📋 복사하기
        </button>
      </div>

      {/* Preview Area */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
          <span className="text-sm font-medium text-secondary-700">미리보기</span>
          <span className="text-xs text-secondary-400">
            {selectedCategory
              ? CATEGORY_INFO[selectedCategory].name
              : '전체 카테고리'}
          </span>
        </div>
        <div className="p-4 max-h-[60vh] overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
              <span className="ml-3 text-secondary-500">생성 중...</span>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-500">{error}</p>
              <button
                onClick={fetchDigest}
                className="mt-4 text-primary-500 hover:underline"
              >
                다시 시도
              </button>
            </div>
          ) : template ? (
            <pre className="whitespace-pre-wrap text-sm text-secondary-700 font-mono leading-relaxed">
              {template}
            </pre>
          ) : (
            <p className="text-center text-secondary-400 py-12">
              뉴스가 없습니다.
            </p>
          )}
        </div>
      </div>

      {/* Help Text */}
      <p className="mt-4 text-xs text-secondary-400 text-center">
        💡 복사 버튼을 클릭하면 마크다운 형식으로 클립보드에 복사됩니다.
        블로그 에디터에 붙여넣기 하세요.
      </p>
    </div>
  );
}
