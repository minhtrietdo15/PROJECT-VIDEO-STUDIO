'use client';

import * as React from 'react';
import { useState } from 'react';
import { Play, Pause, Volume2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

const VOICES = [
  { id: 'v1', name: 'Nam - Miền Bắc', gender: 'male', accent: 'Northern' },
  { id: 'v2', name: 'Nữ - Miền Bắc', gender: 'female', accent: 'Northern' },
  { id: 'v3', name: 'Nam - Miền Nam', gender: 'male', accent: 'Southern' },
  { id: 'v4', name: 'Nữ - Miền Nam', gender: 'female', accent: 'Southern' },
  { id: 'v5', name: 'Trung tính', gender: 'neutral', accent: 'Central' },
] as const;

export interface VoiceConfig {
  voiceId: string;
  speed: number;
  pitch: number;
  volume: number;
}

export interface VoiceConfigurationProps {
  /** Current configuration */
  value?: VoiceConfig;
  /** Called when configuration changes */
  onChange?: (config: VoiceConfig) => void;
  /** Disable all controls */
  disabled?: boolean;
  className?: string;
}

export function VoiceConfiguration({
  value = { voiceId: 'v1', speed: 1.0, pitch: 1.0, volume: 1.0 },
  onChange,
  disabled = false,
  className,
}: VoiceConfigurationProps) {
  const [voiceId, setVoiceId] = useState(value.voiceId);
  const [speed, setSpeed] = useState(value.speed);
  const [pitch, setPitch] = useState(value.pitch);
  const [volume, setVolume] = useState(value.volume);
  const [isPlaying, setIsPlaying] = useState(false);

  const updateConfig = (patch: Partial<VoiceConfig>) => {
    const next = { voiceId, speed, pitch, volume, ...patch };
    setVoiceId(next.voiceId);
    setSpeed(next.speed);
    setPitch(next.pitch);
    setVolume(next.volume);
    onChange?.(next);
  };

  const togglePlayPause = () => {
    setIsPlaying((prev) => !prev);
  };

  return (
    <div className={cn('rounded-lg border bg-background p-4 shadow-sm', className)}>
      <div className="mb-3 flex items-center gap-2">
        <Volume2 className="h-4 w-4" />
        <span className="text-sm font-medium">Voice Configuration</span>
      </div>

      {/* Voice selector grid */}
      <div className="mb-4">
        <label className="mb-2 block text-xs font-medium text-muted-foreground">Select Voice</label>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 md:grid-cols-5">
          {VOICES.map((voice) => (
            <button
              key={voice.id}
              type="button"
              onClick={() => updateConfig({ voiceId: voice.id })}
              disabled={disabled}
              className={cn(
                'rounded border p-2 text-left text-xs transition-colors',
                voiceId === voice.id ? 'border-primary bg-primary/5' : 'border-border hover:bg-accent/50'
              )}
            >
              <div className="font-medium">{voice.name}</div>
              <div className="text-muted-foreground">{voice.accent}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Sliders */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-muted-foreground">Speed: {speed.toFixed(2)}x</label>
          <input
            type="range"
            min="0.5"
            max="2.0"
            step="0.05"
            value={speed}
            onChange={(e) => updateConfig({ speed: Number(e.target.value) })}
            disabled={disabled}
            className="w-full"
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-muted-foreground">Pitch: {pitch.toFixed(2)}x</label>
          <input
            type="range"
            min="0.5"
            max="2.0"
            step="0.05"
            value={pitch}
            onChange={(e) => updateConfig({ pitch: Number(e.target.value) })}
            disabled={disabled}
            className="w-full"
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-muted-foreground">Volume: {Math.round(volume * 100)}%</label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={volume}
            onChange={(e) => updateConfig({ volume: Number(e.target.value) })}
            disabled={disabled}
            className="w-full"
          />
        </div>
      </div>

      {/* Audio waveform preview (placeholder) */}
      <div className="mt-4">
        <div className="flex items-center gap-2">
          <Button type="button" variant="ghost" size="icon" onClick={togglePlayPause} aria-label="Play/Pause">
            {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          </Button>
          <div className="h-8 flex-1 rounded border bg-muted/50">
            <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
              Audio waveform preview (placeholder)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}