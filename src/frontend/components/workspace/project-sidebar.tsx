'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Settings, Film, Clock, HardDrive } from 'lucide-react';

export interface VideoInfo {
  filename: string;
  duration: number;
  resolution: string;
  fps: number;
  size: number;
}

export interface ProjectSettings {
  title: string;
  sourceLang: string;
  targetLang: string;
}

export interface ProjectSidebarProps {
  videoInfo?: VideoInfo;
  settings?: ProjectSettings;
  showSettings?: boolean;
  onOpenSettings?: () => void;
  className?: string;
}

/**
 * Project workspace sidebar showing video info, timeline preview, and settings.
 */
export function ProjectSidebar({
  videoInfo,
  settings,
  showSettings = false,
  onOpenSettings,
  className,
}: ProjectSidebarProps) {
  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatSize = (bytes: number) => {
    const mb = bytes / (1024 * 1024);
    return `${mb.toFixed(1)} MB`;
  };

  return (
    <aside
      className={cn(
        'flex w-80 flex-col gap-4 overflow-y-auto border-r bg-muted/30 p-4',
        className
      )}
    >
      {/* Video Info Card */}
      {videoInfo && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <Film className="h-4 w-4" />
              Video Info
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div>
              <span className="text-muted-foreground">Filename:</span>
              <p className="truncate font-medium">{videoInfo.filename}</p>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4 text-muted-foreground" />
              <span>{formatDuration(videoInfo.duration)}</span>
            </div>
            <div>
              <span className="text-muted-foreground">Resolution:</span>
              <span className="ml-2">{videoInfo.resolution}</span>
            </div>
            <div>
              <span className="text-muted-foreground">FPS:</span>
              <span className="ml-2">{videoInfo.fps}</span>
            </div>
            <div className="flex items-center gap-2">
              <HardDrive className="h-4 w-4 text-muted-foreground" />
              <span>{formatSize(videoInfo.size)}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Timeline Preview (placeholder) */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Timeline</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-32 rounded-md bg-muted">
            <div className="flex h-full items-center justify-center text-xs text-muted-foreground">
              Timeline visualization coming soon
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Settings */}
      {settings && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <Settings className="h-4 w-4" />
              Project Settings
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div>
              <span className="text-muted-foreground">Source:</span>
              <span className="ml-2">{settings.sourceLang}</span>
            </div>
            <div>
              <span className="text-muted-foreground">Target:</span>
              <span className="ml-2">{settings.targetLang}</span>
            </div>
            <Button
              variant="outline"
              size="sm"
              className="w-full"
              onClick={onOpenSettings}
            >
              Edit Settings
            </Button>
          </CardContent>
        </Card>
      )}
    </aside>
  );
}