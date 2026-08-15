import React from 'react';
import { TrendingUp, MessageSquare, Clock, Award, Zap, Activity } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AnimatedCounter, Card, ProgressBar, Badge, Skeleton, BlueprintStat } from './ui/Primitives';
import { DoodleData } from './ui/doodles/DoodleData';
import { cn } from '../lib/cn';
import type { AnalyticsData } from '../types';

interface AnalyticsTabProps {
  analyticsData: AnalyticsData | null;
  loading: boolean;
  modelName: string;
}

const AnalyticsSkeleton = () => (
  <div className="space-y-6 pb-10">
    <div className="space-y-1">
      <Skeleton className="h-7 w-48" />
      <Skeleton className="h-3 w-64" />
    </div>
    <div className="grid grid-cols-2 xl:grid-cols-4 gap-3">
      {Array.from({ length: 4 }).map((_, i) => (
        <Card key={i} className="p-4" hover={false}>
          <div className="space-y-2">
            <Skeleton className="h-3 w-20" />
            <Skeleton className="h-7 w-16" />
            <Skeleton className="h-3 w-24" />
          </div>
        </Card>
      ))}
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
      <Card className="lg:col-span-8 p-5" hover={false}>
        <Skeleton className="h-4 w-40 mb-3" />
        <Skeleton className="h-32 w-full" />
      </Card>
      <Card className="lg:col-span-4 p-5" hover={false}>
        <Skeleton className="h-4 w-32 mb-3" />
        <Skeleton className="h-3 w-full mb-2" count={4} />
      </Card>
    </div>
  </div>
);

export const AnalyticsTab: React.FC<AnalyticsTabProps> = ({ analyticsData, loading, modelName }) => {
  if (loading || !analyticsData) {
    return <AnalyticsSkeleton />;
  }

  const { summary, popular_queries, recent_queries } = analyticsData;

  const chartData = (summary.daily_counts || []).map(d => ({
    name: d.day.slice(5),
    count: d.count,
  }));

  const KPI_CARDS = [
    {
      label: 'Total Queries',
      value: summary.total_queries,
      sub: `${summary.today_queries} today`,
      icon: MessageSquare,
      bg: 'bg-amber-50',
      iconColor: 'text-amber-700',
    },
    {
      label: 'Satisfaction',
      value: summary.satisfaction_rate,
      suffix: '%',
      sub: `${summary.positive_feedback} 👍 / ${summary.negative_feedback} 👎`,
      icon: Award,
      bg: 'bg-olive-50',
      iconColor: 'text-olive-700',
    },
    {
      label: 'Avg Response',
      value: summary.avg_response_time_ms,
      suffix: 'ms',
      sub: modelName,
      icon: Clock,
      bg: 'bg-amber-50',
      iconColor: 'text-amber-600',
    },
    {
      label: 'RAG Vectors',
      value: 1250,
      suffix: '+',
      sub: 'FAISS Index',
      icon: Zap,
      bg: 'bg-orange-50',
      iconColor: 'text-orange-700',
    },
  ];

  return (
    <div className="space-y-6 pb-10 relative">
      <DoodleData />
      <div className="relative z-10">
        <h1 className="font-display text-xl font-semibold gradient-text bg-gradient-to-r from-amber-700 to-amber-800 tracking-tight">Analytics</h1>
        <p className="text-xs text-stone-500 mt-0.5">Usage metrics from the SQLite analytics engine.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-3">
        {KPI_CARDS.map((card, i) => {
          const Icon = card.icon;
          return (
            <Card key={i} className="p-4 bg-[#F3ECE1]/50" hover={false}>
              <div className="flex items-center justify-between mb-2">
                <p className="text-xs text-stone-500">{card.label}</p>
                <div className={cn('p-1.5 rounded-md', card.bg)}>
                  <Icon className={cn('h-3.5 w-3.5', card.iconColor)} />
                </div>
              </div>
              <div className={cn('text-xl font-bold', card.iconColor)}>
                <AnimatedCounter to={card.value} suffix={card.suffix || ''} duration={1500} decimals={card.suffix === '%' ? 1 : 0} />
              </div>
              <p className="text-2xs text-stone-400 mt-0.5 font-mono">{card.sub}</p>
            </Card>
          );
        })}
      </div>

      {/* Chart + Categories */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <Card className="lg:col-span-8 p-5" hover={false}>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="h-4 w-4 text-amber-700" />
            <h2 className="font-medium text-sm text-stone-800">Query Volume — Last 7 Days</h2>
            <Badge variant="amber" className="ml-auto">Live</Badge>
          </div>
          {chartData.length === 0 ? (
            <p className="text-xs text-stone-500 text-center py-10">No data yet.</p>
          ) : (
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#D97706" stopOpacity={0.15}/>
                    <stop offset="95%" stopColor="#D97706" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#E8E2D5" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#B8A99A' }} />
                <YAxis tick={{ fontSize: 11, fill: '#B8A99A' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#FFFDF9',
                    border: '1px solid #E8E2D5',
                    borderRadius: '0.5rem',
                    boxShadow: '0 1px 3px rgba(180, 83, 9, 0.08)',
                    fontSize: '12px',
                  }}
                />
                <Area type="monotone" dataKey="count" stroke="#D97706" strokeWidth={1.5} fillOpacity={1} fill="url(#colorCount)" />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </Card>

        <Card className="lg:col-span-4 p-5" hover={false}>
          <div className="flex items-center gap-2 mb-4">
            <Activity className="h-4 w-4 text-amber-700" />
            <h2 className="font-medium text-sm text-stone-800">Top Categories</h2>
          </div>
          {summary.top_categories.length === 0 ? (
            <p className="text-xs text-stone-500 text-center py-8">No queries yet.</p>
          ) : (
            <div className="space-y-3">
              {summary.top_categories.map((c, i) => {
                const colors = [
                  'from-amber-500 to-amber-600',
                  'from-orange-500 to-orange-600',
                  'from-olive-500 to-olive-600',
                  'from-amber-600 to-amber-700',
                  'from-rose-500 to-rose-600',
                ];
                return (
                  <ProgressBar
                    key={i}
                    label={c.category}
                    value={c.count}
                    max={summary.total_queries || 1}
                    color={colors[i % colors.length]}
                  />
                );
              })}
            </div>
          )}
        </Card>
      </div>

      {/* Popular + Recent */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <Card className="lg:col-span-4 p-5" hover={false}>
          <h2 className="font-medium text-sm text-stone-800 mb-3">Popular Queries</h2>
          <div className="divide-y divide-[#E8E2D5]">
            {popular_queries.length === 0
              ? <p className="text-xs text-stone-500 py-6 text-center">No data.</p>
              : popular_queries.map((q, i) => (
                <div key={i} className="py-2 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="text-2xs font-medium text-stone-400 w-4 flex-shrink-0">{i + 1}</span>
                    <span className="text-xs text-stone-600 truncate">"{q.user_query}"</span>
                  </div>
                  <Badge variant="slate">{q.frequency}×</Badge>
                </div>
              ))}
          </div>
        </Card>

        <Card className="lg:col-span-8 p-5" hover={false}>
          <h2 className="font-medium text-sm text-stone-800 mb-3">Recent Queries</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-[#E8E2D5] text-stone-500 text-2xs">
                  <th className="text-left pb-2 pr-4 font-medium">Query</th>
                  <th className="text-left pb-2 pr-4 font-medium">Category</th>
                  <th className="text-right pb-2 font-medium">Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E8E2D5]">
                {recent_queries.length === 0
                  ? <tr><td colSpan={3} className="py-6 text-center text-stone-500">No logs yet.</td></tr>
                  : recent_queries.map(q => (
                    <tr key={q.id} className="hover:bg-[#F3ECE1]/50 transition-colors">
                      <td className="py-2 pr-4 text-stone-600 truncate max-w-[240px]" title={q.user_query}>
                        "{q.user_query}"
                      </td>
                      <td className="py-2 pr-4">
                        <Badge variant="slate" className="capitalize">{q.category || 'general'}</Badge>
                      </td>
                      <td className="py-2 text-right text-stone-500">
                        {q.timestamp ? new Date(q.timestamp).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'}
                        <span className="block text-2xs text-stone-400">{q.response_time_ms}ms</span>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  );
};
