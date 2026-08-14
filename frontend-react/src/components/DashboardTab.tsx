import React from 'react';
import { motion } from 'framer-motion';
import {
  ArrowRight, Sparkles, GraduationCap, BookOpen,
  Zap, Shield, Globe, Cpu, ChevronRight, Activity,
  FlaskConical, Scale, Stethoscope, Building2, Wheat
} from 'lucide-react';
import { DoodleBanner } from './ui/DoodleBanner';
import {
  Typewriter, AnimatedCounter,
  ShimmerButton, Badge, Card, ScrollReveal, ProgressBar
} from './ui/Primitives';
import { cn } from '../lib/cn';
import type { College, TabId } from '../types';

interface DashboardTabProps {
  colleges: College[];
  selectedCollege: College | null;
  onSelectCollege: (c: College) => void;
  setActiveTab: (t: TabId) => void;
  modelName: string;
}

const STATS = [
  { label: 'Colleges', value: 22, suffix: '+', icon: GraduationCap, color: 'text-blue-600', bg: 'bg-blue-50' },
  { label: 'Query Topics', value: 150, suffix: '+', icon: BookOpen, color: 'text-purple-600', bg: 'bg-purple-50' },
  { label: 'RAG Docs', value: 5000, suffix: '+', icon: Cpu, color: 'text-cyan-600', bg: 'bg-cyan-50' },
  { label: 'Satisfaction', value: 95, suffix: '%', icon: Activity, color: 'text-emerald-600', bg: 'bg-emerald-50' },
];

const DISCIPLINES = [
  { label: 'Engineering', icon: FlaskConical, color: 'from-blue-500 to-indigo-500', desc: 'B.Tech/BE · AICTE · JEE/State CETs', coverage: 82 },
  { label: 'Medical Sciences', icon: Stethoscope, color: 'from-emerald-500 to-teal-500', desc: 'MBBS/BDS · NMC/DCI · NEET', coverage: 76 },
  { label: 'Law & Justice', icon: Scale, color: 'from-amber-500 to-orange-500', desc: 'LLB/LLM · BCI · CLAT/AILET', coverage: 71 },
  { label: 'Management', icon: Building2, color: 'from-purple-500 to-pink-500', desc: 'MBA/BBA · AICTE · CAT/MAT', coverage: 68 },
  { label: 'Arts & Sciences', icon: Globe, color: 'from-rose-500 to-red-500', desc: 'BA/BSc/BCom · UGC/CBCS · CUET', coverage: 88 },
  { label: 'Agriculture', icon: Wheat, color: 'from-lime-500 to-green-500', desc: 'BSc Agri · ICAR · ICAR AIEEA', coverage: 60 },
];

const getFeatures = (modelName: string) => [
  {
    icon: Cpu, title: 'LangGraph ReAct Agent',
    desc: 'Powered by a multi-step reasoning agent that autonomously selects from 5 domain tools — context-aware, real-time.',
    badge: 'Core Engine', badgeVariant: 'blue' as const
  },
  {
    icon: Shield, title: 'FAISS Semantic Search',
    desc: 'Dense vector embeddings from sentence-transformers enable precise sub-second retrieval across campus handbooks.',
    badge: 'RAG', badgeVariant: 'purple' as const
  },
  {
    icon: Zap, title: modelName,
    desc: 'Ultra-fast, token-efficient responses calibrated for Indian academic terminology.',
    badge: 'LLM', badgeVariant: 'amber' as const
  },
  {
    icon: Globe, title: 'Universal Coverage',
    desc: 'Works for ALL Indian college types — Engineering, Medical, Law, Architecture, Agriculture, Pharmacy & more.',
    badge: 'Pan-India', badgeVariant: 'green' as const
  },
];

const staggerContainer = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: 'easeOut' as const } },
};

export const DashboardTab: React.FC<DashboardTabProps> = ({
  colleges, onSelectCollege, setActiveTab, modelName,
}) => {
  return (
    <div className="space-y-16 pb-16">

      {/* ── Hero Section ─────────────────────────────── */}
      <section className="relative min-h-[480px] flex items-center">
        {/* Doodle background */}
        <div className="absolute inset-0 rounded-3xl overflow-hidden">
          <DoodleBanner />
        </div>

        <div className="relative z-10 max-w-4xl pt-12 pb-8 px-4 md:px-0">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-6 inline-block"
          >
            <Badge variant="blue" dot pulse>
              Powered by {modelName} · LangChain · FAISS
            </Badge>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="font-display text-4xl md:text-6xl font-black text-slate-900 leading-[1.08] tracking-tight mb-4"
          >
            Your <span className="text-brand-blue">AI</span> Campus
            <br />
            <span className="text-slate-700">
              <Typewriter
                words={['Assistant', 'Advisor', 'Navigator', 'Directory', 'Calendar']}
                speed={90}
              />
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.25 }}
            className="text-slate-500 text-base md:text-lg leading-relaxed max-w-2xl mb-8"
          >
            Universal campus information intelligence for all Indian college types — from IITs to medical colleges.
            Ask in natural language about regulations, events, contacts, and campus life.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex flex-wrap gap-3"
          >
            <ShimmerButton size="lg" onClick={() => setActiveTab('chat')}>
              <Sparkles className="h-4 w-4" />
              Start AI Chat
              <ArrowRight className="h-4 w-4" />
            </ShimmerButton>
            <ShimmerButton size="lg" variant="secondary" onClick={() => setActiveTab('events')}>
              <span>Explore Events</span>
            </ShimmerButton>
          </motion.div>
        </div>
      </section>

      {/* ── Stats Row ─────────────────────────────────── */}
      <motion.section
        variants={staggerContainer}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: '-60px' }}
        className="grid grid-cols-2 lg:grid-cols-4 gap-4"
      >
        {STATS.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div key={i} variants={fadeUp}>
              <Card className="p-5" hover={false}>
                <div className={cn('w-10 h-10 rounded-xl mb-3 flex items-center justify-center', stat.bg)}>
                  <Icon className={cn('h-5 w-5', stat.color)} />
                </div>
                <div className={cn('text-2xl font-black mb-1', stat.color)}>
                  <AnimatedCounter to={stat.value} suffix={stat.suffix} duration={1800} />
                </div>
                <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">{stat.label}</p>
              </Card>
            </motion.div>
          );
        })}
      </motion.section>

      {/* ── Featured Colleges ─────────────────────────── */}
      <ScrollReveal>
        <section id="all-colleges" className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-display text-xl font-bold text-slate-900 tracking-tight">Campus Contexts</h2>
              <p className="text-xs text-slate-500 mt-0.5">Select a college to focus your AI responses</p>
            </div>
            <ShimmerButton variant="ghost" size="sm" onClick={() => {
              const el = document.getElementById('all-colleges');
              el?.scrollIntoView({ behavior: 'smooth' });
            }}>
              View all <ChevronRight className="h-3.5 w-3.5" />
            </ShimmerButton>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {colleges.slice(0, 6).map((college, i) => (
              <ScrollReveal key={college.id} delay={i * 60} direction="up">
                <Card
                  className="p-5 group border-l-4 border-l-transparent hover:border-l-brand-blue"
                  onClick={() => { onSelectCollege(college); setActiveTab('chat'); }}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="text-2xl p-2.5 bg-slate-50 rounded-xl group-hover:scale-110 transition-transform duration-300">
                      {college.icon}
                    </div>
                    <Badge variant="slate" className="text-2xs">
                      {college.type.split(' ')[0]}
                    </Badge>
                  </div>
                  <h3 title={college.name} className="font-semibold text-slate-900 text-sm group-hover:text-brand-blue transition-colors truncate mb-1">
                    {college.name}
                  </h3>
                  <p className="text-2xs text-slate-500 mb-3 truncate">{college.location}</p>
                  <div className="flex items-center gap-1.5 text-2xs font-semibold text-brand-blue group-hover:gap-2.5 transition-all duration-200">
                    <span>Ask about {college.short}</span>
                    <ChevronRight className="h-3 w-3" />
                  </div>
                </Card>
              </ScrollReveal>
            ))}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Disciplines Coverage ──────────────────────── */}
      <ScrollReveal>
        <section className="space-y-6">
          <div>
            <h2 className="font-display text-xl font-bold text-slate-900 tracking-tight">Academic Discipline Coverage</h2>
            <p className="text-xs text-slate-500 mt-0.5">Knowledge depth across Indian college regulatory domains</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {DISCIPLINES.map((d, i) => {
              const Icon = d.icon;
              return (
                <ScrollReveal key={i} delay={i * 50}>
                  <Card className="p-5 relative overflow-hidden" hover={false}>
                    <div className={cn('absolute top-0 left-0 w-1 h-full rounded-l-2xl bg-gradient-to-b', d.color)} />
                    <div className="pl-4 space-y-3">
                      <div className="flex items-center gap-2.5">
                        <div className={cn('p-2 rounded-lg bg-gradient-to-br', d.color, 'bg-opacity-10')}>
                          <Icon className="h-4 w-4 text-white" />
                        </div>
                        <div>
                          <p className="font-semibold text-sm text-slate-900">{d.label}</p>
                          <p className="text-2xs text-slate-500">{d.desc}</p>
                        </div>
                      </div>
                      <ProgressBar value={d.coverage} label="knowledge coverage" color={`${d.color}`} />
                    </div>
                  </Card>
                </ScrollReveal>
              );
            })}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Features ─────────────────────────────────── */}
      <ScrollReveal>
        <section className="space-y-6">
          <h2 className="font-display text-xl font-bold text-slate-900 tracking-tight">Technology Stack</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {getFeatures(modelName).map((f, i) => {
              const Icon = f.icon;
              return (
                <ScrollReveal key={i} delay={i * 80}>
                  <Card className="p-6 group" hover={false}>
                    <div className="flex items-start gap-4">
                      <div className="p-3 bg-blue-50 rounded-xl flex-shrink-0">
                        <Icon className="h-5 w-5 text-brand-blue" />
                      </div>
                      <div className="space-y-2 flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <p className="font-semibold text-sm text-slate-900">{f.title}</p>
                          <Badge variant={f.badgeVariant} className="ml-auto">{f.badge}</Badge>
                        </div>
                        <p className="text-xs text-slate-500 leading-relaxed">{f.desc}</p>
                      </div>
                    </div>
                  </Card>
                </ScrollReveal>
              );
            })}
          </div>
        </section>
      </ScrollReveal>

      {/* ── CTA Banner ───────────────────────────────── */}
      <ScrollReveal>
        <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-50 via-white to-blue-50 border border-blue-100">
          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6 p-8 md:p-10">
            <div className="space-y-2 text-center md:text-left">
              <h3 className="font-display text-2xl font-bold text-slate-900">Ready to ask about your campus?</h3>
              <p className="text-slate-500 text-sm">Select a college context from the sidebar, then start your AI conversation.</p>
            </div>
            <ShimmerButton size="lg" onClick={() => setActiveTab('chat')} className="flex-shrink-0">
              <Sparkles className="h-4 w-4" />
              Open AI Chat
              <ArrowRight className="h-4 w-4" />
            </ShimmerButton>
          </div>
        </section>
      </ScrollReveal>
    </div>
  );
};
