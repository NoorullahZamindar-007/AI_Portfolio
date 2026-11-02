'use client';
import { useEffect } from 'react';
import fluidCursor from '@/hooks/use-FluidCursor';

const FluidCursor = () => {
  useEffect(() => {
    // The cursor animation is purely decorative: skip it for users who
    // asked the OS for reduced motion instead of animating regardless.
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      return;
    }
    const cleanup = fluidCursor();
    return () => {
      if (cleanup) cleanup();
    };
  }, []);

  return (
    <div className="fixed inset-0 -z-50 pointer-events-none">
      <canvas id="fluid" className="fixed top-0 left-0 w-full h-full z-50 pointer-events-none" />
    </div>
  );
};

export default FluidCursor;
