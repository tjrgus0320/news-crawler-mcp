import { useState, useEffect, useCallback } from 'react';
import { newsApi } from '../api/newsApi';
import type { Article, Category, CrawlStatus, CategoryId } from '../types/news';

interface UseNewsOptions {
  category?: CategoryId | null;
  page?: number;
  size?: number;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

export function useNews(options: UseNewsOptions = {}) {
  const {
    category = null,
    page = 1,
    size = 20,
    autoRefresh = false,
    refreshInterval = 300000, // 5 minutes
  } = options;

  const [articles, setArticles] = useState<Article[]>([]);
  const [total, setTotal] = useState(0);
  const [hasNext, setHasNext] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchNews = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await newsApi.getNews({
        category: category || undefined,
        page,
        size,
      });

      setArticles(response.items);
      setTotal(response.total);
      setHasNext(response.has_next);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch news'));
    } finally {
      setLoading(false);
    }
  }, [category, page, size]);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(fetchNews, refreshInterval);
    return () => clearInterval(interval);
  }, [autoRefresh, refreshInterval, fetchNews]);

  return {
    articles,
    total,
    hasNext,
    loading,
    error,
    refetch: fetchNews,
  };
}

export function useCategories() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchCategories = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await newsApi.getCategories();
      setCategories(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch categories'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  return { categories, loading, error, refetch: fetchCategories };
}

export function useCrawlStatus() {
  const [status, setStatus] = useState<CrawlStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchStatus = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await newsApi.getStatus();
      setStatus(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch status'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  return { status, loading, error, refetch: fetchStatus };
}

export function useBlogTemplate(articleId: string | null) {
  const [template, setTemplate] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchTemplate = useCallback(async () => {
    if (!articleId) {
      setTemplate(null);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const data = await newsApi.getBlogTemplate(articleId);
      setTemplate(data.template);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch template'));
    } finally {
      setLoading(false);
    }
  }, [articleId]);

  useEffect(() => {
    fetchTemplate();
  }, [fetchTemplate]);

  return { template, loading, error, refetch: fetchTemplate };
}
