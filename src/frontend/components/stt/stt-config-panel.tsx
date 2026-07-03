'use client';

import * as React from 'react';
import { useState } from 'react';
import { Settings2 } from 'lucide-react';
import { cn } from '@/lib/utils';

const MODEL_SIZES = [
  { value: 'tiny', label: 'Tiny' },
  { value: 'base', label: 'Base' },
  { value: 'small', label: 'Small' },
  { value: 'medium', label: 'Medium' },
  { value: 'large', label: 'Large' },
] as const;

const LANGUAGES = [
  { value: 'auto', label: 'Auto detect' },
  { value: 'en', label: 'English' },
  { value: 'vi', label: 'Vietnamese' },
  { value: 'zh', label: 'Chinese' },
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'ja', label: 'Japanese' },
  { value: 'ko', label: 'Korean' },
] as const;

export type ModelSize = (typeof MODEL_SIZES)[number]['value'];
export type Language = (typeof LANGUAGES)[number]['value'];

export interface STTConfig {
  modelSize: ModelSize;
  language: Language;
}

export interface STTConfigPanelProps {
  /** Current configuration */
  value?: STTConfig;
  /** Called when configuration changes */
  onChange?: (config: STTConfig) => void;
  /** Disable all controls */
  disabled?: boolean;
  className?: string;
}

export function STTConfigPanel({
  value = { modelSize: 'base', language: 'auto' },
  onChange,
  disabled = false,
  className,
}: STTConfigPanelProps) {
  const [modelSize, setModelSize] = useState<ModelSize>(value.modelSize);
  const [language, setLanguage] = useState<Language>(value.language);

  const handleModelSizeChange = (next: ModelSize) => {
    setModelSize(next);
    onChange?.({ modelSize: next, language });
  };

  const handleLanguageChange = (next: Language) => {
    setLanguage(next);
    onChange?.({ modelSize, language: next });
  };

  return (
    <div className={cn('rounded-lg border bg-background p-4 shadow-sm', className)}>
      <div className="mb-3 flex items-center gap-2">
        <Settings2 className="h-4 w-4" />
        <span className="text-sm font-medium">STT Configuration</span>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-muted-foreground">Whisper model size</label>
          <select
            value={modelSize}
            onChange={(e) => handleModelSizeChange(e.target.value as ModelSize)}
            disabled={disabled}
            className="rounded border px-2 py-1.5 text-sm"
          >
            {MODEL_SIZES.map((m) => (
              <option key={m.value} value={m.value}>
                {m.label}
              </option>
            ))}
          </select>
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-muted-foreground">Language</label>
          <select
            value={language}
            onChange={(e) => handleLanguageChange(e.target.value as Language)}
            disabled={disabled}
            className="rounded border px-2 py-1.5 text-sm"
          >
            {LANGUAGES.map((l) => (
              <option key={l.value} value={l.value}>
                {l.label}
              </option>
            ))}
          </select>
        </div>
      </div>
      <p className="mt-3 text-xs text-muted-foreground">
        Larger models improve accuracy but require more GPU/CPU resources and time.
      </p>
    </div>
  );
}