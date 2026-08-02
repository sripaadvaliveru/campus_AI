export type TabId = 'dashboard' | 'chat' | 'events' | 'directory' | 'analytics';

export interface College {
  id: string;
  name: string;
  short: string;
  icon: string;
  type: string;
  location: string;
  color: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  toolUsed?: string;
  responseTimeMs?: number;
}

export type EventCategory =
  | 'exam'
  | 'cultural'
  | 'sports'
  | 'holiday'
  | 'academic'
  | 'placement'
  | 'orientation'
  | 'technical'
  | 'social';

export interface Event {
  date: string;
  event: string;
  category: EventCategory | string;
  semester: string;
  description?: string;
}

export interface Contact {
  name: string;
  designation: string;
  department: string;
  email: string;
  phone: string;
  specialization?: string;
  cabin?: string;
}

export interface CategoryCount {
  category: string;
  count: number;
}

export interface DailyCount {
  day: string;
  count: number;
}

export interface AnalyticsSummary {
  total_queries: number;
  today_queries: number;
  positive_feedback: number;
  negative_feedback: number;
  satisfaction_rate: number;
  top_categories: CategoryCount[];
  daily_counts: DailyCount[];
  avg_response_time_ms: number;
}

export interface PopularQuery {
  user_query: string;
  frequency: number;
}

export interface RecentQuery {
  id: number;
  user_query: string;
  bot_response: string;
  category: string;
  timestamp: string;
  response_time_ms: number;
}

export interface AnalyticsData {
  summary: AnalyticsSummary;
  popular_queries: PopularQuery[];
  recent_queries: RecentQuery[];
  timestamp: string;
}
