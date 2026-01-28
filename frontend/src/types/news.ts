export type CategoryId = 'politics' | 'economy' | 'society' | 'life' | 'world' | 'it';

export interface Article {
  id: string;
  title: string;
  url: string;
  summary: string | null;
  content: string | null;
  category: CategoryId;
  source: string | null;
  author: string | null;
  image_url: string | null;
  published_at: string | null;
  crawled_at: string;
  created_at: string;
}

export interface ArticleListResponse {
  items: Article[];
  total: number;
  page: number;
  size: number;
  has_next: boolean;
}

export interface Category {
  id: CategoryId;
  name: string;
  count: number;
}

export interface CrawlStatus {
  last_crawled_at: string | null;
  total_articles: number;
  status: string;
  next_crawl_at: string | null;
}

export interface BlogTemplate {
  article_id: string;
  template: string;
}

export const CATEGORY_INFO: Record<CategoryId, { name: string; emoji: string; color: string }> = {
  politics: { name: '정치', emoji: '🏛️', color: 'badge-politics' },
  economy: { name: '경제', emoji: '💰', color: 'badge-economy' },
  society: { name: '사회', emoji: '👥', color: 'badge-society' },
  life: { name: '생활/문화', emoji: '🌸', color: 'badge-life' },
  world: { name: '세계', emoji: '🌍', color: 'badge-world' },
  it: { name: 'IT/과학', emoji: '💻', color: 'badge-it' },
};
