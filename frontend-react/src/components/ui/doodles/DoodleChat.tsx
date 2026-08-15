import React from 'react';
import { cn } from '../../../lib/cn';

interface DoodleProps {
  className?: string;
}

export const DoodleChat: React.FC<DoodleProps> = ({ className }) => (
  <div className={cn('absolute inset-0 overflow-hidden pointer-events-none', className)}>
    {/* Speech Bubble */}
    <svg className="absolute top-[10%] left-[5%] w-14 h-14 doodle-float" style={{ '--rotate': '2deg' } as React.CSSProperties} viewBox="0 0 56 56" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M8 12h40v24H20l-8 8v-8H8z" className="text-amber-400 opacity-10" />
      <path d="M18 22h20M18 30h12" className="text-amber-300 opacity-6" />
    </svg>

    {/* Brain */}
    <svg className="absolute top-[15%] right-[6%] w-12 h-12 doodle-float doodle-float-delay-1" style={{ '--rotate': '-5deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M24 8c-6 0-10 4-10 8 0 2 1 4 2 5-3 2-5 5-5 9 0 5 4 10 13 10s13-5 13-10c0-4-2-7-5-9 1-1 2-3 2-5 0-4-4-8-10-8z" className="text-amber-400 opacity-8" />
      <path d="M24 8v32" className="text-amber-300 opacity-6" />
      <path d="M18 18c-2 2-2 6 0 10M30 18c2 2 2 6 0 10" className="text-amber-300 opacity-4" />
    </svg>

    {/* Lightning Bolt */}
    <svg className="absolute top-[50%] left-[3%] w-10 h-10 doodle-float doodle-float-delay-2" style={{ '--rotate': '8deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 4L8 22h10l-4 14 16-18H20z" className="text-amber-400 opacity-10" />
    </svg>

    {/* Chat Dots */}
    <svg className="absolute bottom-[25%] right-[5%] w-12 h-12 doodle-float" style={{ '--rotate': '-3deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="16" cy="20" rx="12" ry="10" className="text-amber-300 opacity-8" />
      <ellipse cx="34" cy="18" rx="8" ry="7" className="text-amber-400 opacity-6" />
      <path d="M8 28l-4 8 8-4" className="text-amber-300 opacity-6" />
      <circle cx="12" cy="20" r="1.5" className="text-amber-400 opacity-10" fill="currentColor" />
      <circle cx="18" cy="20" r="1.5" className="text-amber-400 opacity-10" fill="currentColor" />
      <circle cx="22" cy="20" r="1.5" className="text-amber-400 opacity-10" fill="currentColor" />
    </svg>

    {/* Magnifying Glass */}
    <svg className="absolute bottom-[15%] left-[8%] w-10 h-10 doodle-float doodle-float-delay-1" style={{ '--rotate': '4deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="18" cy="18" r="12" className="text-amber-400 opacity-8" />
      <path d="M28 28l8 8" className="text-amber-300 opacity-6" />
      <path d="M14 14h8M14 22h4" className="text-amber-300 opacity-4" />
    </svg>

    {/* Question Mark */}
    <svg className="absolute top-[35%] right-[12%] w-8 h-8 doodle-float doodle-float-delay-2" style={{ '--rotate': '-6deg' } as React.CSSProperties} viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 8c-4 0-6 3-6 6 0 4 3 6 6 6 2 0 3-1 4-2l0-4" className="text-amber-400 opacity-8" />
      <circle cx="13" cy="24" r="1.5" className="text-amber-400 opacity-8" fill="currentColor" />
    </svg>

    {/* Dotted Curve */}
    <svg className="absolute top-[60%] left-[25%] w-24 h-10 doodle-float" viewBox="0 0 96 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="3 4">
      <path d="M4 36C24 4 72 4 92 36" className="text-amber-300 opacity-5" />
    </svg>
  </div>
);
