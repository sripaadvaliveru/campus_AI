import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TopNav } from './components/TopNav';
import { DashboardTab } from './components/DashboardTab';
import { ChatTab } from './components/ChatTab';
import { EventsTab } from './components/EventsTab';
import { DirectoryTab } from './components/DirectoryTab';
import { AnalyticsTab } from './components/AnalyticsTab';
import type { College, Message, Event, Contact, AnalyticsData, TabId } from './types';

// Base URL: set VITE_API_URL for production, otherwise use the dev proxy (/api -> localhost:8000).
const API = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '');

const SECTION_CSS: Record<TabId, string> = {
  dashboard: 'var(--dashboard)',
  chat: 'var(--chat)',
  events: 'var(--events)',
  directory: 'var(--directory)',
  analytics: 'var(--analytics)',
};

const FALLBACK_COLLEGES: College[] = [
  { id: 'general', name: 'General (All Indian Colleges)', short: 'General', icon: '🇮🇳', type: 'Universal Guidelines', location: 'Pan-India', color: '#4f8ef7' },
  { id: 'iith', name: 'IIT Hyderabad (IITH)', short: 'IITH', icon: '🔬', type: 'Central Government Institute', location: 'Kandi, Hyderabad', color: '#f0883e' },
  { id: 'iiith', name: 'IIIT Hyderabad (IIITH)', short: 'IIITH', icon: '💻', type: 'Autonomous Deemed University (PPP)', location: 'Gachibowli, Hyderabad', color: '#39c5b9' },
  { id: 'nalsar', name: 'NALSAR University of Law', short: 'NALSAR', icon: '⚖️', type: 'National Law University', location: 'Hyderabad', color: '#7c5cbf' },
  { id: 'nims', name: "NIMS — Nizam's Institute of Medical Sciences", short: 'NIMS', icon: '🏥', type: 'Autonomous Medical University', location: 'Hyderabad', color: '#3fb950' },
  { id: 'hcu', name: 'University of Hyderabad (HCU)', short: 'HCU', icon: '🎓', type: 'Central University', location: 'Gachibowli, Hyderabad', color: '#d29922' },
  { id: 'osmania', name: 'Osmania University', short: 'OU', icon: '📜', type: 'State University', location: 'Hyderabad', color: '#e3b341' },
  { id: 'bits_hyd', name: 'BITS Pilani — Hyderabad Campus', short: 'BITS Hyd', icon: '🏛️', type: 'Private Deemed University', location: 'Shameerpet, Hyderabad', color: '#58a6ff' },
  { id: 'isb_hyd', name: 'Indian School of Business (ISB) Hyderabad', short: 'ISB Hyd', icon: '💼', type: 'Private Business School', location: 'Gachibowli, Hyderabad', color: '#7c5cbf' },
  { id: 'imt_hyd', name: 'IMT Hyderabad', short: 'IMT Hyd', icon: '📈', type: 'Private Business School', location: 'Shamshabad, Hyderabad', color: '#f0883e' },
  { id: 'ibs_hyd', name: 'ICFAI Business School (IBS) Hyderabad', short: 'IBS Hyd', icon: '📊', type: 'Private Business School', location: 'Donthanapally, Hyderabad', color: '#39c5b9' },
  { id: 'omc', name: 'Osmania Medical College (OMC)', short: 'OMC', icon: '🩺', type: 'Government Medical College', location: 'Koti, Hyderabad', color: '#3fb950' },
  { id: 'nizam', name: 'Nizam College Hyderabad', short: 'Nizam', icon: '🏛️', type: 'Constituent College of Osmania University', location: 'Basheerbagh, Hyderabad', color: '#d29922' },
  { id: 'st_francis', name: 'St. Francis College for Women', short: 'St. Francis', icon: '👩‍🎓', type: 'Autonomous Minority College', location: 'Begumpet, Hyderabad', color: '#4f8ef7' },
  { id: 'jntuh', name: 'JNTU Hyderabad (JNTUH)', short: 'JNTUH', icon: '⚙️', type: 'State University', location: 'Kukatpally, Hyderabad', color: '#e3b341' },
  { id: 'cbit', name: 'Chaitanya Bharathi Institute of Technology (CBIT)', short: 'CBIT', icon: '🏫', type: 'Autonomous Private Institute', location: 'Gandipet, Hyderabad', color: '#4f8ef7' },
  { id: 'griet', name: 'Gokaraju Rangaraju Institute (GRIET)', short: 'GRIET', icon: '📐', type: 'Autonomous Private Institute', location: 'Bachupally, Hyderabad', color: '#f0883e' },
  { id: 'vnr_vjiet', name: 'VNR VJIET', short: 'VNR VJIET', icon: '🧪', type: 'Autonomous Private Institute', location: 'Bachupally, Hyderabad', color: '#39c5b9' },
  { id: 'vardhaman', name: 'Vardhaman College of Engineering', short: 'Vardhaman', icon: '🔬', type: 'Autonomous Private Institute', location: 'Shamshabad, Hyderabad', color: '#3fb950' },
  { id: 'anurag', name: 'Anurag University', short: 'Anurag', icon: '🛰️', type: 'Private University', location: 'Venkatapur, Hyderabad', color: '#7c5cbf' },
  { id: 'iare', name: 'Institute of Aeronautical Engineering (IARE)', short: 'IARE', icon: '✈️', type: 'Autonomous Private Institute', location: 'Dundigal, Hyderabad', color: '#58a6ff' },
];

const FALLBACK_EVENTS: Event[] = [
  { date: '2026-07-20', event: 'Registration & Course Enrollment Opens', category: 'academic', semester: 'Odd Semester 2026', description: 'Mandatory course registration for all students on the academic ERP portal.' },
  { date: '2026-08-03', event: 'Commencement of Classwork', category: 'academic', semester: 'Odd Semester 2026', description: 'Classes begin for all engineering, medical and arts batches.' },
  { date: '2026-09-15', event: 'Mid-Term Assessment Examinations', category: 'exam', semester: 'Odd Semester 2026', description: 'Internal assessments carrying 30% weightage of final CGPA calculation.' },
  { date: '2026-10-02', event: 'Gandhi Jayanti National Holiday', category: 'holiday', semester: 'Odd Semester 2026', description: 'All teaching facilities remain closed.' },
  { date: '2026-10-24', event: 'Tarangini Cultural Fest & Sports Meet', category: 'cultural', semester: 'Odd Semester 2026', description: 'Annual multi-discipline college fest with guest music bands and track events.' },
  { date: '2026-11-10', event: 'Campus Placement Drives', category: 'placement', semester: 'Odd Semester 2026', description: 'Recruitment by top-tier tech, consulting, and analytics firms.' },
];

const FALLBACK_CONTACTS: Contact[] = [
  { name: 'Dr. Sandeep Kumar', designation: 'Professor & Head', department: 'Computer Science', email: 'sandeep@college.edu', phone: '+91 98480 22311', specialization: 'Machine Learning & Distributed Systems', cabin: 'Block B – Room 302' },
  { name: 'Prof. Anitha Murthy', designation: 'Dean Academics', department: 'Administration', email: 'dean.acad@college.edu', phone: '+91 40 2301 6002', specialization: 'Curriculum Design & UGC Compliance', cabin: 'Admin Block – Room 101' },
  { name: 'Dr. V. Srinivas', designation: 'Associate Professor', department: 'Mechanical Engineering', email: 'srinivas.m@college.edu', phone: '+91 94401 55621', specialization: 'Robotics & Finite Element Analysis', cabin: 'Workshop Wing – Cabin 4' },
  { name: 'Dr. Shalini Reddy', designation: 'Medical Officer', department: 'Health Center', email: 'dr.reddy@college.edu', phone: '+91 40 2301 6112', specialization: 'General Medicine & Trauma Care', cabin: 'Campus Clinic' },
  { name: 'Mr. Rajendra Prasad', designation: 'Placement Coordinator', department: 'Placement Cell', email: 'placements@college.edu', phone: '+91 90001 88472', specialization: 'Corporate Relations & Internships', cabin: 'Placement Wing – Room 2' },
];

const FALLBACK_ANALYTICS: AnalyticsData = {
  summary: {
    total_queries: 142, today_queries: 12, positive_feedback: 38, negative_feedback: 4,
    satisfaction_rate: 90.5,
    top_categories: [
      { category: 'academics', count: 54 }, { category: 'facilities', count: 32 },
      { category: 'events', count: 28 }, { category: 'contacts', count: 18 }, { category: 'admissions', count: 10 },
    ],
    daily_counts: [
      { day: '2026-07-06', count: 15 }, { day: '2026-07-07', count: 22 }, { day: '2026-07-08', count: 18 },
      { day: '2026-07-09', count: 25 }, { day: '2026-07-10', count: 30 }, { day: '2026-07-11', count: 20 }, { day: '2026-07-12', count: 12 },
    ],
    avg_response_time_ms: 380,
  },
  popular_queries: [
    { user_query: 'passing marks for exams', frequency: 24 }, { user_query: 'hostel wifi timings', frequency: 18 },
    { user_query: 'HOD contact details', frequency: 14 }, { user_query: 'bonafide certificate process', frequency: 11 },
    { user_query: 'placement rules for final year', frequency: 9 },
  ],
  recent_queries: [
    { id: 1, user_query: 'What is the passing marks?', bot_response: '', category: 'academics', timestamp: new Date().toISOString(), response_time_ms: 320 },
    { id: 2, user_query: 'Where is the clinic?', bot_response: '', category: 'facilities', timestamp: new Date().toISOString(), response_time_ms: 410 },
  ],
  timestamp: new Date().toISOString(),
};

async function apiFetch<T>(path: string, fallback: T): Promise<T> {
  try {
    const r = await fetch(`${API}${path}`);
    if (!r.ok) {
      console.warn(`API ${path} returned ${r.status}`);
      return fallback;
    }
    return await r.json();
  } catch (e) {
    console.warn(`API ${path} unreachable:`, e);
    return fallback;
  }
}

export const App: React.FC = () => {
  const [colleges, setColleges] = useState<College[]>(FALLBACK_COLLEGES);
  const [selected, setSelected] = useState<College | null>(FALLBACK_COLLEGES[0]);
  const [tab, setTab] = useState<TabId>('dashboard');
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [events, setEvents] = useState<Event[]>([]);
  const [eventsLoading, setEventsLoading] = useState(false);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [contactsLoading, setContactsLoading] = useState(false);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [modelName, setModelName] = useState('GPT-4o mini');
  const [sessionId] = useState(() => `s_${Math.random().toString(36).slice(2)}`);

  // Dynamic document title
  useEffect(() => {
    if (selected && selected.id !== 'general') {
      document.title = `${selected.short} — CampusAI`;
    } else {
      document.title = `CampusAI — Universal Campus Intelligence`;
    }
  }, [selected, tab]);

  // Update section accent CSS variable when tab changes
  useEffect(() => {
    document.documentElement.style.setProperty('--section-accent', SECTION_CSS[tab]);
  }, [tab]);

  // Load colleges
  useEffect(() => {
    apiFetch<{ colleges: College[] }>('/colleges', { colleges: FALLBACK_COLLEGES })
      .then(data => {
        if (data.colleges?.length) { setColleges(data.colleges); setSelected(data.colleges[0]); }
      });
    apiFetch<{ provider: string; model: string }>('/health', { provider: 'openai', model: 'GPT-4o mini' })
      .then(data => {
        if (data.model) setModelName(data.model);
      });
  }, []);

  // Load tab-specific data (re-fetches when college changes)
  useEffect(() => {
    if (tab === 'events') {
      setEventsLoading(true);
      const params = new URLSearchParams();
      if (selected?.id && selected.id !== 'general') params.set('college_id', selected.id);
      const qs = params.toString();
      apiFetch<{ events: Event[] }>(`/events${qs ? `?${qs}` : ''}`, { events: FALLBACK_EVENTS })
        .then(d => setEvents(d.events || FALLBACK_EVENTS))
        .finally(() => setEventsLoading(false));
    }
    if (tab === 'directory') {
      setContactsLoading(true);
      const params = new URLSearchParams();
      if (selected?.id && selected.id !== 'general') params.set('college_id', selected.id);
      const qs = params.toString();
      apiFetch<{ contacts: Contact[] }>(`/contacts${qs ? `?${qs}` : ''}`, { contacts: FALLBACK_CONTACTS })
        .then(d => setContacts(d.contacts || FALLBACK_CONTACTS))
        .finally(() => setContactsLoading(false));
    }
    if (tab === 'analytics' && !analytics) {
      setAnalyticsLoading(true);
      apiFetch<AnalyticsData>('/analytics', FALLBACK_ANALYTICS)
        .then(d => setAnalytics(d || FALLBACK_ANALYTICS))
        .finally(() => setAnalyticsLoading(false));
    }
  }, [tab, selected?.id]);

  const handleSend = async (text: string) => {
    const userMsg: Message = {
      id: `u_${Date.now()}`, role: 'user', content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages(prev => [...prev, userMsg]);
    setChatLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, college_id: selected?.id || 'general', session_id: sessionId }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      const data = await res.json();
      const content = typeof data?.response === 'string' && data.response.trim()
        ? data.response
        : '⚠️ The assistant returned an empty response. Please try again.';
      setMessages(prev => [...prev, {
        id: `b_${Date.now()}`, role: 'assistant', content,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        toolUsed: data.tool_used, responseTimeMs: data.response_time_ms,
      }]);
    } catch {
      setMessages(prev => [...prev, {
        id: `b_${Date.now()}`, role: 'assistant',
        content: `⚠️ Demo Mode — Backend not reachable.\n\nStart the backend:\n  uvicorn backend.main:app --reload --port 8000\n\nFor demo: passing marks are 40% theory, 75% attendance is mandatory for all exams.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        toolUsed: 'offline_cache', responseTimeMs: 85,
      }]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleFeedback = (id: string, rating: 1 | -1) => {
    fetch(`${API}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message_id: id, rating, session_id: sessionId }),
    }).catch(() => {});
  };

  const tabVariants = {
    initial: { opacity: 0, y: 8 },
    animate: { opacity: 1, y: 0, transition: { duration: 0.35, ease: 'easeOut' as const } },
    exit: { opacity: 0, y: -8, transition: { duration: 0.2 } },
  };

  const renderTab = () => {
    switch (tab) {
      case 'dashboard':
        return <DashboardTab colleges={colleges} selectedCollege={selected} onSelectCollege={setSelected} setActiveTab={setTab} modelName={modelName} onQuickQuery={handleSend} />;
      case 'chat':
        return <ChatTab selectedCollege={selected} messages={messages} onSendMessage={handleSend} onClearHistory={() => setMessages([])} onSendFeedback={handleFeedback} loading={chatLoading} />;
      case 'events':
        return <EventsTab events={events} loading={eventsLoading} />;
      case 'directory':
        return <DirectoryTab contacts={contacts} loading={contactsLoading} />;
      case 'analytics':
        return <AnalyticsTab analyticsData={analytics} loading={analyticsLoading} modelName={modelName} />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-background bg-noise bg-section-grid">
      <TopNav
        colleges={colleges}
        selectedCollege={selected}
        onSelectCollege={setSelected}
        activeTab={tab}
        setActiveTab={setTab}
        modelName={modelName}
      />

      {/* Main content */}
      <main className="pt-16 min-h-screen flex flex-col relative z-10">
        <div className={`flex-1 overflow-y-auto ${tab === 'chat' ? '' : 'px-4 md:px-6 lg:px-8 py-6 lg:py-8'}`}>
          <AnimatePresence mode="wait">
            <motion.div
              key={tab}
              variants={tabVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              className={tab === 'chat' ? 'h-full' : 'max-w-6xl mx-auto'}
            >
              {renderTab()}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
};
