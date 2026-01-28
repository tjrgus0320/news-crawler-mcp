import axios from 'axios';
import type { ArticleListResponse, Article, Category, CrawlStatus, BlogTemplate } from '../types/news';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const newsApi = {
  /**
   * Get news articles with optional filtering
   */
  async getNews(params?: {
    category?: string;
    page?: number;
    size?: number;
  }): Promise<ArticleListResponse> {
    const { data } = await api.get<ArticleListResponse>('/news', { params });
    return data;
  },

  /**
   * Get a single article by ID
   */
  async getArticle(id: string): Promise<Article> {
    const { data } = await api.get<Article>(`/news/${id}`);
    return data;
  },

  /**
   * Get blog template for an article
   */
  async getBlogTemplate(id: string): Promise<BlogTemplate> {
    const { data } = await api.get<BlogTemplate>(`/news/${id}/template`);
    return data;
  },

  /**
   * Get all categories with counts
   */
  async getCategories(): Promise<Category[]> {
    const { data } = await api.get<Category[]>('/categories');
    return data;
  },

  /**
   * Get crawl status
   */
  async getStatus(): Promise<CrawlStatus> {
    const { data } = await api.get<CrawlStatus>('/status');
    return data;
  },

  /**
   * Trigger manual crawl
   */
  async triggerCrawl(params?: {
    categories?: string[];
    max_per_category?: number;
  }): Promise<{ message: string }> {
    const { data } = await api.post('/news/crawl', null, { params });
    return data;
  },
};
