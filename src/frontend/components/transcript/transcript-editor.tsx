'use client';

import * as React from 'react';
import { useState } from 'react';
import { Play, Scissors, Text } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

/**
 * Represents a transcript segment from the backend STT service.
 */
export interface TranscriptSegment {
  id: string;
  start: number; // seconds
  end: number;   // seconds
  text: string;
}

export interface TranscriptEditorProps {
  /** Video duration in seconds (for playback sync/timeline). */
  videoDuration?: number;
  /** Current playback time in seconds (controlled or uncontrolled). */
  currentTime?: number;
  /** Called when the user seeks to a new time. */
  onSeek?: (time: number) => void;
  /** Initial segments to display/edit. */
  segments?: TranscriptSegment[];
  /** Called with updated segments after edits. */
  onChange?: (segments: TranscriptSegment[]) => void;
  className?: string;
}

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.floor((seconds - Math.floor(seconds)) * 100);
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}.${ms.toString().padStart(2, '0')}`;
}

export function TranscriptEditor({
  videoDuration,
  currentTime: controlledCurrentTime,
  onSeek,
  segments = [],
  onChange,
  className,
}: TranscriptEditorProps) {
  const [internalTime, setInternalTime] = useState(0);
  const currentTime = controlledCurrentTime ?? internalTime;

  const handleSeek = (time: number) => {
    setInternalTime(time);
    onSeek?.(time);
  };

  const handleTextChange = (id: string, text: string) => {
    const next = segments.map((seg) => (seg.id === id ? { ...seg, text } : seg));
    onChange?.(next);
  };

  const handleBoundaryChange = (id: string, field: 'start' | 'end', value: number) => {
    const next = segments.map((seg) =>
      seg.id === id ? { ...seg, [field]: Math.max(0, value) } : seg
    );
    onChange?.(next);
  };

  const togglePlayPause = () => {
    // In a real implementation, this would toggle video playback via a media ref.
    // Placeholder action for now.
    console.log('toggle play/pause');
  };

  return (
    <div className={cn('rounded-lg border bg-background shadow-sm', className)}>
      {/* Header / Toolbar */}
      <div className="flex items-center justify-between border-b px-4 py-2">
        <div className="flex items-center gap-2">
          <Text className="h-4 w-4" />
          <span className="text-sm font-medium">Transcript Editor</span>
        </div>
        <div className="flex items-center gap-2">
          <Button type="button" variant="ghost" size="icon" onClick={togglePlayPause} aria-label="Play/Pause">
            <Play className="h-4 w-4" />
          </Button>
          <span className="text-xs text-muted-foreground">
            {formatTime(currentTime)} / {videoDuration ? formatTime(videoDuration) : '--:--.--'}
          </span>
        </div>
      </div>

      {/* Segments list */}
      <div className="max-h-[50vh] overflow-auto">
        {segments.length === 0 && (
          <div className="p-6 text-center text-sm text-muted-foreground">
            Chưa có transcript. Hãy upload video và chạy STT để tạo transcript.
          </div>
        )}
        <ul className="divide-y">
          {segments.map((segment) => {
            const active = currentTime >= segment.start && currentTime < segment.end;
            return (
              <li
                key={segment.id}
                className={cn(
                  'flex flex-col gap-2 px-4 py-3 transition-colors',
                  active ? 'bg-primary/5' : 'bg-background'
                )}
              >
                <div className="flex items-center gap-3">
                  <Scissors className="h-4 w-4 shrink-0 text-muted-foreground" />
                  <div className="flex items-center gap-2 text-xs tabular-nums text-muted-foreground">
                    <input
                      type="number"
                      step="0.01"
                      value={segment.start}
                      onChange={(e) =>
                        handleBoundaryChange(segment.id, 'start', Number(e.target.value))
                      }
                      className="w-16 rounded border px-2 py-1"
                      aria-label="Start time"
                    />
                    <span>→</span>
                    <input
                      type="number"
                      step="0.01"
                      value={segment.end}
                      onChange={(e) =>
                        handleBoundaryChange(segment.id, 'end', Number(e.target.value))
                      }
                      className="w-16 rounded border px-2 py-1"
                      aria-label="End time"
                    />
                  </div>
                  <div className="ml-auto flex items-center gap-1">
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      onClick={() => handleSeek(segment.start)}
                      aria-label="Play segment"
                    >
                      <Play className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </div>
                <textarea
                  value={segment.text}
                  onChange={(e) => handleTextChange(segment.id, e.target.value)}
                  className="w-full rounded border px-3 py-2 text-sm"
                  rows={2}
                />
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}