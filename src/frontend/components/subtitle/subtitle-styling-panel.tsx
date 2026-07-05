'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export interface SubtitleStyle {
  fontFamily: string;
  fontSize: number;
  color: string;
  backgroundColor: string;
  borderColor: string;
  borderWidth: number;
  shadow: boolean;
  position: 'top' | 'bottom' | 'custom';
  offsetY: number;
  animation: 'fade' | 'slide' | 'typewriter' | 'none';
}

export interface SubtitleStylingPanelProps {
  style: SubtitleStyle;
  onStyleChange?: (style: SubtitleStyle) => void;
  onPreview?: () => void;
  className?: string;
}

const FONT_OPTIONS = [
  'Arial',
  'Helvetica',
  'Times New Roman',
  'Courier New',
  'Verdana',
  'Tahoma',
  'Georgia',
  'Palatino',
];

const COLOR_PRESETS = [
  '#FFFFFF', // White
  '#FFFF00', // Yellow
  '#FF0000', // Red
  '#00FF00', // Green
  '#0000FF', // Blue
  '#FF00FF', // Magenta
  '#00FFFF', // Cyan
  '#000000', // Black
];

const ANIMATION_OPTIONS: Array<'fade' | 'slide' | 'typewriter' | 'none'> = [
  'fade',
  'slide',
  'typewriter',
  'none',
];

export function SubtitleStylingPanel({
  style,
  onStyleChange,
  onPreview,
  className,
}: SubtitleStylingPanelProps) {
  const updateStyle = (updates: Partial<SubtitleStyle>) => {
    onStyleChange?.({ ...style, ...updates });
  };

  return (
    <div className={cn('space-y-4', className)}>
      {/* Font picker */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Font</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid gap-2">
            <Label htmlFor="font-family">Font Family</Label>
            <select
              id="font-family"
              value={style.fontFamily}
              onChange={(e) => updateStyle({ fontFamily: e.target.value })}
              className="rounded-md border px-3 py-2"
            >
              {FONT_OPTIONS.map((font) => (
                <option key={font} value={font}>
                  {font}
                </option>
              ))}
            </select>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="font-size">Font Size: {style.fontSize}px</Label>
            <input
              id="font-size"
              type="range"
              min="10"
              max="72"
              value={style.fontSize}
              onChange={(e) => updateStyle({ fontSize: parseInt(e.target.value) })}
              className="w-full"
            />
          </div>
        </CardContent>
      </Card>

      {/* Color picker */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Colors</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <Label>Text Color</Label>
            <div className="mt-2 flex flex-wrap gap-2">
              {COLOR_PRESETS.map((color) => (
                <button
                  key={color}
                  type="button"
                  className={cn(
                    'h-8 w-8 rounded border-2',
                    style.color === color && 'ring-2 ring-primary'
                  )}
                  style={{ backgroundColor: color }}
                  onClick={() => updateStyle({ color })}
                  aria-label={`Select color ${color}`}
                />
              ))}
            </div>
          </div>

          <div>
            <Label>Background Color</Label>
            <div className="mt-2 flex flex-wrap gap-2">
              {COLOR_PRESETS.map((color) => (
                <button
                  key={color}
                  type="button"
                  className={cn(
                    'h-8 w-8 rounded border-2',
                    style.backgroundColor === color && 'ring-2 ring-primary'
                  )}
                  style={{ backgroundColor: color }}
                  onClick={() => updateStyle({ backgroundColor: color })}
                  aria-label={`Select background ${color}`}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Border/Shadow controls */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Border & Shadow</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center gap-2">
            <input
              id="shadow"
              type="checkbox"
              checked={style.shadow}
              onChange={(e) => updateStyle({ shadow: e.target.checked })}
              className="h-4 w-4"
            />
            <Label htmlFor="shadow">Enable Shadow</Label>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="border-width">Border Width: {style.borderWidth}px</Label>
            <input
              id="border-width"
              type="range"
              min="0"
              max="5"
              value={style.borderWidth}
              onChange={(e) => updateStyle({ borderWidth: parseInt(e.target.value) })}
              className="w-full"
            />
          </div>

          <div>
            <Label>Border Color</Label>
            <div className="mt-2 flex flex-wrap gap-2">
              {COLOR_PRESETS.map((color) => (
                <button
                  key={color}
                  type="button"
                  className={cn(
                    'h-8 w-8 rounded border-2',
                    style.borderColor === color && 'ring-2 ring-primary'
                  )}
                  style={{ backgroundColor: color }}
                  onClick={() => updateStyle({ borderColor: color })}
                  aria-label={`Select border ${color}`}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Position presets */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Position</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2">
            {(['top', 'bottom', 'custom'] as const).map((pos) => (
              <Button
                key={pos}
                variant={style.position === pos ? 'default' : 'outline'}
                size="sm"
                onClick={() => updateStyle({ position: pos })}
              >
                {pos.charAt(0).toUpperCase() + pos.slice(1)}
              </Button>
            ))}
          </div>

          {style.position === 'custom' && (
            <div className="grid gap-2">
              <Label htmlFor="offset-y">Vertical Offset (px)</Label>
              <input
                id="offset-y"
                type="range"
                min="-200"
                max="200"
                value={style.offsetY}
                onChange={(e) => updateStyle({ offsetY: parseInt(e.target.value) })}
                className="w-full"
              />
            </div>
          )}
        </CardContent>
      </Card>

      {/* Animation selector */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Animation</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex flex-wrap gap-2">
            {ANIMATION_OPTIONS.map((anim) => (
              <Button
                key={anim}
                variant={style.animation === anim ? 'default' : 'outline'}
                size="sm"
                onClick={() => updateStyle({ animation: anim })}
              >
                {anim.charAt(0).toUpperCase() + anim.slice(1)}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Preview button */}
      <Button className="w-full" onClick={onPreview}>
        Preview
      </Button>
    </div>
  );
}