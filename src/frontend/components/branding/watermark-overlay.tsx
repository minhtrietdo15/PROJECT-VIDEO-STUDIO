'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Upload } from 'lucide-react';

export type WatermarkPosition = 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center';

export interface WatermarkConfig {
  imageUrl?: string;
  position: WatermarkPosition;
  opacity: number; // 0-100
  size: number; // 0-100 (percentage of video width)
  showRange: 'entire' | 'custom';
  startTime?: number; // seconds
  endTime?: number; // seconds
}

export interface WatermarkOverlayProps {
  config: WatermarkConfig;
  onConfigChange?: (config: WatermarkConfig) => void;
  className?: string;
}

const POSITION_PRESETS: { value: WatermarkPosition; label: string }[] = [
  { value: 'top-left', label: 'Top Left' },
  { value: 'top-right', label: 'Top Right' },
  { value: 'bottom-left', label: 'Bottom Left' },
  { value: 'bottom-right', label: 'Bottom Right' },
  { value: 'center', label: 'Center' },
];

export function WatermarkOverlay({
  config,
  onConfigChange,
  className,
}: WatermarkOverlayProps) {
  const updateConfig = (updates: Partial<WatermarkConfig>) => {
    onConfigChange?.({ ...config, ...updates });
  };

  return (
    <div className={cn('space-y-4', className)}>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Logo Image</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-4">
            {config.imageUrl ? (
              <div className="relative h-20 w-20 overflow-hidden rounded-lg border">
                <img
                  src={config.imageUrl}
                  alt="Watermark preview"
                  className="h-full w-full object-contain"
                />
              </div>
            ) : (
              <div className="flex h-20 w-20 items-center justify-center rounded-lg border border-dashed bg-muted">
                <Upload className="h-6 w-6 text-muted-foreground" />
              </div>
            )}
            <Button variant="outline" size="sm">
              <Upload className="mr-2 h-4 w-4" />
              Upload Logo
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Position</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-2">
            {POSITION_PRESETS.map((pos) => (
              <Button
                key={pos.value}
                variant={config.position === pos.value ? 'default' : 'outline'}
                size="sm"
                onClick={() => updateConfig({ position: pos.value })}
              >
                {pos.label}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Opacity: {config.opacity}%</CardTitle>
        </CardHeader>
        <CardContent>
          <input
            type="range"
            min="0"
            max="100"
            value={config.opacity}
            onChange={(e) => updateConfig({ opacity: parseInt(e.target.value) })}
            className="w-full"
          />
          <div className="mt-1 flex justify-between text-xs text-muted-foreground">
            <span>0%</span>
            <span>100%</span>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Size: {config.size}%</CardTitle>
        </CardHeader>
        <CardContent>
          <input
            type="range"
            min="5"
            max="50"
            value={config.size}
            onChange={(e) => updateConfig({ size: parseInt(e.target.value) })}
            className="w-full"
          />
          <div className="mt-1 flex justify-between text-xs text-muted-foreground">
            <span>5%</span>
            <span>50%</span>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Show Range</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2">
            <Button
              variant={config.showRange === 'entire' ? 'default' : 'outline'}
              size="sm"
              onClick={() => updateConfig({ showRange: 'entire' })}
            >
              Entire Video
            </Button>
            <Button
              variant={config.showRange === 'custom' ? 'default' : 'outline'}
              size="sm"
              onClick={() => updateConfig({ showRange: 'custom' })}
            >
              Custom Range
            </Button>
          </div>

          {config.showRange === 'custom' && (
            <div className="grid grid-cols-2 gap-2">
              <div>
                <Label htmlFor="start-time">Start (s)</Label>
                <input
                  id="start-time"
                  type="number"
                  min="0"
                  value={config.startTime || 0}
                  onChange={(e) => updateConfig({ startTime: parseInt(e.target.value) })}
                  className="w-full rounded-md border px-3 py-2"
                />
              </div>
              <div>
                <Label htmlFor="end-time">End (s)</Label>
                <input
                  id="end-time"
                  type="number"
                  min="0"
                  value={config.endTime || 0}
                  onChange={(e) => updateConfig({ endTime: parseInt(e.target.value) })}
                  className="w-full rounded-md border px-3 py-2"
                />
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}