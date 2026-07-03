'use client';

import * as React from 'react';
import { useState } from 'react';
import { Download, X, CheckCircle2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';

const FORMATS = [
  { value: 'mp4', label: 'MP4', ext: '.mp4' },
  { value: 'mov', label: 'MOV', ext: '.mov' },
  { value: 'mkv', label: 'MKV', ext: '.mkv' },
] as const;

const RESOLUTIONS = [
  { value: '1920:1080', label: '1080p (Full HD)' },
  { value: '1280:720', label: '720p (HD)' },
  { value: '854:480', label: '480p (SD)' },
] as const;

const QUALITY_PRESETS = [
  { value: 'fast', label: 'Fast', description: 'Lower quality, faster render' },
  { value: 'balanced', label: 'Balanced', description: 'Good quality, reasonable speed' },
  { value: 'best', label: 'Best', description: 'Highest quality, slower render' },
] as const;

export type ExportFormat = (typeof FORMATS)[number]['value'];
export type Resolution = (typeof RESOLUTIONS)[number]['value'];
export type QualityPreset = (typeof QUALITY_PRESETS)[number]['value'];

export interface ExportConfig {
  format: ExportFormat;
  resolution: Resolution;
  qualityPreset: QualityPreset;
}

export interface ExportConfigurationProps {
  /** Current configuration */
  value?: ExportConfig;
  /** Called when configuration changes */
  onChange?: (config: ExportConfig) => void;
  /** Called when export starts */
  onExport?: (config: ExportConfig) => void;
  /** Called when cancel is requested */
  onCancel?: () => void;
  /** Export progress (0-100) */
  progress?: number;
  /** Export status */
  status?: 'idle' | 'rendering' | 'completed' | 'error';
  /** Error message if any */
  errorMessage?: string;
  /** Disable all controls */
  disabled?: boolean;
  className?: string;
}

export function ExportConfiguration({
  value = { format: 'mp4', resolution: '1920:1080', qualityPreset: 'balanced' },
  onChange,
  onExport,
  onCancel,
  progress = 0,
  status = 'idle',
  errorMessage,
  disabled = false,
  className,
}: ExportConfigurationProps) {
  const [format, setFormat] = useState<ExportFormat>(value.format);
  const [resolution, setResolution] = useState<Resolution>(value.resolution);
  const [qualityPreset, setQualityPreset] = useState<QualityPreset>(value.qualityPreset);

  const updateConfig = (patch: Partial<ExportConfig>) => {
    const next = { format, resolution, qualityPreset, ...patch };
    setFormat(next.format);
    setResolution(next.resolution);
    setQualityPreset(next.qualityPreset);
    onChange?.(next);
  };

  const handleExport = () => {
    onExport?.({ format, resolution, qualityPreset });
  };

  const isRendering = status === 'rendering';
  const isCompleted = status === 'completed';

  return (
    <div className={cn('rounded-lg border bg-background p-4 shadow-sm', className)}>
      <div className="mb-3 flex items-center gap-2">
        <Download className="h-4 w-4" />
        <span className="text-sm font-medium">Export Configuration</span>
      </div>

      {/* Format selector */}
      <div className="mb-4">
        <label className="mb-2 block text-xs font-medium text-muted-foreground">Format</label>
        <div className="flex gap-2">
          {FORMATS.map((fmt) => (
            <button
              key={fmt.value}
              type="button"
              onClick={() => updateConfig({ format: fmt.value })}
              disabled={disabled || isRendering}
              className={cn(
                'rounded border px-3 py-1.5 text-xs transition-colors',
                format === fmt.value ? 'border-primary bg-primary/5' : 'border-border hover:bg-accent/50'
              )}
            >
              {fmt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Resolution selector */}
      <div className="mb-4">
        <label className="mb-2 block text-xs font-medium text-muted-foreground">Resolution</label>
        <select
          value={resolution}
          onChange={(e) => updateConfig({ resolution: e.target.value as Resolution })}
          disabled={disabled || isRendering}
          className="w-full rounded border px-2 py-1.5 text-sm"
        >
          {RESOLUTIONS.map((res) => (
            <option key={res.value} value={res.value}>
              {res.label}
            </option>
          ))}
        </select>
      </div>

      {/* Quality preset selector */}
      <div className="mb-4">
        <label className="mb-2 block text-xs font-medium text-muted-foreground">Quality Preset</label>
        <div className="grid grid-cols-3 gap-2">
          {QUALITY_PRESETS.map((preset) => (
            <button
              key={preset.value}
              type="button"
              onClick={() => updateConfig({ qualityPreset: preset.value })}
              disabled={disabled || isRendering}
              className={cn(
                'rounded border p-2 text-left text-xs transition-colors',
                qualityPreset === preset.value ? 'border-primary bg-primary/5' : 'border-border hover:bg-accent/50'
              )}
            >
              <div className="font-medium">{preset.label}</div>
              <div className="text-muted-foreground">{preset.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Progress display */}
      {(isRendering || isCompleted) && (
        <div className="mb-4">
          <div className="mb-1 flex items-center justify-between text-xs">
            <span className="font-medium">
              {isRendering ? 'Rendering...' : isCompleted ? 'Completed' : 'Error'}
            </span>
            <span>{Math.round(progress)}%</span>
          </div>
          <Progress value={progress} className="h-2" />
          {errorMessage && <p className="mt-1 text-xs text-red-500">{errorMessage}</p>}
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-2">
        {!isRendering && !isCompleted && (
          <Button type="button" onClick={handleExport} disabled={disabled} className="flex-1">
            <Download className="mr-2 h-4 w-4" />
            Export Video
          </Button>
        )}

        {isRendering && (
          <Button type="button" variant="destructive" onClick={onCancel} className="flex-1">
            <X className="mr-2 h-4 w-4" />
            Cancel
          </Button>
        )}

        {isCompleted && (
          <Button type="button" className="flex-1">
            <CheckCircle2 className="mr-2 h-4 w-4" />
            Download
          </Button>
        )}
      </div>
    </div>
  );
}