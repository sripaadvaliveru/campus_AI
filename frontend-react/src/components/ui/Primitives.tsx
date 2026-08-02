import React, { useState, useEffect, useRef } from 'react';
import { cn } from '../../lib/cn';

// ────────────────────────────────────────────────────
//  Typewriter
// ────────────────────────────────────────────────────
interface TypewriterProps {
  words: string[];
  className?: string;
  speed?: number;
  deleteSpeed?: number;
  pauseTime?: number;
}

export const Typewriter: React.FC<TypewriterProps> = ({
  words,
  className,
  speed = 80,
  deleteSpeed = 40,
  pauseTime = 2000,
}) => {
  const [text, setText] = useState('');
  const [wordIndex, setWordIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    if (isPaused) {
      const timer = setTimeout(() => {
        setIsPaused(false);
        setIsDeleting(true);
      }, pauseTime);
      return () => clearTimeout(timer);
    }

    const currentWord = words[wordIndex];
    const timer = setTimeout(() => {
      if (!isDeleting) {
        const next = currentWord.slice(0, text.length + 1);
        setText(next);
        if (next === currentWord) setIsPaused(true);
      } else {
        const next = text.slice(0, text.length - 1);
        setText(next);
        if (next === '') {
          setIsDeleting(false);
          setWordIndex((i) => (i + 1) % words.length);
        }
      }
    }, isDeleting ? deleteSpeed : speed);

    return () => clearTimeout(timer);
  }, [text, isDeleting, isPaused, wordIndex, words, speed, deleteSpeed, pauseTime]);

  return (
    <span className={cn('inline-flex items-center', className)}>
      <span>{text}</span>
      <span className="ml-0.5 w-0.5 h-[1em] bg-current animate-cursor-blink inline-block" />
    </span>
  );
};

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
//  GlowingOrb
// ────────────────────────────────────────────────────
interface GlowingOrbProps {
  color?: string;
  size?: number;
  intensity?: number;
  className?: string;
  animate?: boolean;
}

export const GlowingOrb: React.FC<GlowingOrbProps> = ({
  color = '#3b82f6',
  size = 300,
  intensity = 0.15,
  className,
  animate = true,
}) => (
  <div
    className={cn('absolute rounded-full pointer-events-none', animate && 'animate-float-slow', className)}
    style={{
      width: size,
      height: size,
      background: color,
      filter: `blur(${size * 0.4}px)`,
      opacity: intensity,
    }}
  />
);

// ────────────────────────────────────────────────────
//  MagneticCard
// ────────────────────────────────────────────────────
interface MagneticCardProps {
  children: React.ReactNode;
  className?: string;
  strength?: number;
}

export const MagneticCard: React.FC<MagneticCardProps> = ({
  children,
  className,
  strength = 15,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = ((e.clientX - cx) / (rect.width / 2)) * strength;
    const dy = ((e.clientY - cy) / (rect.height / 2)) * strength;
    cardRef.current.style.transform = `perspective(1000px) rotateX(${-dy * 0.4}deg) rotateY(${dx * 0.4}deg) translateY(-4px)`;
    cardRef.current.style.boxShadow = `${-dx * 0.5}px ${-dy * 0.5}px 30px rgba(59,130,246,0.15)`;
  };

  const handleMouseLeave = () => {
    if (!cardRef.current) return;
    cardRef.current.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
    cardRef.current.style.boxShadow = '';
  };

  return (
    <div
      ref={cardRef}
      className={cn('transition-all duration-200 ease-out', className)}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      {children}
    </div>
  );
};

// ────────────────────────────────────────────────────
//  ShimmerButton
// ────────────────────────────────────────────────────
interface ShimmerButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  shimmer?: boolean;
}

export const ShimmerButton: React.FC<ShimmerButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  className,
  shimmer = true,
  ...props
}) => {
  const variants = {
    primary: 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-glow',
    secondary: 'glass border-border text-slate-200 hover:border-blue-500/30 hover:text-white',
    ghost: 'hover:bg-white/5 text-slate-300 hover:text-white',
    danger: 'bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs rounded-lg gap-1.5',
    md: 'px-5 py-2.5 text-sm rounded-xl gap-2',
    lg: 'px-8 py-3.5 text-base rounded-xl gap-2.5',
  };

  return (
    <button
      className={cn(
        'relative inline-flex items-center justify-center font-semibold transition-all duration-200',
        'focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        'active:scale-95',
        shimmer && variant === 'primary' && 'shine',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
};

// ────────────────────────────────────────────────────
//  Badge
// ────────────────────────────────────────────────────
interface BadgeProps {
  children: React.ReactNode;
  variant?: 'blue' | 'purple' | 'green' | 'amber' | 'rose' | 'cyan' | 'slate';
  dot?: boolean;
  pulse?: boolean;
  className?: string;
}

const badgeVariants = {
  blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  green: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  amber: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  rose: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
  cyan: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
  slate: 'bg-slate-800/80 text-slate-400 border-slate-700/50',
};

const dotColors = {
  blue: 'bg-blue-500', purple: 'bg-purple-500', green: 'bg-emerald-500',
  amber: 'bg-amber-500', rose: 'bg-rose-500', cyan: 'bg-cyan-500', slate: 'bg-slate-500',
};

export const Badge: React.FC<BadgeProps> = ({
  children, variant = 'blue', dot = false, pulse = false, className,
}) => (
  <span className={cn(
    'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-2xs font-semibold uppercase tracking-wider border',
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
//  GlassCard
// ────────────────────────────────────────────────────
interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  glow?: 'blue' | 'purple' | 'cyan' | false;
  onClick?: () => void;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children, className, hover = true, glow = false, onClick,
}) => {
  const glowMap = {
    blue: 'hover:shadow-glow hover:border-blue-500/20',
    purple: 'hover:shadow-glow-purple hover:border-purple-500/20',
    cyan: 'hover:border-cyan-500/20',
  };

  return (
    <div
      className={cn(
        'glass-card rounded-2xl transition-all duration-300',
        hover && 'hover:-translate-y-1 hover:shadow-card-hover cursor-pointer',
        glow && glowMap[glow],
        className
      )}
      onClick={onClick}
    >
      {children}
    </div>
  );
};

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
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setVisible(true); },
      { threshold: 0.1 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  const initialStyles: React.CSSProperties = {
    opacity: 0,
    transform: direction === 'up' ? 'translateY(30px)' :
               direction === 'down' ? 'translateY(-30px)' :
               direction === 'left' ? 'translateX(-30px)' :
               direction === 'right' ? 'translateX(30px)' : 'none',
    transition: `all 0.7s cubic-bezier(0.16, 1, 0.3, 1) ${delay}ms`,
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
  <div className={cn('h-px bg-gradient-to-r from-transparent via-white/10 to-transparent', className)} />
);

// ────────────────────────────────────────────────────
//  LoadingSpinner
// ────────────────────────────────────────────────────
export const LoadingSpinner: React.FC<{ className?: string; size?: number }> = ({
  className, size = 32,
}) => (
  <div className={cn('flex flex-col items-center justify-center gap-3', className)}>
    <div
      className="rounded-full border-2 border-transparent border-t-blue-500 animate-spin"
      style={{ width: size, height: size }}
    />
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
  value, max = 100, label, color = 'from-blue-500 to-indigo-500', className,
}) => {
  const pct = Math.min((value / max) * 100, 100);
  const [width, setWidth] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setWidth(pct); },
      { threshold: 0.3 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [pct]);

  return (
    <div ref={ref} className={cn('space-y-1.5', className)}>
      {label && (
        <div className="flex justify-between text-xs font-medium text-slate-400">
          <span className="capitalize">{label}</span>
          <span className="text-slate-300">{Math.round(pct)}%</span>
        </div>
      )}
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div
          className={cn('h-full rounded-full bg-gradient-to-r transition-all duration-1000 ease-out', color)}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  );
};
