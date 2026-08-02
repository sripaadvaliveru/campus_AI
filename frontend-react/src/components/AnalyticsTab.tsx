import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, MessageSquare, Clock, Award, Zap, Activity } from 'lucide-react';
import { AnimatedCounter, GlassCard, ProgressBar, ScrollReveal, Badge } from './ui/Primitives';
import { GlowingOrb } from './ui/Primitives';
import { cn } from '../lib/cn';
import type { AnalyticsData } from '../types';

interface AnalyticsTabProps {
  analyticsData: AnalyticsData | null;
  loading: boolean;
}

export const AnalyticsTab: React.FC<AnalyticsTabProps> = ({ analyticsData, loading }) => {
  if (loading || !analyticsData) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-3">
        <div className="w-10 h-10 rounded-full border-2 border-blue-500 border-t-transparent animate-spin" />
        <span className="text-sm text-slate-500">Loading analytics data…</span>
      </div>
    );
  }

  const { summary, popular_queries, recent_queries } = analyticsData;

  const KPI_CARDS = [
    {
      label: 'Total Queries',
      value: summary.total_queries,
      sub: `${summary.today_queries} today`,
      icon: MessageSquare,
      gradient: 'from-blue-500/15 to-indigo-500/10',
      border: 'border-blue-500/15',
      iconColor: 'text-blue-400',
      glow: '#3b82f6',
    },
    {
      label: 'Satisfaction',
      value: summary.satisfaction_rate,
      suffix: '%',
      sub: `${summary.positive_feedback} 👍 / ${summary.negative_feedback} 👎`,
      icon: Award,
      gradient: 'from-emerald-500/15 to-green-500/10',
      border: 'border-emerald-500/15',
      iconColor: 'text-emerald-400',
      glow: '#10b981',
    },
    {
      label: 'Avg Response',
      value: summary.avg_response_time_ms,
      suffix: 'ms',
      sub: 'GPT-4o mini',
      icon: Clock,
      gradient: 'from-amber-500/15 to-orange-500/10',
      border: 'border-amber-500/15',
      iconColor: 'text-amber-400',
      glow: '#f59e0b',
    },
    {
      label: 'RAG Vectors',
      value: 1250,
      suffix: '+',
      sub: 'FAISS Index',
      icon: Zap,
      gradient: 'from-purple-500/15 to-pink-500/10',
      border: 'border-purple-500/15',
      iconColor: 'text-purple-400',
      glow: '#8b5cf6',
    },
  ];

  const renderLineChart = () => {
    const data = summary.daily_counts || [];
    if (!data.length) return <p className="text-xs text-slate-500 text-center py-12">No data yet.</p>;

    const max = Math.max(...data.map(d => d.count), 1);
    const W = 500, H = 140, PX = 30, PY = 20;

    const pts = data.map((d, i) => ({
      x: PX + (i * (W - PX * 2)) / Math.max(data.length - 1, 1),
      y: H - PY - ((d.count / max) * (H - PY * 2)),
      count: d.count,
      day: d.day.slice(5),
    }));

    const line = pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
    const area = pts.length > 0
      ? `${line} L ${pts[pts.length - 1].x} ${H - PY} L ${pts[0].x} ${H - PY} Z`
      : '';

    return (
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-36" role="img" aria-label="Query volume line chart for the last 7 days">
        <defs>
          <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.35" />
            <stop offset="100%" stopColor="#3b82f6" stopOpacity="0" />
          </linearGradient>
          <filter id="glow-line">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>
        {/* Grid */}
        {[0.25, 0.5, 0.75].map(r => (
          <line key={r} x1={PX} y1={PY + r * (H - PY * 2)} x2={W - PX} y2={PY + r * (H - PY * 2)}
            stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
        ))}
        {/* Area */}
        <path d={area} fill="url(#areaGrad)" />
        {/* Line */}
        <path d={line} fill="none" stroke="#3b82f6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" filter="url(#glow-line)" />
        {/* Nodes */}
        {pts.map((p, i) => (
          <g key={i}>
            <circle cx={p.x} cy={p.y} r="5" fill="#0f172a" stroke="#3b82f6" strokeWidth="2.5" />
            <circle cx={p.x} cy={p.y} r="2" fill="#3b82f6" />
            {/* Labels */}
            <text x={p.x} y={H - 5} textAnchor="middle" fill="#475569" fontSize="9" fontWeight="600">{p.day}</text>
          </g>
        ))}
      </svg>
    );
  };

  return (
    <div className="space-y-8 pb-10 relative">
      <GlowingOrb color="#6366f1" size={400} intensity={0.05} className="top-20 right-0" />

      <div>
        <h1 className="font-display text-2xl font-black text-white tracking-tight">Analytics Dashboard</h1>
        <p className="text-sm text-slate-400">Real-time usage metrics from the SQLite analytics engine.</p>
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
              <GlassCard
                className={cn('p-5 border relative overflow-hidden', card.border)}
                hover={false}
              >
                <div className={cn('absolute inset-0 bg-gradient-to-br opacity-60', card.gradient)} />
                <div className="relative z-10 space-y-3">
                  <div className="flex items-center justify-between">
                    <p className="text-2xs uppercase tracking-wider font-semibold text-slate-500">{card.label}</p>
                    <Icon className={cn('h-4 w-4', card.iconColor)} />
                  </div>
                  <div className={cn('text-2xl font-black', card.iconColor)}>
                    <AnimatedCounter to={card.value} suffix={card.suffix || ''} duration={1500} decimals={card.suffix === '%' ? 1 : 0} />
                  </div>
                  <p className="text-2xs text-slate-500">{card.sub}</p>
                </div>
              </GlassCard>
            </motion.div>
          );
        })}
      </motion.div>

      {/* Chart + Categories */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <ScrollReveal className="lg:col-span-8">
          <GlassCard className="p-6 space-y-4" hover={false}>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-blue-400" />
              <h2 className="font-semibold text-sm text-white">Query Volume — Last 7 Days</h2>
              <Badge variant="blue" className="ml-auto">Live</Badge>
            </div>
            {renderLineChart()}
          </GlassCard>
        </ScrollReveal>

        <ScrollReveal className="lg:col-span-4" delay={100}>
          <GlassCard className="p-6 space-y-5 h-full" hover={false}>
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-purple-400" />
              <h2 className="font-semibold text-sm text-white">Top Categories</h2>
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
          </GlassCard>
        </ScrollReveal>
      </div>

      {/* Popular + Recent */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <ScrollReveal className="lg:col-span-4" delay={50}>
          <GlassCard className="p-6 space-y-4" hover={false}>
            <h2 className="font-semibold text-sm text-white">Popular Queries</h2>
            <div className="divide-y divide-white/5">
              {popular_queries.length === 0
                ? <p className="text-xs text-slate-500 py-6 text-center">No data.</p>
                : popular_queries.map((q, i) => (
                  <div key={i} className="py-2.5 flex items-center justify-between gap-3">
                    <div className="flex items-center gap-2.5 min-w-0">
                      <span className="text-2xs font-bold text-slate-700 w-4 flex-shrink-0">{i + 1}</span>
                      <span className="text-xs text-slate-300 truncate">"{q.user_query}"</span>
                    </div>
                    <Badge variant="slate">{q.frequency}×</Badge>
                  </div>
                ))}
            </div>
          </GlassCard>
        </ScrollReveal>

        <ScrollReveal className="lg:col-span-8" delay={100}>
          <GlassCard className="p-6 space-y-4" hover={false}>
            <h2 className="font-semibold text-sm text-white">Recent Queries</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-white/5 text-slate-500 uppercase tracking-wider text-2xs">
                    <th className="text-left pb-2 pr-4 font-semibold">Query</th>
                    <th className="text-left pb-2 pr-4 font-semibold">Category</th>
                    <th className="text-right pb-2 font-semibold">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {recent_queries.length === 0
                    ? <tr><td colSpan={3} className="py-8 text-center text-slate-500">No logs yet.</td></tr>
                    : recent_queries.map(q => (
                      <tr key={q.id} className="group hover:bg-white/2 transition-colors">
                        <td className="py-2.5 pr-4 text-slate-300 truncate max-w-[240px]" title={q.user_query}>
                          "{q.user_query}"
                        </td>
                        <td className="py-2.5 pr-4">
                          <Badge variant="slate" className="capitalize">{q.category || 'general'}</Badge>
                        </td>
                        <td className="py-2.5 text-right font-medium text-slate-500">
                          {q.timestamp ? new Date(q.timestamp).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'}
                          <span className="block text-2xs text-slate-600">{q.response_time_ms}ms</span>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </GlassCard>
        </ScrollReveal>
      </div>
    </div>
  );
};
