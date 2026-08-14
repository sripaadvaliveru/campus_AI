import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Calendar, Clock, CheckSquare, Square, Filter } from 'lucide-react';
import { Badge, Card, ShimmerButton, Skeleton } from './ui/Primitives';
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

const EventSkeleton = () => (
  <Card className="p-5" hover={false}>
    <div className="space-y-3">
      <div className="flex items-start justify-between gap-3">
        <Skeleton className="h-5 w-16 rounded-full" />
        <Skeleton className="h-4 w-24 rounded-full" />
      </div>
      <Skeleton className="h-5 w-3/4" />
      <Skeleton className="h-4 w-full" count={2} />
      <div className="flex items-center justify-between pt-1 border-t border-slate-100">
        <Skeleton className="h-4 w-20" />
        <Skeleton className="h-4 w-16" />
      </div>
    </div>
  </Card>
);

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
        <h1 className="font-display text-2xl font-black text-slate-900 tracking-tight">Academic Calendar</h1>
        <p className="text-sm text-slate-500">Exams, fests, holidays, and placements — all in one place.</p>
      </div>

      {/* Filter bar */}
      <Card className="p-4 space-y-3" hover={false}>
        <div className="flex gap-3 flex-col sm:flex-row">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search events…"
              aria-label="Search events"
              className="w-full bg-slate-50 text-sm text-slate-900 placeholder-slate-400 pl-9 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-blue focus:border-transparent transition"
            />
          </div>
          <select
            value={dept}
            onChange={e => setDept(e.target.value)}
            className="bg-slate-50 text-sm text-slate-700 px-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-blue focus:border-transparent transition sm:w-56 appearance-none cursor-pointer"
            style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")`, backgroundPosition: 'right 0.5rem center', backgroundRepeat: 'no-repeat', backgroundSize: '1.5em 1.5em', paddingRight: '2.5rem' }}
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
                ? 'bg-blue-50 border-blue-200 text-brand-blue'
                : 'bg-slate-50 border-slate-200 text-slate-600 hover:text-slate-900 hover:border-slate-300'
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
                  ? 'bg-brand-blue border-brand-blue text-white'
                  : 'bg-white border-slate-200 text-slate-500 hover:text-slate-700 hover:border-slate-300'
              )}
            >
              {c.label}
            </button>
          ))}
          <div className="ml-auto flex items-center gap-1.5 text-2xs text-slate-400">
            <Filter className="h-3 w-3" />
            {filtered.length} events
          </div>
        </div>
      </Card>

      {/* Events grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <EventSkeleton key={i} />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center gap-4">
          <Calendar className="h-10 w-10 text-slate-300" />
          <div>
            <p className="text-slate-700 font-semibold">No events found</p>
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
                  <Card
                    className={cn('p-5 relative overflow-hidden group', isPast && 'opacity-60')}
                    hover={!isPast}
                  >
                    {/* Top gradient accent */}
                    <div className={cn('absolute top-0 inset-x-0 h-0.5 bg-gradient-to-r', accent)} />

                    <div className="space-y-3">
                      <div className="flex items-start justify-between gap-3">
                        <Badge variant={badgeColor}>{e.category}</Badge>
                        <span className="text-2xs text-slate-500 bg-slate-50 px-2 py-0.5 rounded-full border border-slate-200 truncate">
                          {e.semester}
                        </span>
                      </div>

                      <h3 className={cn('font-semibold text-sm text-slate-900 leading-snug line-clamp-2', !isPast && 'group-hover:text-brand-blue transition-colors')}>
                        {e.event}
                      </h3>

                      {e.description && (
                        <p className="text-xs text-slate-500 leading-relaxed line-clamp-2">{e.description}</p>
                      )}

                      <div className="flex items-center justify-between pt-1 border-t border-slate-100">
                        <div className="flex items-center gap-1.5 text-xs font-medium text-brand-blue">
                          <Clock className="h-3 w-3" />
                          {e.date}
                        </div>
                        {isPast ? (
                          <span className="text-2xs text-slate-400 font-medium uppercase tracking-wider">Completed</span>
                        ) : (
                          <span className="text-2xs text-emerald-600 font-semibold uppercase tracking-wider">Upcoming</span>
                        )}
                      </div>
                    </div>
                  </Card>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>
      )}
    </div>
  );
};
