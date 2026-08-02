import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard, MessageSquareCode, Calendar, BookUser,
  BarChart3, GraduationCap, Search, ChevronLeft, Zap, Menu, X
} from 'lucide-react';
import { cn } from '../lib/cn';
import { Badge } from './ui/Primitives';
import type { College, TabId } from '../types';

interface NavItem {
  id: TabId;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'chat', label: 'AI Chat', icon: MessageSquareCode, badge: 'Live' },
  { id: 'events', label: 'Calendar', icon: Calendar },
  { id: 'directory', label: 'Directory', icon: BookUser },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
];

interface SidebarProps {
  colleges: College[];
  selectedCollege: College | null;
  onSelectCollege: (c: College) => void;
  activeTab: TabId;
  setActiveTab: (t: TabId) => void;
}

interface SidebarContentProps {
  collapsed: boolean;
  onToggleCollapse: () => void;
  search: string;
  onSearchChange: (v: string) => void;
  filtered: College[];
  selectedCollege: College | null;
  onSelectCollege: (c: College) => void;
  activeTab: TabId;
  handleNav: (id: TabId) => void;
}

const SidebarContent: React.FC<SidebarContentProps> = ({
  collapsed, onToggleCollapse, search, onSearchChange, filtered,
  selectedCollege, onSelectCollege, activeTab, handleNav,
}) => (
  <div className="flex flex-col h-full">
    {/* Logo */}
    <div className={cn(
      'flex items-center gap-3 px-4 py-5 border-b border-white/5',
      collapsed ? 'justify-center' : 'justify-between'
    )}>
      <div className="flex items-center gap-3 min-w-0">
        <div className="relative flex-shrink-0">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-glow-sm">
            <GraduationCap className="h-5 w-5 text-white" />
          </div>
          <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-emerald-400 border-2 border-slate-950 animate-bounce-subtle" />
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <p className="font-display font-bold text-white text-sm leading-tight tracking-wide">CampusAI</p>
            <p className="text-2xs text-slate-500 font-medium uppercase tracking-widest">Universal</p>
          </div>
        )}
      </div>
      {!collapsed && (
        <button
          onClick={onToggleCollapse}
          className="p-1.5 rounded-lg text-slate-600 hover:text-slate-300 hover:bg-white/5 transition-colors hidden lg:flex"
        >
          <ChevronLeft className="h-4 w-4" />
        </button>
      )}
      {collapsed && (
        <button
          onClick={onToggleCollapse}
          className="absolute left-full top-5 ml-2 p-1.5 glass rounded-lg text-slate-400 hover:text-white transition-colors hidden lg:flex"
        >
          <ChevronLeft className="h-4 w-4 rotate-180" />
        </button>
      )}
    </div>

    {/* Navigation */}
    <nav className="px-2 py-4 space-y-0.5 flex-shrink-0">
      {NAV_ITEMS.map((item) => {
        const Icon = item.icon;
        const isActive = activeTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => handleNav(item.id)}
            className={cn(
              'relative w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200',
              'focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500',
              collapsed ? 'justify-center' : '',
              isActive
                ? 'bg-blue-500/15 text-blue-400 border border-blue-500/20'
                : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
            )}
            title={collapsed ? item.label : undefined}
          >
            {isActive && (
              <motion.div
                layoutId="activeNav"
                className="absolute inset-0 rounded-xl bg-blue-500/10"
                transition={{ type: 'spring', duration: 0.5 }}
              />
            )}
            <Icon className={cn('h-5 w-5 flex-shrink-0 relative z-10', isActive ? 'text-blue-400' : 'text-slate-500')} />
            {!collapsed && (
              <span className="relative z-10 flex-1 text-left">{item.label}</span>
            )}
            {!collapsed && item.badge && (
              <Badge variant="blue" dot pulse className="relative z-10 scale-90">
                {item.badge}
              </Badge>
            )}
          </button>
        );
      })}
    </nav>

    {/* Separator */}
    {!collapsed && (
      <div className="px-4 pb-2">
        <div className="h-px bg-white/5" />
        <p className="text-2xs text-slate-600 uppercase tracking-widest font-semibold mt-3 mb-2 px-1">Campus Context</p>

        {/* Search */}
        <div className="relative mb-2">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3 w-3 text-slate-600" />
          <input
            value={search}
            onChange={e => onSearchChange(e.target.value)}
            placeholder="Search college..."
            aria-label="Search colleges"
            className="w-full bg-slate-900/60 text-xs text-slate-300 placeholder-slate-600 pl-8 pr-3 py-2 rounded-lg border border-white/5 focus:outline-none focus:border-blue-500/30 transition"
          />
        </div>
      </div>
    )}

    {/* College list */}
    <div className={cn('flex-1 overflow-y-auto px-2 pb-4 space-y-0.5', collapsed && 'flex flex-col items-center')}>
      <AnimatePresence>
        {filtered.map((college) => {
          const isSelected = selectedCollege?.id === college.id;
          return (
            <motion.button
              key={college.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              onClick={() => { onSelectCollege(college); handleNav('chat'); }}
              className={cn(
                'w-full flex items-center gap-2.5 px-2.5 py-2 rounded-xl text-left transition-all duration-200 group border',
                collapsed ? 'w-10 h-10 p-0 justify-center' : '',
                isSelected
                  ? 'bg-slate-800/80 border-white/8 text-white'
                  : 'border-transparent text-slate-400 hover:bg-white/5 hover:text-slate-200'
              )}
              title={collapsed ? college.name : undefined}
            >
              <span className={cn('text-base flex-shrink-0 transition-transform duration-200 group-hover:scale-110', collapsed && 'text-lg')}>
                {college.icon}
              </span>
              {!collapsed && (
                <>
                  <div className="flex-1 min-w-0">
                    <p className={cn('text-xs font-semibold truncate', isSelected ? 'text-slate-100' : 'text-slate-400 group-hover:text-slate-200')}>
                      {college.short}
                    </p>
                    <p className="text-2xs text-slate-600 truncate">{college.type}</p>
                  </div>
                  {isSelected && (
                    <div
                      className="w-1.5 h-1.5 rounded-full flex-shrink-0 animate-bounce-subtle"
                      style={{ backgroundColor: college.color }}
                    />
                  )}
                </>
              )}
            </motion.button>
          );
        })}
      </AnimatePresence>
    </div>

    {/* Footer */}
    {!collapsed && (
      <div className="px-4 py-3 border-t border-white/5 flex-shrink-0">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 text-2xs text-slate-600">
            <Zap className="h-3 w-3 text-amber-500" />
            <span>GPT-4o mini · FAISS RAG</span>
          </div>
        </div>
      </div>
    )}
  </div>
);

export const Sidebar: React.FC<SidebarProps> = ({
  colleges, selectedCollege, onSelectCollege, activeTab, setActiveTab,
}) => {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [search, setSearch] = useState('');

  const filtered = colleges.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.short.toLowerCase().includes(search.toLowerCase())
  );

  const handleNav = (id: TabId) => {
    setActiveTab(id);
    setMobileOpen(false);
  };

  const sidebarContentProps: SidebarContentProps = {
    collapsed,
    onToggleCollapse: () => setCollapsed(!collapsed),
    search,
    onSearchChange: setSearch,
    filtered,
    selectedCollege,
    onSelectCollege,
    activeTab,
    handleNav,
  };

  return (
    <>
      {/* Desktop Sidebar */}
      <motion.aside
        animate={{ width: collapsed ? 72 : 256 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className={cn(
          'hidden lg:flex flex-col fixed left-0 top-0 bottom-0 z-50',
          'glass border-r border-white/5 overflow-hidden relative',
        )}
      >
        <SidebarContent {...sidebarContentProps} />
      </motion.aside>

      {/* Mobile trigger */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-4 py-3.5 glass border-b border-white/5">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
            <GraduationCap className="h-4 w-4 text-white" />
          </div>
          <span className="font-display font-bold text-white text-sm">CampusAI</span>
        </div>
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition"
        >
          {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile Sidebar Drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/70 backdrop-blur-sm z-40 lg:hidden"
              onClick={() => setMobileOpen(false)}
            />
            <motion.aside
              initial={{ x: -280 }} animate={{ x: 0 }} exit={{ x: -280 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              className="fixed left-0 top-0 bottom-0 w-64 z-50 glass border-r border-white/5 lg:hidden overflow-hidden"
            >
              <div className="mt-14">
                <SidebarContent {...sidebarContentProps} />
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Desktop spacer */}
      <motion.div
        animate={{ width: collapsed ? 72 : 256 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className="hidden lg:block flex-shrink-0"
      />
    </>
  );
};
