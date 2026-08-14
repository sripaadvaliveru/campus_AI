import React from 'react';
import { cn } from '../../../lib/cn';

interface DoodleProps {
  className?: string;
}

export const DoodleCalendar: React.FC<DoodleProps> = ({ className }) => (
  <div className={cn('absolute inset-0 overflow-hidden pointer-events-none', className)}>
    {/* Calendar Page */}
    <svg className="absolute top-[8%] left-[4%] w-14 h-14 doodle-float" style={{ '--rotate': '2deg' } as React.CSSProperties} viewBox="0 0 56 56" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="6" y="10" width="44" height="38" rx="3" className="text-amber-400 opacity-10" />
      <path d="M6 22h44" className="text-amber-400 opacity-8" />
      <path d="M18 6v10M38 6v10" className="text-amber-400 opacity-10" />
      <rect x="14" y="28" width="6" height="6" rx="1" className="text-amber-300 opacity-6" />
      <rect x="25" y="28" width="6" height="6" rx="1" className="text-amber-400 opacity-8" />
      <rect x="36" y="28" width="6" height="6" rx="1" className="text-amber-300 opacity-6" />
      <rect x="14" y="38" width="6" height="6" rx="1" className="text-amber-300 opacity-6" />
      <rect x="25" y="38" width="6" height="6" rx="1" className="text-amber-300 opacity-6" />
    </svg>

    {/* Clock */}
    <svg className="absolute top-[15%] right-[5%] w-12 h-12 doodle-float doodle-float-delay-1" style={{ '--rotate': '-4deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="24" cy="24" r="18" className="text-amber-400 opacity-8" />
      <path d="M24 12v12l8 8" className="text-amber-400 opacity-10" />
      <circle cx="24" cy="24" r="2" className="text-amber-400 opacity-10" fill="currentColor" />
    </svg>

    {/* Party Popper */}
    <svg className="absolute top-[40%] left-[3%] w-10 h-10 doodle-float doodle-float-delay-2" style={{ '--rotate': '10deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 36L20 20" className="text-amber-400 opacity-10" />
      <path d="M20 20l8-16 8 8-16 8" className="text-amber-300 opacity-8" />
      <circle cx="12" cy="8" r="2" className="text-amber-400 opacity-8" fill="currentColor" />
      <circle cx="8" cy="16" r="1.5" className="text-amber-300 opacity-6" fill="currentColor" />
      <circle cx="28" cy="6" r="1.5" className="text-amber-300 opacity-6" fill="currentColor" />
      <path d="M4 8h4M8 4v4" className="text-amber-300 opacity-6" />
    </svg>

    {/* Trophy */}
    <svg className="absolute bottom-[25%] right-[6%] w-12 h-12 doodle-float" style={{ '--rotate': '-2deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 8h20v14c0 6-4 10-10 10s-10-4-10-10z" className="text-amber-400 opacity-8" />
      <path d="M14 12H8c0 6 3 10 6 10" className="text-amber-300 opacity-6" />
      <path d="M34 12h6c0 6-3 10-6 10" className="text-amber-300 opacity-6" />
      <path d="M20 32v4h8v-4" className="text-amber-400 opacity-8" />
      <path d="M16 40h16" className="text-amber-400 opacity-10" />
    </svg>

    {/* Sun */}
    <svg className="absolute bottom-[20%] left-[8%] w-10 h-10 doodle-float doodle-float-delay-1" style={{ '--rotate': '6deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
      <circle cx="20" cy="20" r="8" className="text-amber-400 opacity-8" />
      <path d="M20 4v4M20 32v4M4 20h4M32 20h4M9 9l3 3M28 28l3 3M31 9l-3 3M12 28l-3 3" className="text-amber-300 opacity-6" />
    </svg>

    {/* Briefcase */}
    <svg className="absolute top-[60%] right-[14%] w-10 h-10 doodle-float doodle-float-delay-2" style={{ '--rotate': '-5deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="4" y="14" width="32" height="20" rx="3" className="text-amber-400 opacity-8" />
      <path d="M14 14V10a4 4 0 018 0v4" className="text-amber-300 opacity-6" />
      <path d="M4 22h32" className="text-amber-300 opacity-4" />
      <rect x="17" y="20" width="6" height="4" rx="1" className="text-amber-300 opacity-6" />
    </svg>

    {/* Stars */}
    <svg className="absolute top-[25%] left-[30%] w-3 h-3 doodle-float" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round">
      <path d="M8 1l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" className="text-amber-300 opacity-6" />
    </svg>
    <svg className="absolute bottom-[35%] right-[28%] w-3 h-3 doodle-float doodle-float-delay-1" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round">
      <path d="M8 1l2 5h5l-4 3 2 5-5-3-5 3 2-5-4-3h5z" className="text-amber-400 opacity-8" />
    </svg>
  </div>
);
