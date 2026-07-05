'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Check, Clock } from 'lucide-react';

export interface AutoSaveIndicatorProps {
  status: 'idle' | 'saving' | 'saved' | 'error';
  lastSaved?: Date | null;
  className?: string;
}

/**
 * Auto-save indicator showing save status.
 */
export function AutoSaveIndicator({
  status,
  lastSaved,
  className,
}: AutoSaveIndicatorProps) {
  const getStatusContent = () => {
    switch (status) {
      case 'saving':
        return (
          <>
            <Clock className="h-3 w-3 animate-pulse" />
            <span>Saving...</span>
          </>
        );
      case 'saved':
        return (
          <>
            <Check className="h-3 w-3" />
            <span>Saved{lastSaved && ` • ${lastSaved.toLocaleTimeString()}`}</span>
          </>
        );
      case 'error':
        return (
          <>
            <span className="h-3 w-3 rounded-full bg-destructive" />
            <span>Save failed</span>
          </>
        );
      default:
        return (
          <>
            <span className="h-3 w-3 rounded-full bg-muted" />
            <span>All changes saved</span>
          </>
        );
    }
  };

  return (
    <div
      className={cn(
        'inline-flex items-center gap-1.5 text-xs text-muted-foreground',
        className
      )}
      aria-live="polite"
    >
      {getStatusContent()}
    </div>
  );
}