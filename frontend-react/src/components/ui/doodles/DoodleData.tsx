import React from 'react';
import { cn } from '../../../lib/cn';

interface DoodleProps {
  className?: string;
}

export const DoodleData: React.FC<DoodleProps> = ({ className }) => (
  <div className={cn('absolute inset-0 overflow-hidden pointer-events-none', className)}>
    {/* Bar Chart */}
    <svg className="absolute top-[10%] left-[4%] w-14 h-14 doodle-float" style={{ '--rotate': '2deg' } as React.CSSProperties} viewBox="0 0 56 56" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M8 48V8" className="text-violet-400 opacity-10" />
      <path d="M8 48h40" className="text-violet-400 opacity-8" />
      <rect x="14" y="28" width="6" height="20" rx="1" className="text-violet-300 opacity-6" />
      <rect x="24" y="18" width="6" height="30" rx="1" className="text-violet-400 opacity-8" />
      <rect x="34" y="24" width="6" height="24" rx="1" className="text-violet-300 opacity-6" />
      <rect x="44" y="14" width="6" height="34" rx="1" className="text-violet-400 opacity-10" />
    </svg>

    {/* Trending Arrow */}
    <svg className="absolute top-[12%] right-[5%] w-12 h-12 doodle-float doodle-float-delay-1" style={{ '--rotate': '-4deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M6 36l12-12 8 4 16-16" className="text-violet-400 opacity-10" />
      <path d="M30 12h12v12" className="text-violet-400 opacity-8" />
      <path d="M6 36l12-12 8 4 16-16" className="text-violet-400 opacity-8" strokeDasharray="none" />
    </svg>

    {/* Target */}
    <svg className="absolute top-[45%] left-[3%] w-10 h-10 doodle-float doodle-float-delay-2" style={{ '--rotate': '7deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="20" cy="20" r="16" className="text-violet-400 opacity-8" />
      <circle cx="20" cy="20" r="10" className="text-violet-300 opacity-6" />
      <circle cx="20" cy="20" r="4" className="text-violet-400 opacity-10" />
      <circle cx="20" cy="20" r="1" className="text-violet-400 opacity-10" fill="currentColor" />
    </svg>

    {/* Gauge */}
    <svg className="absolute bottom-[22%] right-[6%] w-12 h-12 doodle-float" style={{ '--rotate': '-3deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M8 32a16 16 0 0132 0" className="text-violet-400 opacity-8" />
      <path d="M24 32V20" className="text-violet-400 opacity-10" />
      <circle cx="24" cy="32" r="3" className="text-violet-400 opacity-10" fill="currentColor" />
      <path d="M14 14l-4-4M34 14l4-4" className="text-violet-300 opacity-6" />
    </svg>

    {/* Pie Chart */}
    <svg className="absolute bottom-[18%] left-[7%] w-10 h-10 doodle-float doodle-float-delay-1" style={{ '--rotate': '5deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="20" cy="20" r="14" className="text-violet-400 opacity-8" />
      <path d="M20 20L20 6" className="text-violet-400 opacity-10" />
      <path d="M20 20l12 8" className="text-violet-300 opacity-6" />
      <path d="M20 20l-4 13" className="text-violet-300 opacity-6" />
    </svg>

    {/* Connected Dots */}
    <svg className="absolute top-[55%] right-[15%] w-14 h-10 doodle-float doodle-float-delay-2" viewBox="0 0 56 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="8" cy="20" r="3" className="text-violet-400 opacity-8" />
      <circle cx="22" cy="10" r="3" className="text-violet-300 opacity-6" />
      <circle cx="36" cy="28" r="3" className="text-violet-400 opacity-8" />
      <circle cx="50" cy="16" r="3" className="text-violet-300 opacity-6" />
      <path d="M11 19l8-7 8 16 10-10" className="text-violet-300 opacity-6" />
    </svg>

    {/* Dotted Curve */}
    <svg className="absolute top-[30%] left-[22%] w-20 h-10 doodle-float" viewBox="0 0 80 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="3 4">
      <path d="M4 36C20 4 60 4 76 36" className="text-violet-300 opacity-5" />
    </svg>

    {/* Stars */}
    <svg className="absolute top-[22%] left-[28%] w-3 h-3 doodle-float doodle-float-delay-1" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round">
      <path d="M8 1l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" className="text-violet-300 opacity-6" />
    </svg>
    <svg className="absolute bottom-[40%] right-[22%] w-3 h-3 doodle-float" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round">
      <path d="M8 1l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" className="text-violet-400 opacity-8" />
    </svg>
  </div>
);
