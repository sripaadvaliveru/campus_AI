import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Check, ChevronDown } from 'lucide-react';
import { cn } from '../lib/cn';
import type { College } from '../types';

interface CollegePopoverProps {
  colleges: College[];
  selected: College | null;
  onSelect: (college: College) => void;
}

export const CollegePopover: React.FC<CollegePopoverProps> = ({
  colleges, selected, onSelect,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const searchRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const filtered = colleges.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.short.toLowerCase().includes(search.toLowerCase()) ||
    c.type.toLowerCase().includes(search.toLowerCase())
  );

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsOpen(false);
    };
    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, []);

  useEffect(() => {
    if (isOpen && searchRef.current) {
      searchRef.current.focus();
      setSearch('');
    }
  }, [isOpen]);

  return (
    <div ref={containerRef} className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'flex items-center gap-2 px-3 py-1.5 rounded-full transition-colors text-sm font-medium',
          isOpen
            ? 'bg-blue-50 text-brand-blue border border-blue-200'
            : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border border-transparent'
        )}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <span className="text-base">{selected?.icon || '🎓'}</span>
        <span className="max-w-[100px] truncate hidden sm:inline">{selected?.short || 'College'}</span>
        <ChevronDown className={cn('h-3.5 w-3.5 transition-transform', isOpen && 'rotate-180')} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.96 }}
            transition={{ ease: [0.16, 1, 0.3, 1], duration: 0.2 }}
            className="absolute right-0 top-full mt-2 w-80 bg-white/95 backdrop-blur-xl border border-slate-200 rounded-xl shadow-xl overflow-hidden z-50"
            role="dialog"
            aria-label="Select college"
          >
            {/* Search */}
            <div className="p-3 border-b border-slate-100">
              <div className="relative">
                <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
                <input
                  ref={searchRef}
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                  placeholder="Search colleges..."
                  aria-label="Search colleges"
                  className="w-full bg-slate-50 text-sm text-slate-700 placeholder-slate-400 pl-8 pr-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-brand-blue focus:ring-1 focus:ring-brand-blue/20 transition"
                />
              </div>
            </div>

            {/* List */}
            <div className="max-h-72 overflow-y-auto p-1.5" role="listbox">
              {filtered.length === 0 ? (
                <p className="text-center text-sm text-slate-500 py-8">No colleges found.</p>
              ) : (
                filtered.map(college => {
                  const isSelected = selected?.id === college.id;
                  return (
                    <button
                      key={college.id}
                      role="option"
                      aria-selected={isSelected}
                      onClick={() => { onSelect(college); setIsOpen(false); }}
                      className={cn(
                        'w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-left text-sm transition-colors',
                        isSelected
                          ? 'bg-blue-50 text-slate-900'
                          : 'text-slate-600 hover:bg-slate-50'
                      )}
                    >
                      <span className="text-base flex-shrink-0">{college.icon}</span>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">{college.name}</p>
                        <p className="text-xs text-slate-400 truncate">{college.type}</p>
                      </div>
                      {isSelected && <Check className="h-4 w-4 text-brand-blue flex-shrink-0" />}
                    </button>
                  );
                })
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
