import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  ArrowRight, Sparkles, GraduationCap, BookOpen,
  Shield, Globe, Cpu, Activity, Search, Command,
  FlaskConical, Scale, Stethoscope, Building2, Wheat, ChevronRight,
  Database, Zap, CheckCircle2, MessageSquare, Clock
} from 'lucide-react';
import { DoodleHero } from './ui/doodles/DoodleHero';
import {
  AnimatedCounter, ShimmerButton, Badge, Card, ScrollReveal, ProgressBar, BlueprintStat, spring
} from './ui/Primitives';
import { cn } from '../lib/cn';
import type { College, TabId } from '../types';

interface DashboardTabProps {
  colleges: College[];
  selectedCollege: College | null;
  onSelectCollege: (c: College) => void;
  setActiveTab: (t: TabId) => void;
  modelName: string;
  onQuickQuery?: (query: string) => void;
}

const STATS = [
  { label: 'Colleges Covered', value: 22, suffix: '+', icon: GraduationCap, color: 'text-amber-800', bg: 'bg-amber-100/60', tag: 'Pan-India' },
  { label: 'Academic Rules Indexed', value: 5200, suffix: '+', icon: BookOpen, color: 'text-stone-800', bg: 'bg-stone-200/60', tag: 'FAISS Vector' },
  { label: 'Avg Query Latency', value: 380, suffix: 'ms', icon: Cpu, color: 'text-amber-900', bg: 'bg-amber-200/50', tag: 'FastAPI' },
  { label: 'Student Satisfaction', value: 95, suffix: '%', icon: Activity, color: 'text-emerald-800', bg: 'bg-emerald-100/60', tag: 'Verified' },
];

const SAMPLE_QUERIES = [
  { text: 'What is the minimum attendance required for end-sem exams?', category: 'Academics', icon: '📋' },
  { text: 'How do I apply for a Bonafide Certificate & transcript?', category: 'Procedures', icon: '📜' },
  { text: 'What are the hostel curfew timings and guest policy?', category: 'Facilities', icon: '🏠' },
  { text: 'When are the mid-term assessment examinations scheduled?', category: 'Events', icon: '📅' },
  { text: 'Contact details for Placement Officer & Dean of Academics', category: 'Directory', icon: '👥' },
];

const DISCIPLINES = [
  { label: 'Engineering & Tech', icon: FlaskConical, tag: 'AICTE', desc: 'B.Tech / M.Tech regulations, CGPA conversion, lab safety & credit systems', coverage: 94 },
  { label: 'Medical & Health Sciences', icon: Stethoscope, tag: 'NMC / DCI', desc: 'MBBS / BDS clinical rotations, internship stipends, attendance rules', coverage: 88 },
  { label: 'Law & Governance', icon: Scale, tag: 'BCI', desc: 'BA LLB / LLM moot court requirements, exam pass criteria & attendance', coverage: 85 },
  { label: 'Management & Business', icon: Building2, tag: 'AICTE / UGC', desc: 'MBA / BBA trimester credits, summer internships & placement rules', coverage: 90 },
  { label: 'Arts, Science & Commerce', icon: Globe, tag: 'UGC / CBCS', desc: 'BA / BSc / BCom Choice Based Credit System, elective guidelines', coverage: 92 },
  { label: 'Agriculture & Veterinary', icon: Wheat, tag: 'ICAR', desc: 'BSc Agriculture RAWE practical training, semester credits & rules', coverage: 78 },
];

const AGENT_TOOLS = [
  { name: 'campus_knowledge_search', purpose: 'RAG Vector Search across PDFs & regulations', latency: '<320ms', status: 'Active' },
  { name: 'get_campus_events', purpose: 'Live Academic Calendar & Exam Deadlines', latency: '<40ms', status: 'Active' },
  { name: 'search_contacts', purpose: 'Directory Query for HODs, Deans & Staff', latency: '<30ms', status: 'Active' },
  { name: 'get_facility_info', purpose: 'Hostels, Health Center, Library & WiFi details', latency: '<25ms', status: 'Active' },
  { name: 'get_clubs_activities', purpose: 'Student Societies, Sports & Cultural fests', latency: '<35ms', status: 'Active' },
];

export const DashboardTab: React.FC<DashboardTabProps> = ({
  colleges, selectedCollege, onSelectCollege, setActiveTab, modelName, onQuickQuery
}) => {
  const [hoveredQuery, setHoveredQuery] = useState<string | null>(null);

  const handleQueryClick = (queryText: string) => {
    if (onQuickQuery) {
      onQuickQuery(queryText);
    }
    setActiveTab('chat');
  };

  return (
    <div className="space-y-12 pb-16">

      {/* ── Anti-Slop Hero Section ─────────────────────────────── */}
      <section className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-[#FFFDF9] via-[#FBF8F3] to-[#F5EFE6] border border-[#E8E2D5] p-6 sm:p-10 md:p-12 shadow-sm">
        <DoodleHero />

        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          
          {/* Left Column: Hero Editorial Copy */}
          <div className="lg:col-span-7 space-y-6">
            <motion.div
              initial={{ opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-100/70 border border-amber-300/60 text-amber-900 text-xs font-medium"
            >
              <Sparkles className="h-3.5 w-3.5 text-amber-700" />
              <span>Universal Indian Campus Intelligence</span>
              <span className="text-amber-400">·</span>
              <span className="font-mono text-amber-800">{modelName}</span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ ...spring.crisp, delay: 0.1 }}
              className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold leading-[1.1] tracking-tight text-stone-900"
            >
              Campus rules, <br className="hidden sm:inline" />
              <span className="gradient-text bg-gradient-to-r from-amber-800 via-amber-700 to-stone-800">
                decoded in seconds.
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.2 }}
              className="text-stone-600 text-base sm:text-lg leading-relaxed max-w-xl"
            >
              Instant answers on attendance norms, CGPA formulas, hostel curfews, exam dates, and faculty contacts across all Indian college types.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.3 }}
              className="flex flex-wrap items-center gap-3 pt-2"
            >
              <ShimmerButton size="lg" variant="accent" onClick={() => setActiveTab('chat')}>
                Launch AI Assistant
                <ArrowRight className="h-4 w-4 ml-1 transition-transform group-hover:translate-x-1" />
              </ShimmerButton>
              <ShimmerButton size="lg" variant="ghost" onClick={() => {
                document.getElementById('campus-contexts')?.scrollIntoView({ behavior: 'smooth' });
              }}>
                Explore Campuses
              </ShimmerButton>
            </motion.div>
          </div>

          {/* Right Column: Interactive Query Sandbox Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: 12 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ ...spring.crisp, delay: 0.25 }}
            className="lg:col-span-5 bg-[#FFFDF9] rounded-2xl border border-[#E3D9C6] p-5 shadow-md shadow-stone-900/5 space-y-4"
          >
            <div className="flex items-center justify-between pb-3 border-b border-[#E8E2D5]">
              <div className="flex items-center gap-2">
                <Search className="h-4 w-4 text-amber-700" />
                <span className="text-xs font-semibold uppercase tracking-wider text-stone-700">Try a Live Campus Query</span>
              </div>
              <Badge variant="amber" className="text-2xs">Instant RAG</Badge>
            </div>

            <p className="text-xs text-stone-500">
              Click any question below to test the agent with live domain retrieval:
            </p>

            <div className="space-y-2">
              {SAMPLE_QUERIES.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => handleQueryClick(q.text)}
                  onMouseEnter={() => setHoveredQuery(q.text)}
                  onMouseLeave={() => setHoveredQuery(null)}
                  className="w-full text-left p-3 rounded-xl bg-[#F8F4EC] hover:bg-amber-100/60 border border-[#E8E2D5] hover:border-amber-400/60 transition-all duration-150 group flex items-start gap-2.5"
                >
                  <span className="text-sm flex-shrink-0 mt-0.5">{q.icon}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-stone-800 group-hover:text-amber-900 line-clamp-2 leading-snug">
                      {q.text}
                    </p>
                    <span className="text-2xs text-stone-400 group-hover:text-amber-700">{q.category}</span>
                  </div>
                  <ChevronRight className="h-3.5 w-3.5 text-stone-400 group-hover:text-amber-700 flex-shrink-0 transition-transform group-hover:translate-x-0.5 mt-1" />
                </button>
              ))}
            </div>

            <div className="pt-2 flex items-center justify-between text-2xs text-stone-400 border-t border-[#E8E2D5]">
              <span className="flex items-center gap-1">
                <Zap className="h-3 w-3 text-amber-600" /> FAISS Vector Retrieval
              </span>
              <span>Sub-400ms Response</span>
            </div>
          </motion.div>

        </div>
      </section>

      {/* ── Stat Metrics ─────────────────────────────────── */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {STATS.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <Card key={i} className="p-5 bg-[#FFFDF9] border-[#E8E2D5] hover:border-amber-300 transition-all" hover={false}>
              <div className="flex items-center justify-between mb-3">
                <div className={cn('w-9 h-9 rounded-lg flex items-center justify-center', stat.bg)}>
                  <Icon className={cn('h-5 w-5', stat.color)} />
                </div>
                <BlueprintStat label="" value={stat.tag} />
              </div>
              <div className={cn('text-2xl sm:text-3xl font-bold tracking-tight mb-1 text-stone-900')}>
                <AnimatedCounter to={stat.value} suffix={stat.suffix} duration={1800} />
              </div>
              <p className="text-xs sm:text-sm text-stone-500 font-medium">{stat.label}</p>
            </Card>
          );
        })}
      </section>

      {/* ── Featured Campus Contexts Bento ──────────── */}
      <ScrollReveal>
        <section id="campus-contexts" className="space-y-6">
          <div className="flex items-end justify-between">
            <div>
              <Badge variant="amber" className="mb-2">Pan-India Coverage</Badge>
              <h2 className="font-display text-2xl sm:text-3xl font-semibold text-stone-900 tracking-tight">
                Select Your Campus Context
              </h2>
              <p className="text-sm text-stone-500 mt-1">
                Switching context tailors attendance thresholds, grading curves, and faculty lookup.
              </p>
            </div>
            <BlueprintStat label="INSTITUTIONS" value="22 Active" />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {colleges.slice(0, 6).map((college, i) => (
              <motion.div
                key={college.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ ...spring.crisp, delay: i * 0.05 }}
              >
                <Card
                  className="p-5 group relative overflow-hidden bg-[#FFFDF9] border-[#E8E2D5] hover:border-amber-400 hover:shadow-md transition-all cursor-pointer"
                  onClick={() => { onSelectCollege(college); setActiveTab('chat'); }}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">{college.icon}</span>
                      <div className="min-w-0">
                        <h3 title={college.name} className="font-semibold text-base text-stone-900 group-hover:text-amber-800 transition-colors truncate">
                          {college.short}
                        </h3>
                        <p className="text-xs text-stone-400 truncate">{college.location}</p>
                      </div>
                    </div>
                    <span className="flex h-2.5 w-2.5 relative">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
                      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-600" />
                    </span>
                  </div>

                  <p className="text-xs text-stone-500 mb-4 line-clamp-2 leading-relaxed">
                    {college.name}
                  </p>

                  <div className="flex items-center justify-between pt-3 border-t border-[#E8E2D5]/70">
                    <Badge variant="slate" className="text-2xs font-mono">{college.type.split(' ')[0]}</Badge>
                    <span className="text-xs font-semibold text-amber-800 flex items-center gap-1 group-hover:gap-1.5 transition-all">
                      Ask AI <ChevronRight className="h-3.5 w-3.5" />
                    </span>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Regulatory Academic Coverage ──────────────── */}
      <ScrollReveal>
        <section className="space-y-6">
          <div>
            <Badge variant="amber" className="mb-2">Regulatory Compliance</Badge>
            <h2 className="font-display text-2xl sm:text-3xl font-semibold text-stone-900 tracking-tight">
              Academic Framework Alignment
            </h2>
            <p className="text-sm text-stone-500 mt-1">
              Calibrated against official guidelines from statutory apex regulatory bodies in India.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {DISCIPLINES.map((d, i) => {
              const Icon = d.icon;
              return (
                <Card key={i} className="p-5 bg-[#FFFDF9] border-[#E8E2D5]" hover={false}>
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 rounded-xl bg-amber-100/70 border border-amber-200/80">
                        <Icon className="h-5 w-5 text-amber-800" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-base text-stone-900">{d.label}</h3>
                        <Badge variant="amber" className="text-2xs font-mono">{d.tag}</Badge>
                      </div>
                    </div>
                  </div>
                  <p className="text-xs text-stone-500 mb-4 leading-relaxed">{d.desc}</p>
                  <ProgressBar value={d.coverage} label="Indexed Knowledge" color="from-amber-600 to-amber-700" />
                </Card>
              );
            })}
          </div>
        </section>
      </ScrollReveal>

      {/* ── ReAct Agent Tools Architecture Visualizer ───── */}
      <ScrollReveal>
        <section className="rounded-3xl border border-[#E8E2D5] bg-[#FFFDF9] p-6 sm:p-8 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-[#E8E2D5]">
            <div>
              <Badge variant="amber" className="mb-2">Architecture</Badge>
              <h2 className="font-display text-2xl font-semibold text-stone-900">
                LangGraph Multi-Tool ReAct Agent
              </h2>
              <p className="text-sm text-stone-500 mt-1">
                Autonomous reasoning loop that routes questions to specialized tools in real-time.
              </p>
            </div>
            <BlueprintStat label="LLM MODEL" value={modelName} />
          </div>

          <div className="space-y-3">
            {AGENT_TOOLS.map((t, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-[#F8F4EC] border border-[#E8E2D5] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                <div className="flex items-center gap-3">
                  <div className="w-7 h-7 rounded-lg bg-amber-100/70 border border-amber-300/60 flex items-center justify-center font-mono text-2xs text-amber-900 font-bold">
                    0{idx + 1}
                  </div>
                  <div>
                    <p className="font-mono font-semibold text-stone-900">{t.name}</p>
                    <p className="text-stone-500">{t.purpose}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="font-mono text-amber-800 bg-amber-100/50 px-2 py-0.5 rounded text-2xs">{t.latency}</span>
                  <span className="inline-flex items-center gap-1 text-emerald-700 font-medium">
                    <CheckCircle2 className="h-3.5 w-3.5" /> {t.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Ready CTA ──────────────────────────────────── */}
      <ScrollReveal>
        <section className="rounded-2xl border border-[#E3D9C6] bg-gradient-to-r from-[#F5EFE6] via-[#F8F4EC] to-[#F5EFE6] p-8 text-center space-y-4">
          <h3 className="font-display text-2xl sm:text-3xl font-semibold text-stone-900">
            Have a question about your campus?
          </h3>
          <p className="text-stone-600 text-sm max-w-md mx-auto">
            Get instant, policy-verified answers for attendance, exams, hostels, and contacts.
          </p>
          <div className="pt-2">
            <ShimmerButton size="lg" variant="accent" onClick={() => setActiveTab('chat')}>
              Launch AI Chatbot <ArrowRight className="h-4 w-4 ml-1" />
            </ShimmerButton>
          </div>
        </section>
      </ScrollReveal>

    </div>
  );
};

