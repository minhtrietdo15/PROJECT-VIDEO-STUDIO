'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Music, Upload, Repeat, Play, Square } from 'lucide-react';

export interface BackgroundMusicConfig {
  fileUrl?: string;
  fileName?: string;
  volume: number; // 0-100 (music vs voice mix)
  loop: boolean;
  fadeIn: boolean;
  fadeOut: boolean;
}

export interface BackgroundMusicProps {
  config: BackgroundMusicConfig;
  onConfigChange?: (config: BackgroundMusicConfig) => void;
  className?: string;
}

export function BackgroundMusic({
  config,
  onConfigChange,
  className,
}: BackgroundMusicProps) {
  const updateConfig = (updates: Partial<BackgroundMusicConfig>) => {
    onConfigChange?.({ ...config, ...updates });
  };

  return (
    <div className={cn('space-y-4', className)}>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Music File</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Upload className="mr-2 h-4 w-4" />
              {config.fileUrl ? 'Change Music' : 'Upload Music'}
            </Button>
            {config.fileName && (
              <span className="text-sm text-muted-foreground">{config.fileName}</span>
            )}
          </div>

          {config.fileUrl && (
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm">
                <Play className="h-4 w-4" />
              </Button>
              <div className="h-2 flex-1 rounded-full bg-muted">
                <div className="h-full w-0 rounded-full bg-primary" />
              </div>
              <Button variant="ghost" size="sm">
                <Square className="h-4 w-4" />
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Volume Mix: {config.volume}%</CardTitle>
        </CardHeader>
        <CardContent>
          <input
            type="range"
            min="0"
            max="100"
            value={config.volume}
            onChange={(e) => updateConfig({ volume: parseInt(e.target.value) })}
            className="w-full"
          />
          <div className="mt-1 flex justify-between text-xs text-muted-foreground">
            <span>Music only</span>
            <span>Voice only</span>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Options</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <input
              id="loop"
              type="checkbox"
              checked={config.loop}
              onChange={(e) => updateConfig({ loop: e.target.checked })}
              className="h-4 w-4"
            />
            <Label htmlFor="loop" className="flex items-center gap-2">
              <Repeat className="h-4 w-4" /> Loop Music
            </Label>
          </div>
          <div className="flex items-center gap-2">
            <input
              id="fade-in"
              type="checkbox"
              checked={config.fadeIn}
              onChange={(e) => updateConfig({ fadeIn: e.target.checked })}
              className="h-4 w-4"
            />
            <Label htmlFor="fade-in">Fade In</Label>
          </div>
          <div className="flex items-center gap-2">
            <input
              id="fade-out"
              type="checkbox"
              checked={config.fadeOut}
              onChange={(e) => updateConfig({ fadeOut: e.target.checked })}
              className="h-4 w-4"
            />
            <Label htmlFor="fade-out">Fade Out</Label>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}