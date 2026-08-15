import React from 'react';
import { motion } from 'framer-motion';
import {
  ArrowRight, Sparkles, GraduationCap, BookOpen,
  Shield, Globe, Cpu, Activity,
  FlaskConical, Scale, Stethoscope, Building2, Wheat, ChevronRight
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
}

const STATS = [
  { label: 'Colleges', value: 22, suffix: '+', icon: GraduationCap, color: 'text-amber-700', bg: 'bg-amber-50', tag: '22' },
  { label: 'Query Topics', value: 150, suffix: '+', icon: BookOpen, color: 'text-orange-700', bg: 'bg-orange-50', tag: '150+' },
  { label: 'RAG Docs', value: 5000, suffix: '+', icon: Cpu, color: 'text-amber-600', bg: 'bg-amber-50', tag: '5.2k' },
  { label: 'Satisfaction', value: 95, suffix: '%', icon: Activity, color: 'text-olive-700', bg: 'bg-olive-50', tag: '95%' },
];

const DISCIPLINES = [
  { label: 'Engineering', icon: FlaskConical, color: 'from-amber-600 to-amber-700', desc: 'B.Tech/BE · AICTE · JEE/State CETs', coverage: 82 },
  { label: 'Medical Sciences', icon: Stethoscope, color: 'from-olive-600 to-olive-700', desc: 'MBBS/BDS · NMC/DCI · NEET', coverage: 76 },
  { label: 'Law & Justice', icon: Scale, color: 'from-orange-600 to-orange-700', desc: 'LLB/LLM · BCI · CLAT/AILET', coverage: 71 },
  { label: 'Management', icon: Building2, color: 'from-amber-700 to-amber-800', desc: 'MBA/BBA · AICTE · CAT/MAT', coverage: 68 },
  { label: 'Arts & Sciences', icon: Globe, color: 'from-rose-600 to-rose-700', desc: 'BA/BSc/BCom · UGC/CBCS · CUET', coverage: 88 },
  { label: 'Agriculture', icon: Wheat, color: 'from-olive-500 to-olive-600', desc: 'BSc Agri · ICAR · ICAR AIEEA', coverage: 60 },
];

const getFeatures = (modelName: string) => [
  {
    icon: Cpu, title: 'LangGraph ReAct Agent',
    desc: 'Multi-step reasoning agent that autonomously selects from 5 domain tools.',
    badge: 'Core', badgeVariant: 'amber' as const
  },
  {
    icon: Shield, title: 'FAISS Semantic Search',
    desc: 'Dense vector embeddings for precise sub-second retrieval across campus handbooks.',
    badge: 'RAG', badgeVariant: 'slate' as const
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

const GRADIENT_COLORS = [
  'from-amber-500 to-amber-600',
  'from-orange-400 to-orange-500',
  'from-olive-400 to-olive-500',
  'from-amber-600 to-amber-700',
  'from-rose-400 to-rose-500',
  'from-amber-400 to-amber-500',
  'from-orange-500 to-orange-600',
  'from-olive-500 to-olive-600',
];

export const DashboardTab: React.FC<DashboardTabProps> = ({
  colleges, onSelectCollege, setActiveTab, modelName,
}) => {
  return (
    <div className="space-y-12 pb-12">

      {/* ── Hero Section ─────────────────────────────── */}
      <section className="relative rounded-2xl overflow-hidden bg-gradient-to-br from-amber-50/40 via-[#FBF8F3] to-stone-50/40 border border-amber-100/60">
        <DoodleHero />

        <div className="relative z-10 max-w-3xl pt-12 pb-10 px-6 md:px-10">
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="mb-5"
          >
            <Badge variant="amber">
              {modelName} · LangChain · FAISS
            </Badge>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...spring.crisp, delay: 0.1 }}
            className="font-display text-4xl md:text-5xl font-bold leading-tight tracking-tight mb-3 gradient-text bg-gradient-to-r from-amber-700 to-amber-800"
          >
            Your campus, simplified.
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-stone-500 text-base md:text-lg leading-relaxed max-w-xl mb-7"
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
            <ShimmerButton size="lg" variant="accent" onClick={() => setActiveTab('chat')}>
              Start Chatting
              <ChevronRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
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
            <Card key={i} className="p-5 bg-[#F3ECE1]/50" hover={false}>
              <div className="flex items-center justify-between mb-3">
                <div className={cn('w-9 h-9 rounded-lg flex items-center justify-center', stat.bg)}>
                  <Icon className={cn('h-5 w-5', stat.color)} />
                </div>
                <BlueprintStat label="" value={stat.tag} />
              </div>
              <div className={cn('text-2xl font-bold mb-1', stat.color)}>
                <AnimatedCounter to={stat.value} suffix={stat.suffix} duration={1800} />
              </div>
              <p className="text-sm text-stone-500">{stat.label}</p>
            </Card>
          );
        })}
      </section>

      {/* ── Featured Colleges (Bento Grid) ──────────── */}
      <ScrollReveal>
        <section id="all-colleges" className="space-y-5">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-display text-2xl font-semibold text-stone-900 tracking-tight">Campus Contexts</h2>
              <p className="text-sm text-stone-500 mt-1">Select a college to focus your AI responses</p>
            </div>
            <BlueprintStat label="DOCS" value="5.2k" />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {colleges.slice(0, 6).map((college, i) => (
              <motion.div
                key={college.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ ...spring.crisp, delay: i * 0.05 }}
              >
                <Card
                  className="p-4 group relative overflow-hidden"
                  onClick={() => { onSelectCollege(college); setActiveTab('chat'); }}
                >
                  {/* Blueprint top border accent */}
                  <div className={cn(
                    'absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r opacity-60',
                    GRADIENT_COLORS[i % GRADIENT_COLORS.length]
                  )} />

                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{college.icon}</span>
                      <div className="min-w-0">
                        <h3 title={college.name} className="font-medium text-base text-stone-800 group-hover:text-amber-700 transition-colors truncate">
                          {college.name}
                        </h3>
                        <p className="text-sm text-stone-400 truncate">{college.location}</p>
                      </div>
                    </div>
                    {/* Status beacon */}
                    <div className="flex items-center gap-1.5 flex-shrink-0">
                      <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500" />
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <Badge variant="slate" className="text-2xs font-mono">{college.type.split(' ')[0]}</Badge>
                    <span className="text-sm font-medium text-amber-700 flex items-center gap-1 group-hover:gap-1.5 transition-all">
                      Ask <ChevronRight className="h-3.5 w-3.5" />
                    </span>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </section>
      </ScrollReveal>

      {/* ── Disciplines ──────────────────────────────── */}
      <ScrollReveal>
        <section className="space-y-5">
          <div>
            <h2 className="font-display text-2xl font-semibold text-stone-900 tracking-tight">Academic Coverage</h2>
            <p className="text-sm text-stone-500 mt-1">Knowledge depth across Indian regulatory domains</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {DISCIPLINES.map((d, i) => {
              const Icon = d.icon;
              return (
                <Card key={i} className="p-5" hover={false}>
                  <div className="flex items-center gap-3 mb-3">
                    <div className={cn('p-2.5 rounded-lg bg-gradient-to-br', d.color, 'bg-opacity-10')}>
                      <Icon className="h-5 w-5 text-white" />
                    </div>
                    <div>
                      <p className="font-medium text-base text-stone-800">{d.label}</p>
                      <p className="text-sm text-stone-400 font-mono">{d.desc}</p>
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
          <h2 className="font-display text-2xl font-semibold text-stone-900 tracking-tight">Technology</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {getFeatures(modelName).map((f, i) => {
              const Icon = f.icon;
              return (
                <Card key={i} className="p-6" hover={false}>
                  <div className="flex items-start gap-4">
                    <div className="p-2.5 bg-amber-50 rounded-lg flex-shrink-0">
                      <Icon className="h-5 w-5 text-amber-700" />
                    </div>
                    <div className="space-y-1.5 flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-base text-stone-800">{f.title}</p>
                        <Badge variant={f.badgeVariant} className="ml-auto">{f.badge}</Badge>
                      </div>
                      <p className="text-sm text-stone-500 leading-relaxed">{f.desc}</p>
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
        <section className="rounded-xl border border-[#E8E2D5] bg-[#F3ECE1]/50 p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <p className="font-medium text-base text-stone-800">Ready to explore?</p>
            <p className="text-sm text-stone-500">Select a college and start your AI conversation.</p>
          </div>
          <ShimmerButton onClick={() => setActiveTab('chat')} className="flex-shrink-0">
            Start Chatting <ChevronRight className="h-3.5 w-3.5" />
          </ShimmerButton>
        </section>
      </ScrollReveal>
    </div>
  );
};
