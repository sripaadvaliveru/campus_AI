import React from 'react';
import { cn } from '../../lib/cn';

interface DoodleBannerProps {
  className?: string;
}

/**
 * Hand-drawn education doodle SVG background for Dashboard hero.
 * All paths in #DBEAFE (very light blue), opacity 0.8.
 */
export const DoodleBanner: React.FC<DoodleBannerProps> = ({ className }) => (
  <div className={cn('absolute inset-0 overflow-hidden pointer-events-none', className)}>
    {/* Background */}
    <div className="absolute inset-0 bg-gradient-to-br from-amber-50/80 via-[#FBF8F3] to-amber-50/40" />

    {/* Doodle SVG layer */}
    <svg
      className="absolute inset-0 w-full h-full"
      viewBox="0 0 1200 500"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="xMidYMid slice"
    >
      {/* Graduation Cap - top left */}
      <g opacity="0.6" transform="translate(80, 60)">
        <path d="M40 20 L80 0 L120 20 L80 40 Z" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M60 30 L60 55 Q80 65 100 55 L100 30" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M120 20 L120 45" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <circle cx="120" cy="48" r="3" fill="#F5C87A" />
      </g>

      {/* Open Book - top right */}
      <g opacity="0.5" transform="translate(950, 50)">
        <path d="M10 50 Q50 10 100 50 Q150 10 190 50" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M100 50 L100 70" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M25 55 Q55 30 95 55" stroke="#FBE9B5" strokeWidth="1.5" fill="none" strokeLinecap="round" />
        <path d="M105 55 Q145 30 175 55" stroke="#FBE9B5" strokeWidth="1.5" fill="none" strokeLinecap="round" />
      </g>

      {/* Pencil - left center */}
      <g opacity="0.5" transform="translate(50, 250)">
        <path d="M20 80 L60 0 L80 20 L40 100 Z" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M40 100 L30 120 L50 100" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M60 0 L80 20" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
      </g>

      {/* Lightbulb - right center */}
      <g opacity="0.5" transform="translate(1050, 200)">
        <path d="M50 10 Q80 10 80 40 Q80 60 65 70 L65 85 L35 85 L35 70 Q20 60 20 40 Q20 10 50 10 Z" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M40 90 L60 90" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M42 95 L58 95" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M50 10 L50 0" stroke="#FBE9B5" strokeWidth="1.5" fill="none" strokeLinecap="round" />
        <path d="M80 25 L90 20" stroke="#FBE9B5" strokeWidth="1.5" fill="none" strokeLinecap="round" />
        <path d="M20 25 L10 20" stroke="#FBE9B5" strokeWidth="1.5" fill="none" strokeLinecap="round" />
      </g>

      {/* Calculator - bottom left */}
      <g opacity="0.4" transform="translate(150, 380)">
        <rect x="10" y="0" width="50" height="70" rx="5" stroke="#F5C87A" strokeWidth="2" fill="none" />
        <rect x="18" y="8" width="34" height="14" rx="2" stroke="#FBE9B5" strokeWidth="1.5" fill="none" />
        <circle cx="22" cy="35" r="3" stroke="#FBE9B5" strokeWidth="1.5" fill="none" />
        <circle cx="35" cy="35" r="3" stroke="#FBE9B5" strokeWidth="1.5" fill="none" />
        <circle cx="48" cy="35" r="3" stroke="#FBE9B5" strokeWidth="1.5" fill="none" />
        <circle cx="22" cy="50" r="3" stroke="#FBE9B5" strokeWidth="1.5" fill="none" />
        <circle cx="35" cy="50" r="3" stroke="#FBE9B5" strokeWidth="1.5" fill="none" />
        <circle cx="48" cy="50" r="3" stroke="#FBE9B5" strokeWidth="1.5" fill="none" />
      </g>

      {/* Atom - bottom right */}
      <g opacity="0.4" transform="translate(900, 350)">
        <ellipse cx="60" cy="60" rx="55" ry="20" stroke="#F5C87A" strokeWidth="1.5" fill="none" transform="rotate(-30 60 60)" />
        <ellipse cx="60" cy="60" rx="55" ry="20" stroke="#F5C87A" strokeWidth="1.5" fill="none" transform="rotate(30 60 60)" />
        <ellipse cx="60" cy="60" rx="55" ry="20" stroke="#F5C87A" strokeWidth="1.5" fill="none" transform="rotate(90 60 60)" />
        <circle cx="60" cy="60" r="5" fill="#F5C87A" />
      </g>

      {/* Diploma Scroll - center */}
      <g opacity="0.35" transform="translate(550, 400)">
        <path d="M20 10 Q10 10 10 20 L10 60 Q10 70 20 70 L90 70 Q100 70 100 60 L100 20 Q100 10 90 10 Z" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M10 20 Q5 20 5 30" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M100 20 Q105 20 105 30" stroke="#F5C87A" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M30 30 L80 30" stroke="#FBE9B5" strokeWidth="1.5" fill="none" strokeLinecap="round" />
        <path d="M30 42 L70 42" stroke="#FBE9B5" strokeWidth="1.5" fill="none" strokeLinecap="round" />
        <path d="M30 54 L60 54" stroke="#FBE9B5" strokeWidth="1.5" fill="none" strokeLinecap="round" />
      </g>

      {/* E=mc² - top center */}
      <g opacity="0.3" transform="translate(500, 40)">
        <text fontFamily="serif" fontSize="28" fontStyle="italic" fill="#F5C87A">E=mc²</text>
      </g>

      {/* Stars scattered */}
      <g opacity="0.4">
        <path d="M300 80 L305 95 L320 95 L308 105 L312 120 L300 110 L288 120 L292 105 L280 95 L295 95 Z" stroke="#F5C87A" strokeWidth="1.5" fill="none" />
        <path d="M800 120 L803 128 L812 128 L805 133 L807 141 L800 136 L793 141 L795 133 L788 128 L797 128 Z" stroke="#FBE9B5" strokeWidth="1" fill="none" />
        <path d="M700 420 L703 428 L712 428 L705 433 L707 441 L700 436 L693 441 L695 433 L688 428 L697 428 Z" stroke="#FBE9B5" strokeWidth="1" fill="none" />
      </g>

      {/* Dotted curves */}
      <g opacity="0.3">
        <path d="M200 150 Q400 100 600 150" stroke="#F5C87A" strokeWidth="1.5" strokeDasharray="4 6" fill="none" />
        <path d="M600 350 Q800 300 1000 350" stroke="#FBE9B5" strokeWidth="1.5" strokeDasharray="4 6" fill="none" />
      </g>
    </svg>
  </div>
);
