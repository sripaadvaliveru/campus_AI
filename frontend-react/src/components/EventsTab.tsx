import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Calendar, Clock, CheckSquare, Square, Filter } from 'lucide-react';
import { Badge, GlassCard, ShimmerButton } from './ui/Primitives';
import { cn } from '../lib/cn';
import type { Event } from '../types';

interface EventsTabProps {
  events: Event[];
  loading: boolean;
}

const CATEGORIES = [
  { id: 'all', label: 'All', color: 'slate' as const },
  { id: 'exam', label: 'Exams', color: 'amber' as const },
  { id: 'cultural', label: 'Cultural', color: 'purple' as const },
  { id: 'sports', label: 'Sports', color: 'green' as const },
  { id: 'holiday', label: 'Holidays', color: 'cyan' as const },
  { id: 'academic', label: 'Academic', color: 'blue' as const },
  { id: 'placement', label: 'Placement', color: 'rose' as const },
];

const CATEGORY_ACCENT: Record<string, string> = {
  exam: 'from-amber-500 to-orange-500',
  cultural: 'from-purple-500 to-pink-500',
  sports: 'from-emerald-500 to-green-500',
  holiday: 'from-cyan-500 to-teal-500',
  academic: 'from-blue-500 to-indigo-500',
  placement: 'from-rose-500 to-red-500',
};

const CATEGORY_COLOR: Record<string, 'amber' | 'purple' | 'green' | 'cyan' | 'blue' | 'rose' | 'slate'> = {
  exam: 'amber', cultural: 'purple', sports: 'green',
  holiday: 'cyan', academic: 'blue', placement: 'rose',
};

export const EventsTab: React.FC<EventsTabProps> = ({ events, loading }) => {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const [semester, setSemester] = useState('all');
  const [upcoming, setUpcoming] = useState(false);

  const today = (() => {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  })();

  const filtered = events.filter(e => {
    const text = e.event.toLowerCase() + (e.description || '').toLowerCase();
    const matchSearch = text.includes(search.toLowerCase());
    const matchCat = category === 'all' || e.category.toLowerCase() === category;
    const matchSem = semester === 'all' ||
      (semester === 'odd' && e.semester.toLowerCase().includes('odd')) ||
      (semester === 'even' && e.semester.toLowerCase().includes('even'));
    const matchUp = !upcoming || e.date >= today;
    return matchSearch && matchCat && matchSem && matchUp;
  });

  return (
    <div className="space-y-6 pb-10">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="font-display text-2xl font-black text-white tracking-tight">Academic Calendar</h1>
        <p className="text-sm text-slate-400">Exams, fests, holidays, and placements — all in one place.</p>
      </div>

      {/* Filter bar */}
      <GlassCard className="p-4 space-y-3" hover={false}>
        <div className="flex gap-3 flex-col sm:flex-row">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-600" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search events…"
              aria-label="Search events"
              className="w-full bg-slate-900/60 text-sm text-white placeholder-slate-600 pl-9 pr-4 py-2.5 rounded-xl border border-white/5 focus:outline-none focus:border-blue-500/30 transition"
            />
          </div>
          <select
            value={semester}
            onChange={e => setSemester(e.target.value)}
            className="bg-slate-900/60 text-sm text-slate-300 px-3 py-2.5 rounded-xl border border-white/5 focus:outline-none focus:border-blue-500/30 transition sm:w-44"
          >
            <option value="all">All Semesters</option>
            <option value="odd">Odd Semester</option>
            <option value="even">Even Semester</option>
          </select>
          <button
            onClick={() => setUpcoming(!upcoming)}
            className={cn(
              'flex items-center gap-2 px-4 py-2.5 rounded-xl border text-sm font-medium transition-all duration-150 flex-shrink-0',
              upcoming
                ? 'bg-blue-500/15 border-blue-500/30 text-blue-400'
                : 'bg-slate-900/60 border-white/5 text-slate-400 hover:text-slate-200'
            )}
          >
            {upcoming ? <CheckSquare className="h-4 w-4" /> : <Square className="h-4 w-4" />}
            Upcoming
          </button>
        </div>

        {/* Category pills */}
        <div className="flex gap-2 flex-wrap">
          {CATEGORIES.map(c => (
            <button
              key={c.id}
              onClick={() => setCategory(c.id)}
              className={cn(
                'px-3 py-1 rounded-full text-2xs font-semibold uppercase tracking-wider border transition-all duration-150',
                category === c.id
                  ? 'bg-blue-500 border-blue-500 text-white'
                  : 'bg-slate-900/60 border-white/5 text-slate-500 hover:text-slate-300 hover:border-white/10'
              )}
            >
              {c.label}
            </button>
          ))}
          <div className="ml-auto flex items-center gap-1.5 text-2xs text-slate-600">
            <Filter className="h-3 w-3" />
            {filtered.length} events
          </div>
        </div>
      </GlassCard>

      {/* Events grid */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20 gap-3">
          <div className="w-8 h-8 rounded-full border-2 border-blue-500 border-t-transparent animate-spin" />
          <span className="text-xs text-slate-500">Loading calendar…</span>
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center gap-4">
          <Calendar className="h-10 w-10 text-slate-700" />
          <div>
            <p className="text-slate-300 font-semibold">No events found</p>
            <p className="text-sm text-slate-500 mt-1">Try adjusting your filters</p>
          </div>
          <ShimmerButton variant="ghost" size="sm" onClick={() => { setSearch(''); setCategory('all'); setUpcoming(false); }}>
            Clear filters
          </ShimmerButton>
        </div>
      ) : (
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 gap-4"
          initial="hidden"
          animate="show"
          variants={{ hidden: {}, show: { transition: { staggerChildren: 0.06 } } }}
        >
          <AnimatePresence>
            {filtered.map((e, i) => {
              const isPast = e.date < today;
              const accent = CATEGORY_ACCENT[e.category.toLowerCase()] || 'from-slate-500 to-slate-600';
              const badgeColor = CATEGORY_COLOR[e.category.toLowerCase()] || 'slate';
              return (
                <motion.div
                  key={i}
                  variants={{
                    hidden: { opacity: 0, y: 16 },
                    show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.16, 1, 0.3, 1] } },
                  }}
                >
                  <GlassCard
                    className={cn('p-5 relative overflow-hidden group', isPast && 'opacity-60')}
                    hover={!isPast}
                    glow={isPast ? false : 'blue'}
                  >
                    {/* Top gradient accent */}
                    <div className={cn('absolute top-0 inset-x-0 h-0.5 bg-gradient-to-r', accent)} />

                    <div className="space-y-3">
                      <div className="flex items-start justify-between gap-3">
                        <Badge variant={badgeColor}>{e.category}</Badge>
                        <span className="text-2xs text-slate-500 bg-slate-900/60 px-2 py-0.5 rounded-full border border-white/5 truncate">
                          {e.semester}
                        </span>
                      </div>

                      <h3 className={cn('font-semibold text-sm text-slate-200 leading-snug line-clamp-2', !isPast && 'group-hover:text-white transition-colors')}>
                        {e.event}
                      </h3>

                      {e.description && (
                        <p className="text-xs text-slate-500 leading-relaxed line-clamp-2">{e.description}</p>
                      )}

                      <div className="flex items-center justify-between pt-1 border-t border-white/5">
                        <div className="flex items-center gap-1.5 text-xs font-medium text-blue-400">
                          <Clock className="h-3 w-3" />
                          {e.date}
                        </div>
                        {isPast ? (
                          <span className="text-2xs text-slate-600 font-medium uppercase tracking-wider">Completed</span>
                        ) : (
                          <span className="text-2xs text-emerald-500 font-semibold uppercase tracking-wider">Upcoming</span>
                        )}
                      </div>
                    </div>
                  </GlassCard>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>
      )}
    </div>
  );
};
