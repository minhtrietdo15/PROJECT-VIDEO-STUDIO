'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { ZoomIn, ZoomOut, Scissors, Combine } from 'lucide-react';

export interface SubtitleSegment {
  id: string;
  start: number; // seconds
  end: number; // seconds
  text: string;
}

export interface TimelineProps {
  duration: number; // total video duration in seconds
  segments: SubtitleSegment[];
  selectedSegmentId?: string | null;
  zoomLevel?: 'seconds' | 'minutes';
  onSegmentSelect?: (id: string) => void;
  onSegmentUpdate?: (id: string, start: number, end: number) => void;
  onSegmentSplit?: (id: string, splitTime: number) => void;
  onSegmentMerge?: (ids: string[]) => void;
  className?: string;
}

/**
 * Timeline component for subtitle editing.
 * Supports zoom in/out, drag to adjust timing, split/merge segments.
 */
export function Timeline({
  duration,
  segments,
  selectedSegmentId,
  zoomLevel = 'seconds',
  onSegmentSelect,
  onSegmentUpdate,
  onSegmentSplit,
  onSegmentMerge,
  className,
}: TimelineProps) {
  const [scale, setScale] = React.useState(1);
  const timelineRef = React.useRef<HTMLDivElement>(null);

  const pixelsPerSecond = 100 * scale;
  const timelineWidth = Math.max(duration * pixelsPerSecond, 800);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    const hundredths = Math.floor((seconds % 1) * 100);
    return `${mins}:${secs.toString().padStart(2, '0')}.${hundredths.toString().padStart(2, '0')}`;
  };

  const handleZoomIn = () => setScale((s) => Math.min(s * 1.5, 4));
  const handleZoomOut = () => setScale((s) => Math.max(s / 1.5, 0.25));

  return (
    <div className={cn('space-y-4', className)}>
      {/* Timeline controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleZoomOut}
            aria-label="Zoom out"
          >
            <ZoomOut className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleZoomIn}
            aria-label="Zoom in"
          >
            <ZoomIn className="h-4 w-4" />
          </Button>
          <span className="text-sm text-muted-foreground">
            Zoom: {Math.round(scale * 100)}%
          </span>
        </div>

        <div className="flex items-center gap-2">
          {selectedSegmentId && segments.length > 1 && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                const selectedIds = segments
                  .filter((s) => s.id === selectedSegmentId || Math.abs(segments[0].start - s.start) < 0.1)
                  .map((s) => s.id);
                if (selectedIds.length > 1) {
                  onSegmentMerge?.(selectedIds);
                }
              }}
              aria-label="Merge segments"
            >
              <Combine className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>

      {/* Timeline ruler */}
      <div className="relative h-8 border-b bg-muted/50 text-xs">
        <div
          className="relative h-full"
          style={{ width: `${timelineWidth}px` }}
        >
          {Array.from({ length: Math.floor(duration) + 1 }).map((_, i) => (
            <div
              key={i}
              className="absolute bottom-0 border-l border-muted-foreground/30"
              style={{ left: `${i * pixelsPerSecond}px` }}
            >
              <span className="absolute bottom-0 left-1 text-muted-foreground">
                {formatTime(i)}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Timeline segments */}
      <div
        ref={timelineRef}
        className="relative h-20 overflow-x-auto border bg-background"
        style={{ width: `${timelineWidth}px` }}
      >
        {segments.map((segment) => {
          const left = segment.start * pixelsPerSecond;
          const width = (segment.end - segment.start) * pixelsPerSecond;
          const isSelected = segment.id === selectedSegmentId;

          return (
            <div
              key={segment.id}
              className={cn(
                'absolute top-2 h-16 cursor-pointer rounded border bg-primary/10 transition-all',
                isSelected && 'ring-2 ring-primary'
              )}
              style={{
                left: `${left}px`,
                width: `${width}px`,
              }}
              onClick={() => onSegmentSelect?.(segment.id)}
            >
              <div className="flex h-full flex-col justify-between p-2">
                <span className="text-xs font-medium">{formatTime(segment.start)}</span>
                <span className="line-clamp-1 text-xs">{segment.text}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}