import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Mail, Phone, Building2, Copy, Check, Users, UserCircle2 } from 'lucide-react';
import { Card, Badge, ShimmerButton, Skeleton } from './ui/Primitives';
import { cn } from '../lib/cn';
import type { Contact } from '../types';

interface DirectoryTabProps {
  contacts: Contact[];
  loading: boolean;
}

const ContactSkeleton = () => (
  <Card className="p-5" hover={false}>
    <div className="flex items-start gap-3 mb-4">
      <Skeleton className="w-10 h-10 rounded-xl flex-shrink-0" />
      <div className="flex-1 min-w-0 space-y-2">
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-3 w-1/2" />
      </div>
    </div>
    <Skeleton className="h-5 w-20 rounded-full mb-3" />
    <div className="space-y-2 pt-3 border-t border-slate-100">
      <Skeleton className="h-3 w-full" />
      <Skeleton className="h-3 w-2/3" />
    </div>
  </Card>
);

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

  const AVATAR_COLORS = [
    'from-blue-500 to-indigo-600',
    'from-purple-500 to-pink-600',
    'from-emerald-500 to-teal-600',
    'from-amber-500 to-orange-600',
    'from-rose-500 to-red-600',
    'from-cyan-500 to-sky-600',
  ];

  return (
    <div className="space-y-6 pb-10">
      <div>
        <h1 className="font-display text-2xl font-black text-slate-900 tracking-tight">Contact Directory</h1>
        <p className="text-sm text-slate-500">Faculty, staff, HoDs, wardens, and placement coordinators.</p>
      </div>

      {/* Filters */}
      <Card className="p-4 space-y-3" hover={false}>
        <div className="flex gap-3 flex-col sm:flex-row">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search name, title, or specialization…"
              aria-label="Search contacts by name, title, or specialization"
              className="w-full bg-slate-50 text-sm text-slate-900 placeholder-slate-400 pl-9 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-blue focus:border-transparent transition"
            />
          </div>
          <select
            value={dept}
            onChange={e => setDept(e.target.value)}
            className="bg-slate-50 text-sm text-slate-700 px-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-blue focus:border-transparent transition sm:w-56"
          >
            {departments.map((d, i) => (
              <option key={i} value={d}>{d === 'all' ? 'All Departments' : d}</option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-1.5 text-2xs text-slate-400">
          <Users className="h-3 w-3" />
          {filtered.length} of {contacts.length} contacts
        </div>
      </Card>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <ContactSkeleton key={i} />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center gap-4">
          <UserCircle2 className="h-10 w-10 text-slate-300" />
          <div>
            <p className="text-slate-700 font-semibold">No contacts found</p>
            <p className="text-sm text-slate-500 mt-1">Try a different search term</p>
          </div>
          <ShimmerButton variant="ghost" size="sm" onClick={() => { setSearch(''); setDept('all'); }}>
            Clear filters
          </ShimmerButton>
        </div>
      ) : (
        <motion.div
          className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4"
          initial="hidden"
          animate="show"
          variants={{ hidden: {}, show: { transition: { staggerChildren: 0.05 } } }}
        >
          <AnimatePresence>
            {filtered.map((c, i) => {
              const avatarGradient = AVATAR_COLORS[i % AVATAR_COLORS.length];
              return (
                <motion.div
                  key={i}
                  variants={{
                    hidden: { opacity: 0, scale: 0.96 },
                    show: { opacity: 1, scale: 1, transition: { duration: 0.35, ease: [0.16, 1, 0.3, 1] } },
                  }}
                >
                  <Card className="p-5 group">
                    {/* Card header */}
                    <div className="flex items-start gap-3 mb-4">
                      <div className={cn(
                        'w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold text-sm flex-shrink-0 bg-gradient-to-br',
                        avatarGradient
                      )}>
                        {initials(c.name)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-bold text-sm text-slate-900 group-hover:text-brand-blue transition-colors truncate">
                          {c.name}
                        </h3>
                        <p className="text-2xs text-slate-500 font-medium truncate">{c.designation}</p>
                      </div>
                    </div>

                    {/* Department badge */}
                    <div className="mb-3">
                      <Badge variant="slate" className="truncate max-w-full">{c.department}</Badge>
                    </div>

                    {/* Specialization */}
                    {c.specialization && (
                      <p className="text-2xs text-slate-500 mb-3 line-clamp-1">
                        Spec: {c.specialization}
                      </p>
                    )}

                    {/* Contact details */}
                    <div className="space-y-1.5 pt-3 border-t border-slate-100">
                      {/* Email */}
                      <div className="flex items-center justify-between group/row">
                        <a
                          href={`mailto:${c.email}`}
                          className="flex items-center gap-2 text-2xs text-slate-500 hover:text-brand-blue transition-colors truncate pr-2"
                        >
                          <Mail className="h-3 w-3 flex-shrink-0 text-slate-400" />
                          <span className="truncate">{c.email}</span>
                        </a>
                        <button
                          onClick={() => copy(c.email, `${i}-email`)}
                          className="opacity-0 group-hover/row:opacity-100 p-1 rounded text-slate-400 hover:text-slate-700 transition-all duration-150 flex-shrink-0"
                        >
                          {copied === `${i}-email` ? <Check className="h-3 w-3 text-emerald-500" /> : <Copy className="h-3 w-3" />}
                        </button>
                      </div>

                      {/* Phone */}
                      {c.phone && (
                        <div className="flex items-center justify-between group/row">
                          <a
                            href={`tel:${c.phone}`}
                            className="flex items-center gap-2 text-2xs text-slate-500 hover:text-emerald-600 transition-colors"
                          >
                            <Phone className="h-3 w-3 flex-shrink-0 text-slate-400" />
                            <span>{c.phone}</span>
                          </a>
                          <button
                            onClick={() => copy(c.phone, `${i}-phone`)}
                            className="opacity-0 group-hover/row:opacity-100 p-1 rounded text-slate-400 hover:text-slate-700 transition-all duration-150 flex-shrink-0"
                          >
                            {copied === `${i}-phone` ? <Check className="h-3 w-3 text-emerald-500" /> : <Copy className="h-3 w-3" />}
                          </button>
                        </div>
                      )}

                      {/* Office */}
                      {c.cabin && (
                        <div className="flex items-center gap-2 text-2xs text-slate-500">
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
        </motion.div>
      )}
    </div>
  );
};
