import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard, MessageSquareCode, Calendar, BookUser,
  BarChart3, GraduationCap, Search, ChevronLeft, Menu, X
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
      'flex items-center gap-3 px-4 py-4 border-b border-slate-100',
      collapsed ? 'justify-center' : 'justify-between'
    )}>
      <div className="flex items-center gap-2.5 min-w-0">
        <div className="w-8 h-8 rounded-lg bg-brand-blue flex items-center justify-center flex-shrink-0">
          <GraduationCap className="h-4 w-4 text-white" />
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <p className="font-display font-semibold text-slate-900 text-sm leading-tight tracking-tight">CampusAI</p>
          </div>
        )}
      </div>
      {!collapsed && (
        <button
          onClick={onToggleCollapse}
          className="p-1 rounded-md text-slate-400 hover:text-slate-600 hover:bg-slate-50 transition-colors hidden lg:flex"
        >
          <ChevronLeft className="h-4 w-4" />
        </button>
      )}
      {collapsed && (
        <button
          onClick={onToggleCollapse}
          className="absolute left-full top-4 ml-2 p-1 bg-white border border-slate-200 rounded-md text-slate-400 hover:text-slate-600 transition-colors hidden lg:flex shadow-sm"
        >
          <ChevronLeft className="h-4 w-4 rotate-180" />
        </button>
      )}
    </div>

    {/* Navigation */}
    <nav className="px-2 py-3 space-y-0.5 flex-shrink-0">
      {NAV_ITEMS.map((item) => {
        const Icon = item.icon;
        const isActive = activeTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => handleNav(item.id)}
            aria-current={isActive ? 'page' : undefined}
            className={cn(
              'relative w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-150',
              'focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue',
              collapsed ? 'justify-center' : '',
              isActive
                ? 'bg-brand-blue text-white'
                : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
            )}
            title={collapsed ? item.label : undefined}
          >
            {isActive && (
              <motion.div
                layoutId="activeNav"
                className="absolute inset-0 rounded-lg bg-brand-blue"
                transition={{ type: 'spring', stiffness: 350, damping: 30 }}
              />
            )}
            <Icon className={cn('h-4 w-4 flex-shrink-0 relative z-10', isActive ? 'text-white' : 'text-slate-400')} />
            {!collapsed && (
              <span className="relative z-10 flex-1 text-left">{item.label}</span>
            )}
            {!collapsed && item.badge && (
              <span className="relative z-10 inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-2xs font-medium bg-emerald-50 text-emerald-600">
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

    {/* Separator + College section */}
    {!collapsed && (
      <div className="px-3 pb-2 flex-shrink-0">
        <div className="h-px bg-slate-100 mb-3" />
        <p className="text-xs text-slate-400 font-medium mb-2">Select College</p>

        {/* Search */}
        <div className="relative mb-2">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
          <input
            value={search}
            onChange={e => onSearchChange(e.target.value)}
            placeholder="Search..."
            aria-label="Search colleges"
            className="w-full bg-slate-50 text-xs text-slate-700 placeholder-slate-400 pl-8 pr-3 py-2 rounded-lg border border-slate-200 focus:outline-none focus:border-brand-blue focus:ring-1 focus:ring-brand-blue/20 transition"
          />
        </div>
      </div>
    )}

    {/* College list */}
    <div className={cn('flex-1 overflow-y-auto px-2 pb-3 space-y-0.5', collapsed && 'flex flex-col items-center')}>
      <AnimatePresence>
        {filtered.map((college) => {
          const isSelected = selectedCollege?.id === college.id;
          return (
            <motion.button
              key={college.id}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -8 }}
              onClick={() => { onSelectCollege(college); handleNav('chat'); }}
              className={cn(
                'w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-left transition-colors duration-150 group',
                collapsed ? 'w-9 h-9 p-0 justify-center' : '',
                isSelected
                  ? 'bg-blue-50 text-slate-900'
                  : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
              )}
              title={collapsed ? college.name : undefined}
            >
              <span className={cn('text-base flex-shrink-0', collapsed && 'text-lg')}>
                {college.icon}
              </span>
              {!collapsed && (
                <div className="flex-1 min-w-0">
                  <p className={cn('text-xs font-medium truncate', isSelected ? 'text-slate-900' : 'text-slate-600')}>
                    {college.short}
                  </p>
                </div>
              )}
            </motion.button>
          );
        })}
      </AnimatePresence>
    </div>

    {/* Footer */}
    {!collapsed && (
      <div className="px-4 py-3 border-t border-slate-100 flex-shrink-0">
        <p className="text-2xs text-slate-400">{modelName}</p>
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
        transition={{ type: 'spring', stiffness: 350, damping: 30 }}
        className={cn(
          'hidden lg:flex flex-col fixed left-0 top-0 bottom-0 z-50',
          'bg-white border-r border-slate-100 overflow-hidden relative',
        )}
      >
        <SidebarContent {...sidebarContentProps} />
      </motion.aside>

      {/* Mobile trigger */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-4 py-3 bg-white border-b border-slate-100">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-brand-blue flex items-center justify-center">
            <GraduationCap className="h-3.5 w-3.5 text-white" />
          </div>
          <span className="font-display font-semibold text-slate-900 text-sm">CampusAI</span>
        </div>
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="p-1.5 rounded-md text-slate-400 hover:text-slate-600 hover:bg-slate-50 transition"
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
              className="fixed inset-0 bg-black/20 z-40 lg:hidden"
              onClick={() => setMobileOpen(false)}
            />
            <motion.aside
              initial={{ x: -280 }} animate={{ x: 0 }} exit={{ x: -280 }}
              transition={{ type: 'spring', stiffness: 350, damping: 30 }}
              className="fixed left-0 top-0 bottom-0 w-64 z-50 bg-white border-r border-slate-100 lg:hidden overflow-hidden"
            >
              <div className="mt-12">
                <SidebarContent {...sidebarContentProps} />
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
};
