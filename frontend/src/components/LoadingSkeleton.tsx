export function LoadingSkeleton() {
  return (
    <div className="card p-5 animate-pulse">
      {/* Category badge skeleton */}
      <div className="flex items-center justify-between mb-3">
        <div className="h-5 w-16 bg-gray-200 rounded-full" />
        <div className="h-4 w-12 bg-gray-200 rounded" />
      </div>

      {/* Title skeleton */}
      <div className="space-y-2 mb-4">
        <div className="h-5 bg-gray-200 rounded w-full" />
        <div className="h-5 bg-gray-200 rounded w-3/4" />
      </div>

      {/* Summary skeleton */}
      <div className="space-y-2 mb-4">
        <div className="h-4 bg-gray-200 rounded w-full" />
        <div className="h-4 bg-gray-200 rounded w-full" />
        <div className="h-4 bg-gray-200 rounded w-2/3" />
      </div>

      {/* Footer skeleton */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="h-4 w-20 bg-gray-200 rounded" />
        <div className="h-8 w-24 bg-gray-200 rounded-lg" />
      </div>
    </div>
  );
}
