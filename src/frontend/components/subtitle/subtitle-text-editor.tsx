'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';

export interface SubtitleSegmentData {
  id: string;
  start: number; // seconds
  end: number; // seconds
  text: string;
}

export interface SubtitleTextEditorProps {
  segments: SubtitleSegmentData[];
  selectedSegmentId?: string | null;
  onSegmentSelect?: (id: string) => void;
  onSegmentTextChange?: (id: string, text: string) => void;
  onCharacterCountChange?: (id: string, count: number) => void;
  characterLimit?: number;
  className?: string;
}

/**
 * Subtitle text editor with multi-line support and character limit.
 */
export function SubtitleTextEditor({
  segments,
  selectedSegmentId,
  onSegmentSelect,
  onSegmentTextChange,
  characterLimit = 42,
  className,
}: SubtitleTextEditorProps) {
  const selectedSegment = segments.find((s) => s.id === selectedSegmentId);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className={cn('space-y-4', className)}>
      {/* Segment list */}
      <div className="max-h-96 space-y-2 overflow-y-auto">
        {segments.map((segment) => {
          const isSelected = segment.id === selectedSegmentId;
          const charCount = segment.text.length;
          const isOverLimit = charCount > characterLimit;

          return (
            <div
              key={segment.id}
              className={cn(
                'cursor-pointer rounded-lg border p-3 transition-all',
                isSelected ? 'border-primary bg-primary/5' : 'border-border hover:bg-muted/50'
              )}
              onClick={() => onSegmentSelect?.(segment.id)}
            >
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="text-muted-foreground">
                  {formatTime(segment.start)} → {formatTime(segment.end)}
                </span>
                <span
                  className={cn(
                    'text-xs',
                    isOverLimit ? 'text-destructive' : 'text-muted-foreground'
                  )}
                >
                  {charCount}/{characterLimit} chars
                </span>
              </div>
              <Textarea
                value={segment.text}
                onChange={(e) => onSegmentTextChange?.(segment.id, e.target.value)}
                placeholder="Enter subtitle text..."
                className="min-h-20 resize-none"
                maxLength={characterLimit * 2} // Allow some overflow for editing
                onClick={(e) => e.stopPropagation()}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}