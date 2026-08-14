import React from 'react';
import { cn } from '../../../lib/cn';

interface DoodleProps {
  className?: string;
}

export const DoodleHero: React.FC<DoodleProps> = ({ className }) => (
  <div className={cn('absolute inset-0 overflow-hidden pointer-events-none', className)}>
    {/* Graduation Cap */}
    <svg className="absolute top-[8%] left-[4%] w-16 h-16 doodle-float" style={{ '--rotate': '3deg' } as React.CSSProperties} viewBox="0 0 64 64" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M32 8L4 24L32 40L60 24Z" className="text-indigo-400 opacity-10" />
      <path d="M16 28v16c0 4 7.2 8 16 8s16-4 16-8V28" className="text-indigo-400 opacity-8" />
      <path d="M52 24v16" className="text-indigo-400 opacity-8" />
      <circle cx="52" cy="42" r="2" className="text-indigo-400 opacity-8" fill="currentColor" />
    </svg>

    {/* Open Book */}
    <svg className="absolute top-[12%] right-[6%] w-14 h-14 doodle-float doodle-float-delay-1" style={{ '--rotate': '-4deg' } as React.CSSProperties} viewBox="0 0 56 56" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M28 12C20 12 8 14 8 14v28s8-2 20-2" className="text-indigo-300 opacity-10" />
      <path d="M28 12c8 0 20 2 20 2v28s-8-2-20-2" className="text-indigo-300 opacity-8" />
      <path d="M28 12v30" className="text-indigo-400 opacity-10" />
      <path d="M14 20h8M14 26h6" className="text-indigo-300 opacity-6" />
      <path d="M34 20h8M36 26h6" className="text-indigo-300 opacity-6" />
    </svg>

    {/* Pencil */}
    <svg className="absolute top-[45%] left-[3%] w-12 h-12 doodle-float doodle-float-delay-2" style={{ '--rotate': '12deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M8 40L32 8l8 8L16 40H8z" className="text-indigo-400 opacity-8" />
      <path d="M32 8l8 8" className="text-indigo-400 opacity-10" />
      <path d="M8 40l4-12" className="text-indigo-300 opacity-8" />
      <path d="M12 36l-4 4h8" className="text-indigo-300 opacity-6" />
    </svg>

    {/* Lightbulb */}
    <svg className="absolute top-[30%] right-[4%] w-12 h-12 doodle-float" style={{ '--rotate': '-2deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M24 4c-8 0-14 6-14 14 0 6 3 10 8 12v4h12v-4c5-2 8-6 8-12 0-8-6-14-14-14z" className="text-indigo-400 opacity-10" />
      <path d="M18 34h12" className="text-indigo-400 opacity-8" />
      <path d="M20 38h8" className="text-indigo-300 opacity-8" />
      <path d="M24 4v-0M36 8l2-2M12 8l-2-2M40 20h2M6 20h2" className="text-indigo-300 opacity-6" />
    </svg>

    {/* Atom */}
    <svg className="absolute bottom-[20%] right-[8%] w-14 h-14 doodle-float doodle-float-delay-1" style={{ '--rotate': '5deg' } as React.CSSProperties} viewBox="0 0 56 56" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="28" cy="28" rx="22" ry="8" className="text-indigo-300 opacity-8" />
      <ellipse cx="28" cy="28" rx="22" ry="8" className="text-indigo-300 opacity-6" transform="rotate(60 28 28)" />
      <ellipse cx="28" cy="28" rx="22" ry="8" className="text-indigo-300 opacity-6" transform="rotate(120 28 28)" />
      <circle cx="28" cy="28" r="3" className="text-indigo-400 opacity-10" fill="currentColor" />
    </svg>

    {/* Calculator */}
    <svg className="absolute bottom-[15%] left-[6%] w-12 h-12 doodle-float doodle-float-delay-2" style={{ '--rotate': '-3deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="8" y="4" width="32" height="40" rx="3" className="text-indigo-400 opacity-8" />
      <rect x="12" y="8" width="24" height="10" rx="1" className="text-indigo-300 opacity-6" />
      <circle cx="16" cy="26" r="2" className="text-indigo-300 opacity-6" />
      <circle cx="24" cy="26" r="2" className="text-indigo-300 opacity-6" />
      <circle cx="32" cy="26" r="2" className="text-indigo-300 opacity-6" />
      <circle cx="16" cy="34" r="2" className="text-indigo-300 opacity-6" />
      <circle cx="24" cy="34" r="2" className="text-indigo-300 opacity-6" />
      <circle cx="32" cy="34" r="2" className="text-indigo-400 opacity-8" />
    </svg>

    {/* Diploma Scroll */}
    <svg className="absolute top-[55%] right-[15%] w-10 h-10 doodle-float" style={{ '--rotate': '6deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M8 8h24v24H8z" className="text-indigo-300 opacity-6" />
      <path d="M8 8c-2 0-4 2-4 4s2 4 4 4" className="text-indigo-300 opacity-6" />
      <path d="M32 8c2 0 4 2 4 4s-2 4-4 4" className="text-indigo-300 opacity-6" />
      <path d="M14 16h12M14 22h8M14 28h10" className="text-indigo-300 opacity-4" />
    </svg>

    {/* E=mc² */}
    <svg className="absolute top-[5%] left-[40%] w-20 h-8 doodle-float doodle-float-delay-1" viewBox="0 0 80 32" fill="none">
      <text x="4" y="22" fontFamily="Georgia, serif" fontStyle="italic" fontSize="16" className="text-indigo-300 opacity-8" fill="currentColor">E=mc²</text>
    </svg>

    {/* Stars */}
    <svg className="absolute top-[20%] left-[25%] w-4 h-4 doodle-float doodle-float-delay-2" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round">
      <path d="M8 1l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" className="text-indigo-300 opacity-6" />
    </svg>
    <svg className="absolute bottom-[35%] left-[15%] w-3 h-3 doodle-float" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round">
      <path d="M8 1l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" className="text-indigo-400 opacity-8" />
    </svg>
    <svg className="absolute top-[65%] right-[25%] w-3 h-3 doodle-float doodle-float-delay-1" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round">
      <path d="M8 1l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" className="text-indigo-300 opacity-6" />
    </svg>

    {/* Dotted Curves */}
    <svg className="absolute bottom-[40%] right-[3%] w-20 h-10 doodle-float" viewBox="0 0 80 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="3 4">
      <path d="M4 36C20 4 60 4 76 36" className="text-indigo-300 opacity-6" />
    </svg>
    <svg className="absolute top-[40%] left-[20%] w-16 h-8 doodle-float doodle-float-delay-2" viewBox="0 0 64 32" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="3 4">
      <path d="M4 28C16 4 48 4 60 28" className="text-indigo-400 opacity-6" />
    </svg>
  </div>
);
