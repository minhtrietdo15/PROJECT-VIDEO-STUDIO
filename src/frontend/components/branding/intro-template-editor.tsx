'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Upload, Music, Save } from 'lucide-react';

export interface IntroTemplate {
  logoUrl?: string;
  channelName: string;
  animationStyle: 'fade' | 'slide' | 'zoom' | 'reveal';
  duration: number; // seconds (3-15)
  musicUrl?: string;
  fadeIn: boolean;
  fadeOut: boolean;
}

export interface IntroTemplateEditorProps {
  template: IntroTemplate;
  onTemplateChange?: (template: IntroTemplate) => void;
  onSave?: () => void;
  className?: string;
}

const ANIMATION_STYLES = [
  { value: 'fade', label: 'Fade In' },
  { value: 'slide', label: 'Slide In' },
  { value: 'zoom', label: 'Zoom In' },
  { value: 'reveal', label: 'Reveal' },
] as const;

export function IntroTemplateEditor({
  template,
  onTemplateChange,
  onSave,
  className,
}: IntroTemplateEditorProps) {
  const updateTemplate = (updates: Partial<IntroTemplate>) => {
    onTemplateChange?.({ ...template, ...updates });
  };

  return (
    <div className={cn('space-y-4', className)}>
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Logo</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-4">
            {template.logoUrl ? (
              <div className="relative h-20 w-20 overflow-hidden rounded-lg border">
                <img
                  src={template.logoUrl}
                  alt="Logo preview"
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
          <CardTitle className="text-base">Channel Name</CardTitle>
        </CardHeader>
        <CardContent>
          <Input
            value={template.channelName}
            onChange={(e) => updateTemplate({ channelName: e.target.value })}
            placeholder="Enter your channel name..."
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Animation Style</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {ANIMATION_STYLES.map((style) => (
              <Button
                key={style.value}
                variant={template.animationStyle === style.value ? 'default' : 'outline'}
                size="sm"
                onClick={() => updateTemplate({ animationStyle: style.value })}
              >
                {style.label}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Duration: {template.duration}s</CardTitle>
        </CardHeader>
        <CardContent>
          <input
            type="range"
            min="3"
            max="15"
            value={template.duration}
            onChange={(e) => updateTemplate({ duration: parseInt(e.target.value) })}
            className="w-full"
          />
          <div className="mt-1 flex justify-between text-xs text-muted-foreground">
            <span>3s</span>
            <span>15s</span>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Background Music</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Music className="mr-2 h-4 w-4" />
              {template.musicUrl ? 'Change Music' : 'Upload Music'}
            </Button>
            {template.musicUrl && (
              <span className="text-sm text-muted-foreground">Music selected</span>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Fade Effects</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <input
              id="fade-in"
              type="checkbox"
              checked={template.fadeIn}
              onChange={(e) => updateTemplate({ fadeIn: e.target.checked })}
              className="h-4 w-4"
            />
            <Label htmlFor="fade-in">Fade In</Label>
          </div>
          <div className="flex items-center gap-2">
            <input
              id="fade-out"
              type="checkbox"
              checked={template.fadeOut}
              onChange={(e) => updateTemplate({ fadeOut: e.target.checked })}
              className="h-4 w-4"
            />
            <Label htmlFor="fade-out">Fade Out</Label>
          </div>
        </CardContent>
      </Card>

      <Button className="w-full" onClick={onSave}>
        <Save className="mr-2 h-4 w-4" />
        Save as Template
      </Button>
    </div>
  );
}