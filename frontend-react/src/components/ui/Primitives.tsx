import React, { useState, useEffect, useRef } from 'react';
import { cn } from '../../lib/cn';

// ────────────────────────────────────────────────────
//  Animated Counter
// ────────────────────────────────────────────────────
interface AnimatedCounterProps {
  to: number;
  from?: number;
  duration?: number;
  suffix?: string;
  prefix?: string;
  className?: string;
  decimals?: number;
}

export const AnimatedCounter: React.FC<AnimatedCounterProps> = ({
  to,
  from = 0,
  duration = 2000,
  suffix = '',
  prefix = '',
  className,
  decimals = 0,
}) => {
  const [value, setValue] = useState(from);
  const observerRef = useRef<IntersectionObserver | null>(null);
  const containerRef = useRef<HTMLSpanElement>(null);
  const hasAnimated = useRef(false);

  useEffect(() => {
    observerRef.current = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !hasAnimated.current) {
          hasAnimated.current = true;
          const start = performance.now();
          const animate = (now: number) => {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            setValue(from + (to - from) * eased);
            if (progress < 1) requestAnimationFrame(animate);
          };
          requestAnimationFrame(animate);
        }
      },
      { threshold: 0.3 }
    );

    if (containerRef.current) {
      observerRef.current.observe(containerRef.current);
    }

    return () => observerRef.current?.disconnect();
  }, [to, from, duration]);

  return (
    <span ref={containerRef} className={className}>
      {prefix}{value.toFixed(decimals)}{suffix}
    </span>
  );
};

// ────────────────────────────────────────────────────
//  Spring Physics Presets
// ────────────────────────────────────────────────────
export const spring = {
  crisp: { type: 'spring' as const, stiffness: 400, damping: 28 },
  gentle: { type: 'spring' as const, stiffness: 300, damping: 30 },
  bouncy: { type: 'spring' as const, stiffness: 500, damping: 24 },
} as const;

// ────────────────────────────────────────────────────
//  Card
// ────────────────────────────────────────────────────
interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({
  children, className, hover = true, onClick,
}) => (
  <div
    className={cn(
      'bg-white/90 rounded-xl border border-slate-200/60 shadow-card transition-all duration-200',
      hover && 'hover:shadow-card-hover hover:border-slate-300/60 hover:scale-[1.02] cursor-pointer',
      className
    )}
    onClick={onClick}
  >
    {children}
  </div>
);

// ────────────────────────────────────────────────────
//  Button (renamed from ShimmerButton)
// ────────────────────────────────────────────────────
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'accent';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const ShimmerButton: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  className,
  ...props
}) => {
  const variants = {
    primary: 'bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 text-white shadow-sm hover:shadow-lg hover:shadow-blue-500/25',
    secondary: 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300',
    ghost: 'hover:bg-slate-100 text-slate-500 hover:text-slate-700',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    accent: 'bg-gradient-to-r from-indigo-500 to-violet-500 hover:from-indigo-600 hover:to-violet-600 text-white shadow-sm hover:shadow-lg hover:shadow-indigo-500/25',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs rounded-lg gap-1.5',
    md: 'px-5 py-2.5 text-sm rounded-lg gap-2',
    lg: 'px-8 py-3.5 text-base rounded-lg gap-2.5',
  };

  return (
    <button
      className={cn(
        'group/btn relative inline-flex items-center justify-center font-medium transition-all duration-150',
        'focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-blue focus-visible:ring-offset-2',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        'active:scale-95',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      <span className="inline-flex items-center gap-2 transition-transform duration-200 group-hover/btn:translate-x-0.5">
        {children}
      </span>
    </button>
  );
};

// ────────────────────────────────────────────────────
//  Blueprint Stat (monospace metadata tag)
// ────────────────────────────────────────────────────
interface BlueprintStatProps {
  label: string;
  value: string | number;
  className?: string;
}

export const BlueprintStat: React.FC<BlueprintStatProps> = ({
  label, value, className,
}) => (
  <span className={cn(
    'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md',
    'bg-slate-50 border border-slate-200/80',
    'font-mono text-2xs tracking-wider text-slate-600 uppercase',
    className
  )}>
    {label && <span className="text-slate-400">{label}:</span>}
    <span className="text-slate-800 font-semibold">{value}</span>
  </span>
);

// ────────────────────────────────────────────────────
//  Badge (WCAG AA contrast)
// ────────────────────────────────────────────────────
interface BadgeProps {
  children: React.ReactNode;
  variant?: 'blue' | 'purple' | 'green' | 'amber' | 'rose' | 'cyan' | 'slate';
  dot?: boolean;
  pulse?: boolean;
  className?: string;
}

const badgeVariants = {
  blue: 'bg-blue-50 text-blue-900 border-blue-200/60',
  purple: 'bg-purple-50 text-purple-900 border-purple-200/60',
  green: 'bg-emerald-50 text-emerald-900 border-emerald-200/60',
  amber: 'bg-amber-50 text-amber-900 border-amber-200/60',
  rose: 'bg-rose-50 text-rose-900 border-rose-200/60',
  cyan: 'bg-cyan-50 text-cyan-900 border-cyan-200/60',
  slate: 'bg-slate-100 text-slate-700 border-slate-200/60',
};

const dotColors = {
  blue: 'bg-blue-500', purple: 'bg-purple-500', green: 'bg-emerald-500',
  amber: 'bg-amber-500', rose: 'bg-rose-500', cyan: 'bg-cyan-500', slate: 'bg-slate-500',
};

export const Badge: React.FC<BadgeProps> = ({
  children, variant = 'blue', dot = false, pulse = false, className,
}) => (
  <span className={cn(
    'inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-xs font-medium border',
    badgeVariants[variant], className
  )}>
    {dot && (
      <span className="relative flex h-1.5 w-1.5">
        {pulse && <span className={cn('animate-ping absolute inline-flex h-full w-full rounded-full opacity-75', dotColors[variant])} />}
        <span className={cn('relative inline-flex rounded-full h-1.5 w-1.5', dotColors[variant])} />
      </span>
    )}
    {children}
  </span>
);

// ────────────────────────────────────────────────────
//  ScrollReveal
// ────────────────────────────────────────────────────
interface ScrollRevealProps {
  children: React.ReactNode;
  delay?: number;
  direction?: 'up' | 'down' | 'left' | 'right' | 'none';
  className?: string;
}

export const ScrollReveal: React.FC<ScrollRevealProps> = ({
  children, delay = 0, direction = 'up', className,
}) => {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mq.matches) { setVisible(true); return; }

    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setVisible(true); },
      { threshold: 0.1 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  const initialStyles: React.CSSProperties = {
    opacity: 0,
    transform: direction === 'up' ? 'translateY(20px)' :
               direction === 'down' ? 'translateY(-20px)' :
               direction === 'left' ? 'translateX(-20px)' :
               direction === 'right' ? 'translateX(20px)' : 'none',
    transition: `all 0.5s cubic-bezier(0.16, 1, 0.3, 1) ${delay}ms`,
  };

  const visibleStyles: React.CSSProperties = {
    opacity: 1,
    transform: 'none',
  };

  return (
    <div
      ref={ref}
      className={className}
      style={visible ? { ...initialStyles, ...visibleStyles } : initialStyles}
    >
      {children}
    </div>
  );
};

// ────────────────────────────────────────────────────
//  Divider
// ────────────────────────────────────────────────────
export const Divider: React.FC<{ className?: string }> = ({ className }) => (
  <div className={cn('h-px bg-slate-100', className)} />
);

// ────────────────────────────────────────────────────
//  LoadingSpinner
// ────────────────────────────────────────────────────
export const LoadingSpinner: React.FC<{ className?: string; size?: number }> = ({
  className, size = 32,
}) => (
  <div className={cn('flex flex-col items-center justify-center gap-3', className)}>
    <div
      className="rounded-full border-2 border-slate-200 border-t-brand-blue animate-spin"
      style={{ width: size, height: size }}
    />
  </div>
);

// ────────────────────────────────────────────────────
//  Skeleton
// ────────────────────────────────────────────────────
interface SkeletonProps {
  className?: string;
  count?: number;
}

export const Skeleton: React.FC<SkeletonProps> = ({ className, count = 1 }) => (
  <div className="space-y-3">
    {Array.from({ length: count }).map((_, i) => (
      <div
        key={i}
        className={cn('animate-skeleton bg-slate-100 rounded-lg', className)}
      />
    ))}
  </div>
);

// ────────────────────────────────────────────────────
//  ProgressBar
// ────────────────────────────────────────────────────
interface ProgressBarProps {
  value: number;
  max?: number;
  label?: string;
  color?: string;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value, max = 100, label, color = 'from-blue-500 to-blue-600', className,
}) => {
  const pct = Math.min((value / max) * 100, 100);
  const [width, setWidth] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setWidth(pct); },
      { threshold: 0.5 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [pct]);

  return (
    <div ref={ref} className={cn('space-y-1.5', className)}>
      {label && (
        <div className="flex justify-between text-xs text-slate-500">
          <span className="capitalize">{label}</span>
          <span className="text-slate-700 font-medium">{Math.round(pct)}%</span>
        </div>
      )}
      <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
        <div
          className={cn('h-full rounded-full bg-gradient-to-r transition-all duration-1000 ease-out', color)}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  );
};
