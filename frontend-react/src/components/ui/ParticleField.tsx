import React, { useEffect, useRef, useCallback } from 'react';
import { cn } from '../../lib/cn';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  opacity: number;
  color: string;
  life: number;
  maxLife: number;
}

interface ParticleFieldProps {
  className?: string;
  particleCount?: number;
  colors?: string[];
  connectionDistance?: number;
  speed?: number;
}

export const ParticleField: React.FC<ParticleFieldProps> = ({
  className,
  particleCount = 60,
  colors = ['#3b82f6', '#8b5cf6', '#06b6d4', '#6366f1'],
  connectionDistance = 140,
  speed = 0.4,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animFrameRef = useRef<number>(0);
  const mouseRef = useRef({ x: -1000, y: -1000 });

  const createParticle = useCallback((canvas: HTMLCanvasElement): Particle => {
    const color = colors[Math.floor(Math.random() * colors.length)];
    const life = Math.random() * 300 + 200;
    const w = canvas.offsetWidth || 0;
    const h = canvas.offsetHeight || 0;
    return {
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * speed,
      vy: (Math.random() - 0.5) * speed,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.6 + 0.1,
      color,
      life,
      maxLife: life,
    };
  }, [colors, speed]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const resize = () => {
      canvas.width = canvas.offsetWidth * window.devicePixelRatio;
      canvas.height = canvas.offsetHeight * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    };

    resize();
    particlesRef.current = Array.from({ length: particleCount }, () => createParticle(canvas));

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouseRef.current = { x: e.clientX - rect.left, y: e.clientY - rect.top };
    };

    canvas.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('resize', resize);

    const draw = () => {
      const w = canvas.offsetWidth;
      const h = canvas.offsetHeight;
      ctx.clearRect(0, 0, w, h);

      particlesRef.current.forEach((p, i) => {
        // Mouse repulsion
        const dx = p.x - mouseRef.current.x;
        const dy = p.y - mouseRef.current.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > 0 && dist < 80) {
          const force = (80 - dist) / 80;
          p.vx += (dx / dist) * force * 0.3;
          p.vy += (dy / dist) * force * 0.3;
        }

        // Dampen velocity
        p.vx *= 0.99;
        p.vy *= 0.99;

        p.x += p.vx;
        p.y += p.vy;
        p.life--;

        if (p.x < 0 || p.x > w || p.y < 0 || p.y > h || p.life <= 0) {
          particlesRef.current[i] = createParticle(canvas);
          return;
        }

        const lifeRatio = p.life / p.maxLife;
        const opacity = p.opacity * Math.sin(lifeRatio * Math.PI);

        // Draw connections
        for (let j = i + 1; j < particlesRef.current.length; j++) {
          const q = particlesRef.current[j];
          const dx2 = p.x - q.x;
          const dy2 = p.y - q.y;
          const d2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);
          if (d2 < connectionDistance) {
            const alpha = (1 - d2 / connectionDistance) * 0.12;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.strokeStyle = `${p.color}${Math.round(alpha * 255).toString(16).padStart(2, '0')}`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }

        // Draw particle
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `${p.color}${Math.round(opacity * 255).toString(16).padStart(2, '0')}`;
        ctx.fill();
      });

      animFrameRef.current = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animFrameRef.current);
      canvas.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', resize);
    };
  }, [particleCount, connectionDistance, createParticle]);

  return (
    <canvas
      ref={canvasRef}
      className={cn('w-full h-full', className)}
      style={{ display: 'block' }}
    />
  );
};
