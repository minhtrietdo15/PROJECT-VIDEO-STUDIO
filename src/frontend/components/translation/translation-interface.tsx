'use client';

import * as React from 'react';
import { useState } from 'react';
import { Languages, RefreshCw } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { TranscriptEditor, TranscriptSegment } from '@/components/transcript/transcript-editor';

const ENGINES = [
  { value: 'ollama', label: 'Ollama (Local)' },
  { value: 'openai', label: 'OpenAI' },
  { value: 'gemini', label: 'Gemini' },
  { value: 'claude', label: 'Claude' },
] as const;

const STYLES = [
  { value: 'neutral', label: 'Trung tính' },
  { value: 'natural', label: 'Tự nhiên' },
  { value: 'short_video', label: 'Video ngắn' },
  { value: 'educational', label: 'Giáo dục' },
] as const;

export type TranslationEngine = (typeof ENGINES)[number]['value'];
export type TranslationStyle = (typeof STYLES)[number]['value'];

export interface TranslationInterfaceProps {
  /** Original transcript segments */
  segments?: TranscriptSegment[];
  /** Called when translation is requested */
  onTranslate?: (engine: TranslationEngine, style: TranslationStyle) => void;
  /** Translated segments (for side-by-side view) */
  translatedSegments?: TranscriptSegment[];
  /** Loading state for translation */
  isTranslating?: boolean;
  className?: string;
}

export function TranslationInterface({
  segments = [],
  onTranslate,
  translatedSegments = [],
  isTranslating = false,
  className,
}: TranslationInterfaceProps) {
  const [engine, setEngine] = useState<TranslationEngine>('openai');
  const [style, setStyle] = useState<TranslationStyle>('neutral');
  const [viewMode, setViewMode] = useState<'side-by-side' | 'translated-only'>('side-by-side');

  const handleTranslate = () => {
    onTranslate?.(engine, style);
  };

  return (
    <div className={cn('space-y-4', className)}>
      {/* Controls */}
      <div className="flex flex-wrap items-center gap-3 rounded-lg border bg-background p-4">
        <div className="flex items-center gap-2">
          <Languages className="h-4 w-4" />
          <span className="text-sm font-medium">Translation</span>
        </div>

        <div className="flex flex-1 items-center gap-3">
          <select
            value={engine}
            onChange={(e) => setEngine(e.target.value as TranslationEngine)}
            disabled={isTranslating}
            className="rounded border px-2 py-1.5 text-sm"
          >
            {ENGINES.map((en) => (
              <option key={en.value} value={en.value}>
                {en.label}
              </option>
            ))}
          </select>

          <select
            value={style}
            onChange={(e) => setStyle(e.target.value as TranslationStyle)}
            disabled={isTranslating}
            className="rounded border px-2 py-1.5 text-sm"
          >
            {STYLES.map((st) => (
              <option key={st.value} value={st.value}>
                {st.label}
              </option>
            ))}
          </select>

          <div className="flex rounded border">
            <button
              type="button"
              onClick={() => setViewMode('side-by-side')}
              className={cn('px-3 py-1.5 text-xs', viewMode === 'side-by-side' && 'bg-primary text-primary-foreground')}
            >
              Side-by-side
            </button>
            <button
              type="button"
              onClick={() => setViewMode('translated-only')}
              className={cn('px-3 py-1.5 text-xs', viewMode === 'translated-only' && 'bg-primary text-primary-foreground')}
            >
              Translated only
            </button>
          </div>

          <Button type="button" onClick={handleTranslate} disabled={isTranslating || segments.length === 0}>
            {isTranslating ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Translating...
              </>
            ) : (
              <>
                <Languages className="mr-2 h-4 w-4" />
                Translate
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Content */}
      {viewMode === 'side-by-side' ? (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          <div>
            <h3 className="mb-2 text-sm font-medium text-muted-foreground">Original</h3>
            <TranscriptEditor segments={segments} />
          </div>
          <div>
            <h3 className="mb-2 text-sm font-medium text-muted-foreground">Translated</h3>
            <TranscriptEditor segments={translatedSegments} />
          </div>
        </div>
      ) : (
        <div>
          <h3 className="mb-2 text-sm font-medium text-muted-foreground">Translated</h3>
          <TranscriptEditor segments={translatedSegments.length > 0 ? translatedSegments : segments} />
        </div>
      )}
    </div>
  );
}