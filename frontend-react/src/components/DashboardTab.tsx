import React from 'react';
import { motion } from 'framer-motion';
import {
  ArrowRight, Sparkles, GraduationCap, BookOpen,
  Zap, Shield, Globe, Cpu, ChevronRight, Activity,
  FlaskConical, Scale, Stethoscope, Building2, Wheat
} from 'lucide-react';
import { ParticleField } from './ui/ParticleField';
import {
  Typewriter, AnimatedCounter, GlowingOrb, MagneticCard,
  ShimmerButton, Badge, GlassCard, ScrollReveal, ProgressBar
} from './ui/Primitives';
import { cn } from '../lib/cn';
import type { College, TabId } from '../types';

interface DashboardTabProps {
  colleges: College[];
  selectedCollege: College | null;
  onSelectCollege: (c: College) => void;
  setActiveTab: (t: TabId) => void;
}

const STATS = [
  { label: 'Colleges', value: 21, suffix: '+', icon: GraduationCap, color: 'text-blue-400', bg: 'from-blue-500/10 to-blue-600/5', border: 'border-blue-500/15' },
  { label: 'Query Topics', value: 150, suffix: '+', icon: BookOpen, color: 'text-purple-400', bg: 'from-purple-500/10 to-purple-600/5', border: 'border-purple-500/15' },
  { label: 'RAG Docs', value: 5000, suffix: '+', icon: Cpu, color: 'text-cyan-400', bg: 'from-cyan-500/10 to-cyan-600/5', border: 'border-cyan-500/15' },
  { label: 'Satisfaction', value: 95, suffix: '%', icon: Activity, color: 'text-emerald-400', bg: 'from-emerald-500/10 to-emerald-600/5', border: 'border-emerald-500/15' },
];

const DISCIPLINES = [
  { label: 'Engineering', icon: FlaskConical, color: 'from-blue-500 to-indigo-500', desc: 'B.Tech/BE · AICTE · JEE/State CETs', coverage: 82 },
  { label: 'Medical Sciences', icon: Stethoscope, color: 'from-emerald-500 to-teal-500', desc: 'MBBS/BDS · NMC/DCI · NEET', coverage: 76 },
  { label: 'Law & Justice', icon: Scale, color: 'from-amber-500 to-orange-500', desc: 'LLB/LLM · BCI · CLAT/AILET', coverage: 71 },
  { label: 'Management', icon: Building2, color: 'from-purple-500 to-pink-500', desc: 'MBA/BBA · AICTE · CAT/MAT', coverage: 68 },
  { label: 'Arts & Sciences', icon: Globe, color: 'from-rose-500 to-red-500', desc: 'BA/BSc/BCom · UGC/CBCS · CUET', coverage: 88 },
  { label: 'Agriculture', icon: Wheat, color: 'from-lime-500 to-green-500', desc: 'BSc Agri · ICAR · ICAR AIEEA', coverage: 60 },
];

const FEATURES = [
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
    icon: Zap, title: 'GPT-4o mini',
    desc: 'Ultra-fast, token-efficient responses via OpenAI\'s efficient model — calibrated for Indian academic terminology.',
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
  colleges, onSelectCollege, setActiveTab,
}) => {
  return (
    <div className="space-y-16 pb-16">

      {/* ── Hero Section ─────────────────────────────── */}
      <section className="relative min-h-[420px] flex items-center">
        {/* Particle background */}
        <div className="absolute inset-0 rounded-3xl overflow-hidden">
          <ParticleField className="opacity-60" particleCount={50} />
          <GlowingOrb color="#3b82f6" size={500} intensity={0.08} className="top-[-100px] right-[10%]" />
          <GlowingOrb color="#8b5cf6" size={400} intensity={0.07} className="bottom-[-80px] left-[5%]" />
          {/* Grid overlay */}
          <div className="absolute inset-0 bg-grid" style={{ backgroundSize: '64px 64px' }} />
          {/* Radial fade */}
          <div className="absolute inset-0 bg-gradient-radial from-transparent via-transparent to-slate-950/80" />
        </div>

        <div className="relative z-10 max-w-4xl pt-10">
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-6 inline-block"
          >
            <Badge variant="blue" dot pulse>
              Powered by GPT-4o mini · LangChain · FAISS
            </Badge>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="font-display text-4xl md:text-6xl font-black text-white leading-[1.08] tracking-tight mb-4"
          >
            Your AI Campus
            <br />
            <span className="gradient-text">
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
            className="text-slate-400 text-base md:text-lg leading-relaxed max-w-2xl mb-8"
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
              <GlassCard className={cn('p-5 border', stat.border)} hover={false}>
                <div className={cn('w-10 h-10 rounded-xl mb-3 flex items-center justify-center bg-gradient-to-br', stat.bg, 'border', stat.border)}>
                  <Icon className={cn('h-5 w-5', stat.color)} />
                </div>
                <div className={cn('text-2xl font-black mb-1', stat.color)}>
                  <AnimatedCounter to={stat.value} suffix={stat.suffix} duration={1800} />
                </div>
                <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">{stat.label}</p>
              </GlassCard>
            </motion.div>
          );
        })}
      </motion.section>

      {/* ── Featured Colleges ─────────────────────────── */}
      <ScrollReveal>
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-display text-xl font-bold text-white tracking-tight">Campus Contexts</h2>
              <p className="text-xs text-slate-500 mt-0.5">Select a college to focus your AI responses</p>
            </div>
            <ShimmerButton variant="ghost" size="sm" onClick={() => setActiveTab('chat')}>
              View all <ChevronRight className="h-3.5 w-3.5" />
            </ShimmerButton>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {colleges.slice(0, 6).map((college, i) => (
              <ScrollReveal key={college.id} delay={i * 60} direction="up">
                <MagneticCard>
                  <GlassCard
                    glow="blue"
                    className="p-5 group"
                    onClick={() => { onSelectCollege(college); setActiveTab('chat'); }}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="text-2xl p-2.5 bg-slate-800/60 rounded-xl border border-white/5 group-hover:scale-110 transition-transform duration-300">
                        {college.icon}
                      </div>
                      <Badge variant="slate" className="text-2xs">
                        {college.type.split(' ')[0]}
                      </Badge>
                    </div>
                    <h3 className="font-semibold text-slate-200 text-sm group-hover:text-white transition-colors truncate mb-1">
                      {college.name}
                    </h3>
                    <p className="text-2xs text-slate-500 mb-3 truncate">{college.location}</p>
                    <div className="flex items-center gap-1.5 text-2xs font-semibold text-blue-400 group-hover:gap-2.5 transition-all duration-200">
                      <span>Ask about {college.short}</span>
                      <ChevronRight className="h-3 w-3" />
                    </div>

                    {/* Subtle color accent line */}
                    <div
                      className="absolute bottom-0 left-0 right-0 h-0.5 rounded-b-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                      style={{ background: `linear-gradient(to right, transparent, ${college.color}, transparent)` }}
                    />
                  </GlassCard>
                </MagneticCard>
              </ScrollReveal>
            ))}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Disciplines Coverage ──────────────────────── */}
      <ScrollReveal>
        <section className="space-y-6">
          <div>
            <h2 className="font-display text-xl font-bold text-white tracking-tight">Academic Discipline Coverage</h2>
            <p className="text-xs text-slate-500 mt-0.5">Knowledge depth across Indian college regulatory domains</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {DISCIPLINES.map((d, i) => {
              const Icon = d.icon;
              return (
                <ScrollReveal key={i} delay={i * 50}>
                  <GlassCard className="p-5 relative overflow-hidden" hover={false}>
                    <div className={cn('absolute top-0 left-0 w-1 h-full rounded-l-2xl bg-gradient-to-b', d.color)} />
                    <div className="pl-4 space-y-3">
                      <div className="flex items-center gap-2.5">
                        <div className={cn('p-2 rounded-lg bg-gradient-to-br', d.color, 'bg-opacity-10')}>
                          <Icon className="h-4 w-4 text-white" />
                        </div>
                        <div>
                          <p className="font-semibold text-sm text-white">{d.label}</p>
                          <p className="text-2xs text-slate-500">{d.desc}</p>
                        </div>
                      </div>
                      <ProgressBar value={d.coverage} label="knowledge coverage" color={`${d.color}`} />
                    </div>
                  </GlassCard>
                </ScrollReveal>
              );
            })}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Features ─────────────────────────────────── */}
      <ScrollReveal>
        <section className="space-y-6">
          <h2 className="font-display text-xl font-bold text-white tracking-tight">Technology Stack</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {FEATURES.map((f, i) => {
              const Icon = f.icon;
              return (
                <ScrollReveal key={i} delay={i * 80}>
                  <GlassCard className="p-6 group shine" hover={false}>
                    <div className="flex items-start gap-4">
                      <div className="p-3 bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl border border-white/5 group-hover:border-blue-500/20 transition-colors flex-shrink-0">
                        <Icon className="h-5 w-5 text-blue-400" />
                      </div>
                      <div className="space-y-2 flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <p className="font-semibold text-sm text-white">{f.title}</p>
                          <Badge variant={f.badgeVariant} className="ml-auto">{f.badge}</Badge>
                        </div>
                        <p className="text-xs text-slate-400 leading-relaxed">{f.desc}</p>
                      </div>
                    </div>
                  </GlassCard>
                </ScrollReveal>
              );
            })}
          </div>
        </section>
      </ScrollReveal>

      {/* ── CTA Banner ───────────────────────────────── */}
      <ScrollReveal>
        <section className="relative overflow-hidden rounded-3xl">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-indigo-600/15 to-purple-600/20" />
          <div className="absolute inset-0 bg-grid opacity-30" style={{ backgroundSize: '40px 40px' }} />
          <GlowingOrb color="#6366f1" size={300} intensity={0.2} className="top-[-60px] right-[10%]" />
          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6 p-8 md:p-10">
            <div className="space-y-2 text-center md:text-left">
              <h3 className="font-display text-2xl font-bold text-white">Ready to ask about your campus?</h3>
              <p className="text-slate-400 text-sm">Select a college context from the sidebar, then start your AI conversation.</p>
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
