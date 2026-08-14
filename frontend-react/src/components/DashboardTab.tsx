import React from 'react';
import { motion } from 'framer-motion';
import {
  ArrowRight, Sparkles, GraduationCap, BookOpen,
  Shield, Globe, Cpu, Activity,
  FlaskConical, Scale, Stethoscope, Building2, Wheat
} from 'lucide-react';
import { DoodleBanner } from './ui/DoodleBanner';
import {
  AnimatedCounter, ShimmerButton, Badge, Card, ScrollReveal, ProgressBar
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
    desc: 'Multi-step reasoning agent that autonomously selects from 5 domain tools.',
    badge: 'Core', badgeVariant: 'blue' as const
  },
  {
    icon: Shield, title: 'FAISS Semantic Search',
    desc: 'Dense vector embeddings for precise sub-second retrieval across campus handbooks.',
    badge: 'RAG', badgeVariant: 'purple' as const
  },
  {
    icon: Sparkles, title: modelName,
    desc: 'Token-efficient responses calibrated for Indian academic terminology.',
    badge: 'LLM', badgeVariant: 'amber' as const
  },
  {
    icon: Globe, title: 'Universal Coverage',
    desc: 'Works for ALL Indian college types — Engineering, Medical, Law, Agriculture & more.',
    badge: 'Pan-India', badgeVariant: 'green' as const
  },
];

export const DashboardTab: React.FC<DashboardTabProps> = ({
  colleges, onSelectCollege, setActiveTab, modelName,
}) => {
  return (
    <div className="space-y-12 pb-12">

      {/* ── Hero Section ─────────────────────────────── */}
      <section className="relative rounded-2xl overflow-hidden bg-white border border-slate-100">
        {/* Doodle accent — subtle, not dominant */}
        <div className="absolute inset-0 opacity-[0.07] pointer-events-none">
          <DoodleBanner />
        </div>

        <div className="relative z-10 max-w-3xl pt-12 pb-10 px-6 md:px-10">
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="mb-5"
          >
            <Badge variant="blue">
              {modelName} · LangChain · FAISS
            </Badge>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="font-display text-4xl md:text-5xl font-bold text-slate-900 leading-tight tracking-tight mb-3"
          >
            Your campus, simplified.
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-slate-500 text-sm md:text-base leading-relaxed max-w-xl mb-7"
          >
            Universal campus intelligence for all Indian college types.
            Ask about academics, events, contacts, and campus life.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.3 }}
            className="flex flex-wrap gap-3"
          >
            <ShimmerButton size="lg" onClick={() => setActiveTab('chat')}>
              Start Chatting
              <ArrowRight className="h-4 w-4" />
            </ShimmerButton>
            <ShimmerButton size="lg" variant="ghost" onClick={() => {
              document.getElementById('all-colleges')?.scrollIntoView({ behavior: 'smooth' });
            }}>
              Browse Colleges
            </ShimmerButton>
          </motion.div>
        </div>
      </section>

      {/* ── Stats Row ─────────────────────────────────── */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {STATS.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <Card key={i} className="p-4 bg-slate-50/80" hover={false}>
              <div className={cn('w-8 h-8 rounded-lg mb-2.5 flex items-center justify-center', stat.bg)}>
                <Icon className={cn('h-4 w-4', stat.color)} />
              </div>
              <div className={cn('text-xl font-bold mb-0.5', stat.color)}>
                <AnimatedCounter to={stat.value} suffix={stat.suffix} duration={1800} />
              </div>
              <p className="text-xs text-slate-500">{stat.label}</p>
            </Card>
          );
        })}
      </section>

      {/* ── Featured Colleges ─────────────────────────── */}
      <ScrollReveal>
        <section id="all-colleges" className="space-y-5">
          <div>
            <h2 className="font-display text-lg font-semibold text-slate-900 tracking-tight">Campus Contexts</h2>
            <p className="text-xs text-slate-500 mt-0.5">Select a college to focus your AI responses</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {colleges.slice(0, 6).map((college) => (
              <Card
                key={college.id}
                className="p-4 group"
                onClick={() => { onSelectCollege(college); setActiveTab('chat'); }}
              >
                <div className="flex items-start justify-between mb-3">
                  <span className="text-xl">{college.icon}</span>
                  <Badge variant="slate" className="text-2xs">{college.type.split(' ')[0]}</Badge>
                </div>
                <h3 title={college.name} className="font-medium text-sm text-slate-800 group-hover:text-brand-blue transition-colors truncate mb-0.5">
                  {college.name}
                </h3>
                <p className="text-xs text-slate-400 truncate mb-2">{college.location}</p>
                <span className="text-xs font-medium text-brand-blue">Ask about {college.short} →</span>
              </Card>
            ))}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Disciplines ──────────────────────────────── */}
      <ScrollReveal>
        <section className="space-y-5">
          <div>
            <h2 className="font-display text-lg font-semibold text-slate-900 tracking-tight">Academic Coverage</h2>
            <p className="text-xs text-slate-500 mt-0.5">Knowledge depth across Indian regulatory domains</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {DISCIPLINES.map((d, i) => {
              const Icon = d.icon;
              return (
                <Card key={i} className="p-4" hover={false}>
                  <div className="flex items-center gap-3 mb-3">
                    <div className={cn('p-2 rounded-lg bg-gradient-to-br', d.color, 'bg-opacity-10')}>
                      <Icon className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="font-medium text-sm text-slate-800">{d.label}</p>
                      <p className="text-2xs text-slate-400">{d.desc}</p>
                    </div>
                  </div>
                  <ProgressBar value={d.coverage} label="coverage" color={d.color} />
                </Card>
              );
            })}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Features ─────────────────────────────────── */}
      <ScrollReveal>
        <section className="space-y-5">
          <h2 className="font-display text-lg font-semibold text-slate-900 tracking-tight">Technology</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {getFeatures(modelName).map((f, i) => {
              const Icon = f.icon;
              return (
                <Card key={i} className="p-5" hover={false}>
                  <div className="flex items-start gap-3">
                    <div className="p-2 bg-blue-50 rounded-lg flex-shrink-0">
                      <Icon className="h-4 w-4 text-brand-blue" />
                    </div>
                    <div className="space-y-1 flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-sm text-slate-800">{f.title}</p>
                        <Badge variant={f.badgeVariant} className="ml-auto">{f.badge}</Badge>
                      </div>
                      <p className="text-xs text-slate-500 leading-relaxed">{f.desc}</p>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </section>
      </ScrollReveal>

      {/* ── CTA ──────────────────────────────────────── */}
      <ScrollReveal>
        <section className="rounded-xl border border-slate-100 bg-slate-50/50 p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <p className="font-medium text-sm text-slate-800">Ready to explore?</p>
            <p className="text-xs text-slate-500">Select a college and start your AI conversation.</p>
          </div>
          <ShimmerButton onClick={() => setActiveTab('chat')} className="flex-shrink-0">
            Start Chatting <ArrowRight className="h-3.5 w-3.5" />
          </ShimmerButton>
        </section>
      </ScrollReveal>
    </div>
  );
};
