import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Calendar, Clock, CheckSquare, Square, Filter } from 'lucide-react';
import { Badge, Card, ShimmerButton, Skeleton, BlueprintStat } from './ui/Primitives';
import { DoodleCalendar } from './ui/doodles/DoodleCalendar';
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
  cultural: 'from-orange-400 to-orange-500',
  sports: 'from-olive-400 to-olive-500',
  holiday: 'from-amber-400 to-amber-500',
  academic: 'from-amber-600 to-amber-700',
  placement: 'from-rose-400 to-rose-500',
};

const CATEGORY_COLOR: Record<string, 'amber' | 'purple' | 'green' | 'cyan' | 'blue' | 'rose' | 'slate'> = {
  exam: 'amber', cultural: 'purple', sports: 'green',
  holiday: 'cyan', academic: 'blue', placement: 'rose',
};

const EventSkeleton = () => (
  <Card className="p-4" hover={false}>
    <div className="space-y-2.5">
      <div className="flex items-start justify-between gap-3">
        <Skeleton className="h-5 w-16 rounded-full" />
        <Skeleton className="h-4 w-24 rounded-full" />
      </div>
      <Skeleton className="h-5 w-3/4" />
      <Skeleton className="h-4 w-full" count={2} />
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
    <div className="space-y-5 pb-10 relative">
      <DoodleCalendar />
      {/* Header */}
      <div className="relative z-10">
        <h1 className="font-display text-xl font-semibold gradient-text bg-gradient-to-r from-amber-700 to-amber-800 tracking-tight">Academic Calendar</h1>
        <p className="text-xs text-stone-500 mt-0.5">Exams, fests, holidays, and placements.</p>
      </div>

      {/* Filter bar */}
      <div className="space-y-3">
        <div className="flex gap-2 flex-col sm:flex-row">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-stone-400" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search events…"
              aria-label="Search events"
              className="w-full bg-[#FFFDF9] text-sm text-stone-700 placeholder-stone-400 pl-9 pr-3 py-2 rounded-lg border border-[#E3D9C6] focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500/20 transition"
            />
          </div>
          <select
            value={semester}
            onChange={e => setSemester(e.target.value)}
            className="bg-[#FFFDF9] text-sm text-stone-700 px-3 py-2 rounded-lg border border-[#E3D9C6] focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500/20 transition sm:w-44 appearance-none cursor-pointer"
            style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2378716C' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")`, backgroundPosition: 'right 0.5rem center', backgroundRepeat: 'no-repeat', backgroundSize: '1.5em 1.5em', paddingRight: '2.5rem' }}
          >
            <option value="all">All Semesters</option>
            <option value="odd">Odd Semester</option>
            <option value="even">Even Semester</option>
          </select>
          <button
            onClick={() => setUpcoming(!upcoming)}
            className={cn(
              'flex items-center gap-2 px-3 py-2 rounded-lg border text-sm font-medium transition-colors duration-150 flex-shrink-0',
              upcoming
                ? 'bg-amber-50 border-amber-200 text-amber-800'
                : 'bg-[#FFFDF9] border-[#E3D9C6] text-stone-500 hover:text-stone-700 hover:border-[#D6CFC2]'
            )}
          >
            {upcoming ? <CheckSquare className="h-4 w-4" /> : <Square className="h-4 w-4" />}
            Upcoming
          </button>
        </div>

        {/* Category pills */}
        <div className="flex gap-1.5 flex-wrap items-center">
          {CATEGORIES.map(c => (
            <button
              key={c.id}
              onClick={() => setCategory(c.id)}
              className={cn(
                'px-2.5 py-1 rounded-md text-xs font-medium border transition-colors duration-150',
                category === c.id
                  ? 'bg-amber-600 border-amber-600 text-white'
                  : 'bg-[#FFFDF9] border-[#E3D9C6] text-stone-500 hover:text-stone-700 hover:border-[#D6CFC2]'
              )}
            >
              {c.label}
            </button>
          ))}
          <span className="ml-auto text-xs text-stone-400 flex items-center gap-1">
            <Filter className="h-3 w-3" />
            {filtered.length}
          </span>
        </div>
      </div>

      {/* Events grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <EventSkeleton key={i} />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 text-center gap-3">
          <Calendar className="h-8 w-8 text-stone-300" />
          <div>
            <p className="text-stone-700 font-medium text-sm">No events found</p>
            <p className="text-xs text-stone-500 mt-0.5">Try adjusting your filters</p>
          </div>
          <ShimmerButton variant="ghost" size="sm" onClick={() => { setSearch(''); setCategory('all'); setUpcoming(false); }}>
            Clear filters
          </ShimmerButton>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <AnimatePresence>
            {filtered.map((e, i) => {
              const isPast = e.date < today;
              const accent = CATEGORY_ACCENT[e.category.toLowerCase()] || 'from-stone-400 to-stone-500';
              const badgeColor = CATEGORY_COLOR[e.category.toLowerCase()] || 'slate';
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: i * 0.03 }}
                >
                  <Card
                    className={cn('p-4 relative overflow-hidden group', isPast && 'opacity-50')}
                    hover={!isPast}
                  >
                    <div className={cn('absolute top-0 inset-x-0 h-0.5 bg-gradient-to-r', accent)} />

                    <div className="space-y-2">
                      <div className="flex items-start justify-between gap-2">
                        <Badge variant={badgeColor}>{e.category}</Badge>
                        <BlueprintStat label="" value={e.semester} />
                      </div>

                      <h3 className={cn('font-medium text-sm text-stone-800 leading-snug line-clamp-2', !isPast && 'group-hover:text-amber-700 transition-colors')}>
                        {e.event}
                      </h3>

                      {e.description && (
                        <p className="text-xs text-stone-500 leading-relaxed line-clamp-2">{e.description}</p>
                      )}

                      <div className="flex items-center justify-between pt-1.5 border-t border-[#E8E2D5]">
                        <div className="flex items-center gap-1.5 text-xs text-amber-700">
                          <Clock className="h-3 w-3" />
                          {e.date}
                        </div>
                        {isPast ? (
                          <span className="text-2xs text-stone-400">Done</span>
                        ) : (
                          <span className="text-2xs text-amber-700 font-medium">Upcoming</span>
                        )}
                      </div>
                    </div>
                  </Card>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
};
