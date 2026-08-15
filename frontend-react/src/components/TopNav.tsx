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
  dashboard: 'bg-amber-50 text-amber-800',
  chat: 'bg-amber-50 text-amber-800',
  events: 'bg-yellow-50 text-yellow-800',
  directory: 'bg-olive-50 text-olive-800',
  analytics: 'bg-orange-50 text-orange-800',
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
      <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-[#FBF8F3]/80 backdrop-blur-md border-b border-[#E8E2D5]">
        <div className="flex items-center h-full px-4 md:px-6 lg:px-8 max-w-[1600px] mx-auto">
          {/* Logo */}
          <div className="flex items-center gap-2.5 mr-6 lg:mr-10 flex-shrink-0">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-600 to-amber-700 flex items-center justify-center">
              <GraduationCap className="h-4 w-4 text-white" />
            </div>
            <span className="font-display font-bold text-stone-900 text-sm tracking-tight hidden sm:inline">
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
                    'focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-amber',
                    isActive
                      ? SECTION_BG[item.id]
                      : 'text-stone-500 hover:text-stone-700 hover:bg-[#F3ECE1]'
                  )}
                >
                  <Icon className="h-4 w-4 inline mr-1.5" />
                  {item.label}
                  {item.badge && !isActive && (
                    <span className="ml-1.5 inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-2xs font-medium bg-amber-50 text-amber-700">
                      <span className="relative flex h-1.5 w-1.5">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
                        <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-amber-500" />
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
            <button className="p-2 rounded-lg hover:bg-[#F3ECE1] text-stone-500 transition-colors hidden md:flex" aria-label="Search">
              <Search className="h-4 w-4" />
            </button>

            {/* Mobile Hamburger */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="p-2 rounded-lg text-stone-500 hover:bg-[#F3ECE1] transition-colors md:hidden"
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
              className="fixed inset-x-0 top-0 z-50 bg-[#FBF8F3]/95 backdrop-blur-2xl border-b border-[#E8E2D5] shadow-xl md:hidden"
              role="dialog"
              aria-modal="true"
              aria-label="Navigation menu"
            >
              <div className="px-4 pt-4 pb-6 space-y-4">
                {/* Header */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-600 to-amber-700 flex items-center justify-center">
                      <GraduationCap className="h-4 w-4 text-white" />
                    </div>
                    <span className="font-display font-bold text-stone-900 text-sm">CampusAI</span>
                  </div>
                  <button
                    onClick={() => setMobileOpen(false)}
                    className="p-2 rounded-lg text-stone-400 hover:text-stone-600 hover:bg-[#F3ECE1] transition"
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
                            : 'text-stone-500 hover:text-stone-700 hover:bg-[#F3ECE1]'
                        )}
                      >
                        <Icon className="h-5 w-5" />
                        {item.label}
                        {item.badge && (
                          <span className="ml-auto inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-2xs font-medium bg-amber-50 text-amber-700">
                            {item.badge}
                          </span>
                        )}
                      </button>
                    );
                  })}
                </nav>

                {/* College Picker (Mobile) */}
                <div className="pt-2 border-t border-[#E8E2D5]">
                  <p className="px-4 text-xs text-stone-400 font-medium mb-2">Select College</p>
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
