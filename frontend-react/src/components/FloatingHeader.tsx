import React from 'react';
import { motion } from 'framer-motion';
import { Search, Wifi } from 'lucide-react';
import { spring } from './ui/Primitives';
import type { College } from '../types';

interface FloatingHeaderProps {
  college: College | null;
  modelName: string;
  onSearchShortcut?: () => void;
}

export const FloatingHeader: React.FC<FloatingHeaderProps> = ({
  college, modelName, onSearchShortcut,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -12, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ ...spring.crisp, delay: 0.1 }}
      className="fixed top-3 left-1/2 -translate-x-1/2 z-50 hidden lg:flex"
    >
      <div className="flex items-center gap-3 px-4 py-2 rounded-2xl bg-white/80 backdrop-blur-xl border border-slate-200/60 shadow-card">
        {/* College badge */}
        <div className="flex items-center gap-2">
          <span className="text-sm">{college?.icon || '🎓'}</span>
          <span className="text-xs font-medium text-slate-700 max-w-[140px] truncate">
            {college?.short || 'Select College'}
          </span>
        </div>

        {/* Separator */}
        <div className="w-px h-4 bg-slate-200" />

        {/* Context badge */}
        <span className="font-mono text-2xs tracking-wider text-slate-400 uppercase">
          {modelName}
        </span>

        {/* Separator */}
        <div className="w-px h-4 bg-slate-200" />

        {/* Online status */}
        <div className="flex items-center gap-1.5">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
          </span>
          <span className="font-mono text-2xs text-slate-400">Online</span>
        </div>

        {/* Separator */}
        <div className="w-px h-4 bg-slate-200" />

        {/* Search shortcut */}
        <button
          onClick={onSearchShortcut}
          className="flex items-center gap-1.5 px-2 py-1 rounded-lg hover:bg-slate-100 transition-colors group"
        >
          <Search className="h-3 w-3 text-slate-400 group-hover:text-slate-600 transition-colors" />
          <kbd className="font-mono text-2xs text-slate-400 bg-slate-50 border border-slate-200 rounded px-1 py-0.5">
            /
          </kbd>
        </button>
      </div>
    </motion.div>
  );
};
