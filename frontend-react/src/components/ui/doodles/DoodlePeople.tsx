import React from 'react';
import { cn } from '../../../lib/cn';

interface DoodleProps {
  className?: string;
}

export const DoodlePeople: React.FC<DoodleProps> = ({ className }) => (
  <div className={cn('absolute inset-0 overflow-hidden pointer-events-none', className)}>
    {/* Person Silhouette */}
    <svg className="absolute top-[8%] left-[5%] w-12 h-12 doodle-float" style={{ '--rotate': '2deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="24" cy="14" r="8" className="text-emerald-400 opacity-10" />
      <path d="M8 42c0-8 7-16 16-16s16 8 16 16" className="text-emerald-400 opacity-8" />
    </svg>

    {/* Phone */}
    <svg className="absolute top-[12%] right-[6%] w-10 h-10 doodle-float doodle-float-delay-1" style={{ '--rotate': '-6deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="8" y="4" width="24" height="32" rx="3" className="text-emerald-400 opacity-8" />
      <path d="M8 30h24" className="text-emerald-300 opacity-6" />
      <circle cx="20" cy="34" r="2" className="text-emerald-300 opacity-6" />
      <path d="M16 8h8" className="text-emerald-300 opacity-4" />
    </svg>

    {/* Email Envelope */}
    <svg className="absolute top-[45%] left-[3%] w-12 h-12 doodle-float doodle-float-delay-2" style={{ '--rotate': '5deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="4" y="10" width="40" height="28" rx="3" className="text-emerald-400 opacity-8" />
      <path d="M4 10l20 16 20-16" className="text-emerald-400 opacity-10" />
    </svg>

    {/* Building */}
    <svg className="absolute bottom-[20%] right-[5%] w-12 h-12 doodle-float" style={{ '--rotate': '-3deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="8" y="8" width="32" height="36" rx="2" className="text-emerald-400 opacity-8" />
      <path d="M8 8l16-4 16 4" className="text-emerald-300 opacity-6" />
      <rect x="14" y="16" width="6" height="6" rx="1" className="text-emerald-300 opacity-6" />
      <rect x="28" y="16" width="6" height="6" rx="1" className="text-emerald-300 opacity-6" />
      <rect x="14" y="28" width="6" height="6" rx="1" className="text-emerald-300 opacity-6" />
      <rect x="28" y="28" width="6" height="6" rx="1" className="text-emerald-300 opacity-6" />
      <rect x="20" y="36" width="8" height="8" rx="1" className="text-emerald-400 opacity-8" />
    </svg>

    {/* ID Badge */}
    <svg className="absolute bottom-[25%] left-[8%] w-10 h-10 doodle-float doodle-float-delay-1" style={{ '--rotate': '4deg' } as React.CSSProperties} viewBox="0 0 40 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="6" y="6" width="28" height="28" rx="3" className="text-emerald-400 opacity-8" />
      <circle cx="20" cy="16" r="5" className="text-emerald-300 opacity-6" />
      <path d="M12 28c0-4 3.6-7 8-7s8 3 8 7" className="text-emerald-300 opacity-6" />
      <path d="M16 4h8" className="text-emerald-300 opacity-4" />
    </svg>

    {/* Handshake */}
    <svg className="absolute top-[55%] right-[12%] w-12 h-12 doodle-float doodle-float-delay-2" style={{ '--rotate': '-4deg' } as React.CSSProperties} viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 20l8-8 8 4 8-8 8 4 8-4" className="text-emerald-400 opacity-8" />
      <path d="M12 12l8 8-4 8" className="text-emerald-300 opacity-6" />
      <path d="M36 12l-8 8 4 8" className="text-emerald-300 opacity-6" />
      <path d="M20 28l4 8 4-8" className="text-emerald-400 opacity-8" />
    </svg>

    {/* Dotted Curve */}
    <svg className="absolute top-[35%] right-[3%] w-20 h-10 doodle-float" viewBox="0 0 80 40" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="3 4">
      <path d="M4 36C20 4 60 4 76 36" className="text-emerald-300 opacity-5" />
    </svg>
  </div>
);
