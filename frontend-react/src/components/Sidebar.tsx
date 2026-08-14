import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard, MessageSquareCode, Calendar, BookUser,
  BarChart3, GraduationCap, Search, ChevronLeft, Zap, Menu, X
} from 'lucide-react';
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

interface SidebarProps {
  colleges: College[];
  selectedCollege: College | null;
  onSelectCollege: (c: College) => void;
  activeTab: TabId;
  setActiveTab: (t: TabId) => void;
  modelName: string;
  onWidthChange?: (width: number) => void;
  onCollapsedChange?: (collapsed: boolean) => void;
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
  modelName: string;
}

const SidebarContent: React.FC<SidebarContentProps> = ({
  collapsed, onToggleCollapse, search, onSearchChange, filtered,
  selectedCollege, onSelectCollege, activeTab, handleNav, modelName,
}) => (
  <div className="flex flex-col h-full bg-white">
    {/* Logo */}
    <div className={cn(
      'flex items-center gap-3 px-4 py-5 border-b border-slate-200',
      collapsed ? 'justify-center' : 'justify-between'
    )}>
      <div className="flex items-center gap-3 min-w-0">
        <div className="relative flex-shrink-0">
          <div className="w-9 h-9 rounded-xl bg-brand-blue flex items-center justify-center">
            <GraduationCap className="h-5 w-5 text-white" />
          </div>
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <p className="font-display font-bold text-slate-900 text-sm leading-tight tracking-wide">CampusAI</p>
            <p className="text-2xs text-slate-400 font-medium uppercase tracking-widest">Universal</p>
          </div>
        )}
      </div>
      {!collapsed && (
        <button
          onClick={onToggleCollapse}
          className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors hidden lg:flex"
        >
          <ChevronLeft className="h-4 w-4" />
        </button>
      )}
      {collapsed && (
        <button
          onClick={onToggleCollapse}
          className="absolute left-full top-5 ml-2 p-1.5 bg-white border border-slate-200 rounded-lg text-slate-400 hover:text-slate-600 transition-colors hidden lg:flex shadow-sm"
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
              'focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue',
              collapsed ? 'justify-center' : '',
              isActive
                ? 'bg-brand-blue text-white'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            )}
            title={collapsed ? item.label : undefined}
          >
            {isActive && (
              <motion.div
                layoutId="activeNav"
                className="absolute inset-0 rounded-xl bg-brand-blue"
                transition={{ type: 'spring', duration: 0.5 }}
              />
            )}
            <Icon className={cn('h-5 w-5 flex-shrink-0 relative z-10', isActive ? 'text-white' : 'text-slate-400')} />
            {!collapsed && (
              <span className="relative z-10 flex-1 text-left">{item.label}</span>
            )}
            {!collapsed && item.badge && (
              <span className="relative z-10 inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-2xs font-semibold bg-emerald-50 text-emerald-600 border border-emerald-200">
                <span className="relative flex h-1.5 w-1.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-500" />
                </span>
                {item.badge}
              </span>
            )}
          </button>
        );
      })}
    </nav>

    {/* Separator */}
    {!collapsed && (
      <div className="px-4 pb-2">
        <div className="h-px bg-slate-200" />
        <p className="text-2xs text-slate-400 uppercase tracking-widest font-semibold mt-3 mb-2 px-1">Select College</p>

        {/* Search */}
        <div className="relative mb-2">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3 w-3 text-slate-400" />
          <input
            value={search}
            onChange={e => onSearchChange(e.target.value)}
            placeholder="Search college..."
            aria-label="Search colleges"
            className="w-full bg-slate-50 text-xs text-slate-700 placeholder-slate-400 pl-8 pr-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-blue focus:border-transparent transition"
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
                  ? 'bg-blue-50 border-blue-200 text-slate-900'
                  : 'border-transparent text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              )}
              title={collapsed ? college.name : undefined}
            >
              <span className={cn('text-base flex-shrink-0 transition-transform duration-200 group-hover:scale-110', collapsed && 'text-lg')}>
                {college.icon}
              </span>
              {!collapsed && (
                <>
                  <div className="flex-1 min-w-0">
                    <p className={cn('text-xs font-semibold truncate', isSelected ? 'text-slate-900' : 'text-slate-600 group-hover:text-slate-900')}>
                      {college.short}
                    </p>
                    <p className="text-2xs text-slate-400 truncate">{college.type}</p>
                  </div>
                  {isSelected && (
                    <div
                      className="w-1.5 h-1.5 rounded-full flex-shrink-0"
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
      <div className="px-4 py-3 border-t border-slate-200 flex-shrink-0">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 text-2xs text-slate-500">
            <Zap className="h-3 w-3 text-amber-500" />
            <span>{modelName} · FAISS RAG</span>
          </div>
        </div>
      </div>
    )}
  </div>
);

export const Sidebar: React.FC<SidebarProps> = ({
  colleges, selectedCollege, onSelectCollege, activeTab, setActiveTab, modelName, onCollapsedChange,
}) => {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [search, setSearch] = useState('');

  const handleToggleCollapse = () => {
    const next = !collapsed;
    setCollapsed(next);
    onCollapsedChange?.(next);
  };

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
    onToggleCollapse: handleToggleCollapse,
    search,
    onSearchChange: setSearch,
    filtered,
    selectedCollege,
    onSelectCollege,
    activeTab,
    handleNav,
    modelName,
  };

  return (
    <>
      {/* Desktop Sidebar */}
      <motion.aside
        animate={{ width: collapsed ? 72 : 256 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className={cn(
          'hidden lg:flex flex-col fixed left-0 top-0 bottom-0 z-50',
          'bg-white border-r border-slate-200 overflow-hidden relative',
        )}
      >
        <SidebarContent {...sidebarContentProps} />
      </motion.aside>

      {/* Mobile trigger */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-4 py-3.5 bg-white border-b border-slate-200">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-brand-blue flex items-center justify-center">
            <GraduationCap className="h-4 w-4 text-white" />
          </div>
          <span className="font-display font-bold text-slate-900 text-sm">CampusAI</span>
        </div>
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-50 transition"
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
              className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 lg:hidden"
              onClick={() => setMobileOpen(false)}
            />
            <motion.aside
              initial={{ x: -280 }} animate={{ x: 0 }} exit={{ x: -280 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              className="fixed left-0 top-0 bottom-0 w-64 z-50 bg-white border-r border-slate-200 lg:hidden overflow-hidden"
            >
              <div className="mt-14">
                <SidebarContent {...sidebarContentProps} />
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

    </>
  );
};
