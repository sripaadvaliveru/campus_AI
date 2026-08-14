import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, MessageSquare, Clock, Award, Zap, Activity } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AnimatedCounter, Card, ProgressBar, ScrollReveal, Badge, Skeleton } from './ui/Primitives';
import { cn } from '../lib/cn';
import type { AnalyticsData } from '../types';

interface AnalyticsTabProps {
  analyticsData: AnalyticsData | null;
  loading: boolean;
  modelName: string;
}

const AnalyticsSkeleton = () => (
  <div className="space-y-8 pb-10">
    <div className="space-y-1">
      <Skeleton className="h-8 w-48" />
      <Skeleton className="h-4 w-64" />
    </div>
    <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <Card key={i} className="p-5" hover={false}>
          <div className="space-y-3">
            <Skeleton className="h-3 w-20" />
            <Skeleton className="h-8 w-16" />
            <Skeleton className="h-3 w-24" />
          </div>
        </Card>
      ))}
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <Card className="lg:col-span-8 p-6" hover={false}>
        <Skeleton className="h-5 w-40 mb-4" />
        <Skeleton className="h-36 w-full" />
      </Card>
      <Card className="lg:col-span-4 p-6" hover={false}>
        <Skeleton className="h-5 w-32 mb-4" />
        <Skeleton className="h-4 w-full mb-3" count={4} />
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
      bg: 'bg-blue-50',
      iconColor: 'text-brand-blue',
    },
    {
      label: 'Satisfaction',
      value: summary.satisfaction_rate,
      suffix: '%',
      sub: `${summary.positive_feedback} 👍 / ${summary.negative_feedback} 👎`,
      icon: Award,
      bg: 'bg-emerald-50',
      iconColor: 'text-emerald-600',
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
      bg: 'bg-purple-50',
      iconColor: 'text-purple-600',
    },
  ];

  return (
    <div className="space-y-8 pb-10">
      <div>
        <h1 className="font-display text-2xl font-black text-slate-900 tracking-tight">Analytics Dashboard</h1>
        <p className="text-sm text-slate-500">Real-time usage metrics from the SQLite analytics engine.</p>
      </div>

      {/* KPI Cards */}
      <motion.div
        className="grid grid-cols-2 xl:grid-cols-4 gap-4"
        initial="hidden"
        animate="show"
        variants={{ hidden: {}, show: { transition: { staggerChildren: 0.08 } } }}
      >
        {KPI_CARDS.map((card, i) => {
          const Icon = card.icon;
          return (
            <motion.div
              key={i}
              variants={{
                hidden: { opacity: 0, y: 20 },
                show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
              }}
            >
              <Card className="p-5" hover={false}>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <p className="text-2xs uppercase tracking-wider font-semibold text-slate-500">{card.label}</p>
                    <div className={cn('p-2 rounded-lg', card.bg)}>
                      <Icon className={cn('h-4 w-4', card.iconColor)} />
                    </div>
                  </div>
                  <div className={cn('text-2xl font-black', card.iconColor)}>
                    <AnimatedCounter to={card.value} suffix={card.suffix || ''} duration={1500} decimals={card.suffix === '%' ? 1 : 0} />
                  </div>
                  <p className="text-2xs text-slate-500">{card.sub}</p>
                </div>
              </Card>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Chart + Categories */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <ScrollReveal className="lg:col-span-8">
          <Card className="p-6 space-y-4" hover={false}>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-brand-blue" />
              <h2 className="font-semibold text-sm text-slate-900">Query Volume — Last 7 Days</h2>
              <Badge variant="blue" className="ml-auto">Live</Badge>
            </div>
            {chartData.length === 0 ? (
              <p className="text-xs text-slate-500 text-center py-12">No data yet.</p>
            ) : (
              <ResponsiveContainer width="100%" height={200}>
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#2563EB" stopOpacity={0.2}/>
                      <stop offset="95%" stopColor="#2563EB" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E4E7F0" />
                  <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#6B7280' }} />
                  <YAxis tick={{ fontSize: 12, fill: '#6B7280' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '1px solid #E4E7F0',
                      borderRadius: '0.5rem',
                      boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
                    }}
                  />
                  <Area type="monotone" dataKey="count" stroke="#2563EB" strokeWidth={2} fillOpacity={1} fill="url(#colorCount)" />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </Card>
        </ScrollReveal>

        <ScrollReveal className="lg:col-span-4" delay={100}>
          <Card className="p-6 space-y-5 h-full" hover={false}>
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-purple-600" />
              <h2 className="font-semibold text-sm text-slate-900">Top Categories</h2>
            </div>
            {summary.top_categories.length === 0 ? (
              <p className="text-xs text-slate-500 text-center py-8">No queries yet.</p>
            ) : (
              <div className="space-y-4">
                {summary.top_categories.map((c, i) => {
                  const colors = [
                    'from-blue-500 to-indigo-500',
                    'from-purple-500 to-pink-500',
                    'from-amber-500 to-orange-500',
                    'from-emerald-500 to-teal-500',
                    'from-rose-500 to-red-500',
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
        </ScrollReveal>
      </div>

      {/* Popular + Recent */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <ScrollReveal className="lg:col-span-4" delay={50}>
          <Card className="p-6 space-y-4" hover={false}>
            <h2 className="font-semibold text-sm text-slate-900">Popular Queries</h2>
            <div className="divide-y divide-slate-100">
              {popular_queries.length === 0
                ? <p className="text-xs text-slate-500 py-6 text-center">No data.</p>
                : popular_queries.map((q, i) => (
                  <div key={i} className="py-2.5 flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2.5 min-w-0">
                      <span className="text-2xs font-bold text-slate-400 w-4 flex-shrink-0">{i + 1}</span>
                      <span className="text-xs text-slate-700 truncate">"{q.user_query}"</span>
                    </div>
                    <Badge variant="slate">{q.frequency}×</Badge>
                  </div>
                ))}
            </div>
          </Card>
        </ScrollReveal>

        <ScrollReveal className="lg:col-span-8" delay={100}>
          <Card className="p-6 space-y-4" hover={false}>
            <h2 className="font-semibold text-sm text-slate-900">Recent Queries</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 uppercase tracking-wider text-2xs">
                    <th className="text-left pb-2 pr-4 font-semibold">Query</th>
                    <th className="text-left pb-2 pr-4 font-semibold">Category</th>
                    <th className="text-right pb-2 font-semibold">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {recent_queries.length === 0
                    ? <tr><td colSpan={3} className="py-8 text-center text-slate-500">No logs yet.</td></tr>
                    : recent_queries.map(q => (
                      <tr key={q.id} className="group hover:bg-slate-50 transition-colors">
                        <td className="py-2.5 pr-4 text-slate-700 truncate max-w-[240px]" title={q.user_query}>
                          "{q.user_query}"
                        </td>
                        <td className="py-2.5 pr-4">
                          <Badge variant="slate" className="capitalize">{q.category || 'general'}</Badge>
                        </td>
                        <td className="py-2.5 text-right font-medium text-slate-500">
                          {q.timestamp ? new Date(q.timestamp).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'}
                          <span className="block text-2xs text-slate-400">{q.response_time_ms}ms</span>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </Card>
        </ScrollReveal>
      </div>
    </div>
  );
};
