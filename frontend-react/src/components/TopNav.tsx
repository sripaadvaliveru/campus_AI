import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard, MessageSquareCode, Calendar, BookUser,
  BarChart3, GraduationCap, Search, Menu, X
} from 'lucide-react';
import { CollegePopover } from './CollegePopover';
import { cn } from '../lib/cn';
import type { College, TabId } from '../types';

interface NavItem {
  id: TabId;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'chat', label: 'Chat', icon: MessageSquareCode, badge: 'Live' },
  { id: 'events', label: 'Events', icon: Calendar },
  { id: 'directory', label: 'Directory', icon: BookUser },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
];

const SECTION_COLORS: Record<TabId, string> = {
  dashboard: 'var(--dashboard)',
  chat: 'var(--chat)',
  events: 'var(--events)',
  directory: 'var(--directory)',
  analytics: 'var(--analytics)',
};

const SECTION_BG: Record<TabId, string> = {
  dashboard: 'bg-indigo-50 text-indigo-700',
  chat: 'bg-blue-50 text-blue-700',
  events: 'bg-amber-50 text-amber-700',
  directory: 'bg-emerald-50 text-emerald-700',
  analytics: 'bg-violet-50 text-violet-700',
};

interface TopNavProps {
  colleges: College[];
  selectedCollege: College | null;
  onSelectCollege: (c: College) => void;
  activeTab: TabId;
  setActiveTab: (t: TabId) => void;
  modelName: string;
}

export const TopNav: React.FC<TopNavProps> = ({
  colleges, selectedCollege, onSelectCollege, activeTab, setActiveTab, modelName,
}) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleNav = (id: TabId) => {
    setActiveTab(id);
    setMobileOpen(false);
  };

  return (
    <>
      {/* Desktop + Tablet Top Nav */}
      <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-white/80 backdrop-blur-xl border-b border-slate-200/60">
        <div className="flex items-center h-full px-4 md:px-6 lg:px-8 max-w-[1600px] mx-auto">
          {/* Logo */}
          <div className="flex items-center gap-2.5 mr-6 lg:mr-10 flex-shrink-0">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center">
              <GraduationCap className="h-4 w-4 text-white" />
            </div>
            <span className="font-display font-bold text-slate-900 text-sm tracking-tight hidden sm:inline">
              CampusAI
            </span>
          </div>

          {/* Nav Tabs (tablet+) */}
          <nav className="hidden md:flex items-center gap-1 flex-1" role="navigation" aria-label="Main">
            {NAV_ITEMS.map(item => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNav(item.id)}
                  aria-current={isActive ? 'page' : undefined}
                  className={cn(
                    'relative px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-150',
                    'focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue',
                    isActive
                      ? SECTION_BG[item.id]
                      : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                  )}
                >
                  <Icon className="h-4 w-4 inline mr-1.5" />
                  {item.label}
                  {item.badge && !isActive && (
                    <span className="ml-1.5 inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-2xs font-medium bg-emerald-50 text-emerald-600">
                      <span className="relative flex h-1.5 w-1.5">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                        <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-500" />
                      </span>
                      {item.badge}
                    </span>
                  )}
                  {isActive && (
                    <motion.div
                      layoutId="activeTabIndicator"
                      className="absolute bottom-0 left-2 right-2 h-0.5 rounded-full"
                      style={{ backgroundColor: SECTION_COLORS[item.id] }}
                      transition={{ ease: [0.16, 1, 0.3, 1], duration: 0.3 }}
                    />
                  )}
                </button>
              );
            })}
          </nav>

          {/* Right Actions */}
          <div className="ml-auto flex items-center gap-2 md:gap-3">
            <CollegePopover
              colleges={colleges}
              selected={selectedCollege}
              onSelect={onSelectCollege}
            />
            <button className="p-2 rounded-lg hover:bg-slate-100 text-slate-500 transition-colors hidden md:flex" aria-label="Search">
              <Search className="h-4 w-4" />
            </button>

            {/* Mobile Hamburger */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 transition-colors md:hidden"
              aria-label="Menu"
            >
              {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 md:hidden"
              onClick={() => setMobileOpen(false)}
            />
            <motion.div
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -20, opacity: 0 }}
              transition={{ ease: [0.16, 1, 0.3, 1], duration: 0.25 }}
              className="fixed inset-x-0 top-0 z-50 bg-white/95 backdrop-blur-2xl border-b border-slate-200 shadow-xl md:hidden"
              role="dialog"
              aria-modal="true"
              aria-label="Navigation menu"
            >
              <div className="px-4 pt-4 pb-6 space-y-4">
                {/* Header */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center">
                      <GraduationCap className="h-4 w-4 text-white" />
                    </div>
                    <span className="font-display font-bold text-slate-900 text-sm">CampusAI</span>
                  </div>
                  <button
                    onClick={() => setMobileOpen(false)}
                    className="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition"
                    aria-label="Close menu"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>

                {/* Nav Links */}
                <nav className="space-y-1" role="navigation" aria-label="Mobile navigation">
                  {NAV_ITEMS.map(item => {
                    const Icon = item.icon;
                    const isActive = activeTab === item.id;
                    return (
                      <button
                        key={item.id}
                        onClick={() => handleNav(item.id)}
                        aria-current={isActive ? 'page' : undefined}
                        className={cn(
                          'w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors',
                          isActive
                            ? SECTION_BG[item.id]
                            : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                        )}
                      >
                        <Icon className="h-5 w-5" />
                        {item.label}
                        {item.badge && (
                          <span className="ml-auto inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-2xs font-medium bg-emerald-50 text-emerald-600">
                            {item.badge}
                          </span>
                        )}
                      </button>
                    );
                  })}
                </nav>

                {/* College Picker (Mobile) */}
                <div className="pt-2 border-t border-slate-100">
                  <p className="px-4 text-xs text-slate-400 font-medium mb-2">Select College</p>
                  <div className="px-4">
                    <CollegePopover
                      colleges={colleges}
                      selected={selectedCollege}
                      onSelect={(c) => { onSelectCollege(c); setMobileOpen(false); }}
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};
