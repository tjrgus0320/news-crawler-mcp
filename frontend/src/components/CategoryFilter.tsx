import { useCategories } from '../hooks/useNews';
import { CATEGORY_INFO, type CategoryId } from '../types/news';

interface CategoryFilterProps {
  selected: CategoryId | null;
  onSelect: (category: CategoryId | null) => void;
}

export function CategoryFilter({ selected, onSelect }: CategoryFilterProps) {
  const { categories } = useCategories();

  const allCount = categories.reduce((sum, cat) => sum + cat.count, 0);

  return (
    <div className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="flex gap-1 py-3 overflow-x-auto scrollbar-hide">
          {/* All categories button */}
          <button
            onClick={() => onSelect(null)}
            className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              selected === null
                ? 'bg-primary-500 text-white'
                : 'bg-gray-100 text-secondary-600 hover:bg-gray-200'
            }`}
          >
            전체
            <span className="ml-1.5 text-xs opacity-75">({allCount})</span>
          </button>

          {/* Category buttons */}
          {(Object.keys(CATEGORY_INFO) as CategoryId[]).map((catId) => {
            const info = CATEGORY_INFO[catId];
            const catData = categories.find((c) => c.id === catId);
            const count = catData?.count || 0;

            return (
              <button
                key={catId}
                onClick={() => onSelect(catId)}
                className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  selected === catId
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-100 text-secondary-600 hover:bg-gray-200'
                }`}
              >
                <span className="mr-1">{info.emoji}</span>
                {info.name}
                <span className="ml-1.5 text-xs opacity-75">({count})</span>
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
