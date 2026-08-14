import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Mail, Phone, Building2, Copy, Check, Users, UserCircle2 } from 'lucide-react';
import { Card, Badge, ShimmerButton, Skeleton } from './ui/Primitives';
import { DoodlePeople } from './ui/doodles/DoodlePeople';
import { cn } from '../lib/cn';
import type { Contact } from '../types';

interface DirectoryTabProps {
  contacts: Contact[];
  loading: boolean;
}

const ContactSkeleton = () => (
  <Card className="p-4" hover={false}>
    <div className="flex items-start gap-3 mb-3">
      <Skeleton className="w-9 h-9 rounded-full flex-shrink-0" />
      <div className="flex-1 min-w-0 space-y-2">
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-3 w-1/2" />
      </div>
    </div>
    <Skeleton className="h-5 w-20 rounded-full mb-2" />
    <div className="space-y-1.5 pt-2 border-t border-slate-100">
      <Skeleton className="h-3 w-full" />
      <Skeleton className="h-3 w-2/3" />
    </div>
  </Card>
);

const AVATAR_COLORS = [
  'from-blue-500 to-indigo-600',
  'from-purple-500 to-pink-600',
  'from-emerald-500 to-teal-600',
  'from-amber-500 to-orange-600',
  'from-rose-500 to-red-600',
  'from-cyan-500 to-sky-600',
];

export const DirectoryTab: React.FC<DirectoryTabProps> = ({ contacts, loading }) => {
  const [search, setSearch] = useState('');
  const [dept, setDept] = useState('all');
  const [copied, setCopied] = useState<string | null>(null);

  const departments = ['all', ...Array.from(new Set(contacts.map(c => c.department).filter(Boolean)))];

  const copy = (text: string, key: string) => {
    navigator.clipboard.writeText(text).catch(() => {});
    setCopied(key);
    setTimeout(() => setCopied(null), 2000);
  };

  const filtered = contacts.filter(c => {
    const text = [c.name, c.designation, c.department, c.specialization || ''].join(' ').toLowerCase();
    return text.includes(search.toLowerCase()) &&
      (dept === 'all' || c.department.toLowerCase() === dept.toLowerCase());
  });

  const initials = (name: string) => name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();

  return (
    <div className="space-y-5 pb-10 relative">
      <DoodlePeople />
      <div className="relative z-10">
        <h1 className="font-display text-xl font-semibold gradient-text bg-gradient-to-r from-emerald-600 to-teal-600 tracking-tight">Contact Directory</h1>
        <p className="text-xs text-slate-500 mt-0.5">Faculty, staff, HoDs, and placement coordinators.</p>
      </div>

      {/* Filters */}
      <div className="space-y-2">
        <div className="flex gap-2 flex-col sm:flex-row">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search name, title, or specialization…"
              aria-label="Search contacts"
              className="w-full bg-white text-sm text-slate-700 placeholder-slate-400 pl-9 pr-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-brand-blue focus:ring-1 focus:ring-brand-blue/20 transition"
            />
          </div>
          <select
            value={dept}
            onChange={e => setDept(e.target.value)}
            className="bg-white text-sm text-slate-700 px-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-brand-blue focus:ring-1 focus:ring-brand-blue/20 transition sm:w-56 appearance-none cursor-pointer"
            style={{ backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e")`, backgroundPosition: 'right 0.5rem center', backgroundRepeat: 'no-repeat', backgroundSize: '1.5em 1.5em', paddingRight: '2.5rem' }}
          >
            {departments.map((d, i) => (
              <option key={i} value={d}>{d === 'all' ? 'All Departments' : d}</option>
            ))}
          </select>
        </div>
        <p className="text-xs text-slate-400 flex items-center gap-1">
          <Users className="h-3 w-3" />
          {filtered.length} of {contacts.length} contacts
        </p>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <ContactSkeleton key={i} />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 text-center gap-3">
          <UserCircle2 className="h-8 w-8 text-slate-300" />
          <div>
            <p className="text-slate-700 font-medium text-sm">No contacts found{search ? ` for "${search}"` : ''}</p>
            <p className="text-xs text-slate-500 mt-0.5">Try a different search or department filter</p>
          </div>
          <ShimmerButton variant="ghost" size="sm" onClick={() => { setSearch(''); setDept('all'); }}>
            Clear filters
          </ShimmerButton>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-3">
          <AnimatePresence>
            {filtered.map((c, i) => {
              const avatarGradient = AVATAR_COLORS[i % AVATAR_COLORS.length];
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, scale: 0.97 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.25, delay: i * 0.02 }}
                >
                  <Card className="p-4 group">
                    <div className="flex items-start gap-3 mb-3">
                      <div className={cn(
                        'w-9 h-9 rounded-full flex items-center justify-center text-white font-semibold text-xs flex-shrink-0 bg-gradient-to-br',
                        avatarGradient
                      )}>
                        {initials(c.name)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-medium text-sm text-slate-800 group-hover:text-brand-blue transition-colors truncate">
                          {c.name}
                        </h3>
                        <p className="text-xs text-slate-500 truncate">{c.designation}</p>
                      </div>
                    </div>

                    <div className="mb-2">
                      <Badge variant="slate" className="truncate max-w-full">{c.department}</Badge>
                    </div>

                    {c.specialization && (
                      <p className="text-xs text-slate-400 mb-2 line-clamp-1">
                        {c.specialization}
                      </p>
                    )}

                    <div className="space-y-1 pt-2 border-t border-slate-100">
                      <div className="flex items-center justify-between group/row">
                        <a
                          href={`mailto:${c.email}`}
                          className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-brand-blue transition-colors truncate pr-2"
                        >
                          <Mail className="h-3 w-3 flex-shrink-0 text-slate-400" />
                          <span className="truncate">{c.email}</span>
                        </a>
                        <button
                          onClick={() => copy(c.email, `${i}-email`)}
                          className="opacity-0 group-hover/row:opacity-100 p-0.5 rounded text-slate-400 hover:text-slate-700 transition-all duration-150 flex-shrink-0"
                        >
                          {copied === `${i}-email` ? <Check className="h-3 w-3 text-emerald-500" /> : <Copy className="h-3 w-3" />}
                        </button>
                      </div>

                      {c.phone && (
                        <div className="flex items-center justify-between group/row">
                          <a
                            href={`tel:${c.phone}`}
                            className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-emerald-600 transition-colors"
                          >
                            <Phone className="h-3 w-3 flex-shrink-0 text-slate-400" />
                            <span>{c.phone}</span>
                          </a>
                          <button
                            onClick={() => copy(c.phone, `${i}-phone`)}
                            className="opacity-0 group-hover/row:opacity-100 p-0.5 rounded text-slate-400 hover:text-slate-700 transition-all duration-150 flex-shrink-0"
                          >
                            {copied === `${i}-phone` ? <Check className="h-3 w-3 text-emerald-500" /> : <Copy className="h-3 w-3" />}
                          </button>
                        </div>
                      )}

                      {c.cabin && (
                        <div className="flex items-center gap-1.5 text-xs text-slate-500">
                          <Building2 className="h-3 w-3 flex-shrink-0 text-slate-400" />
                          <span>{c.cabin}</span>
                        </div>
                      )}
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
