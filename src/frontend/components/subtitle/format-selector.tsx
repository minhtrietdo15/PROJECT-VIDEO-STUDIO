'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { SubtitleSegment } from './timeline';

export type SubtitleFormat = 'srt' | 'ass' | 'vtt';

export interface FormatSelectorProps {
  segments: SubtitleSegment[];
  format: SubtitleFormat;
  onFormatChange?: (format: SubtitleFormat) => void;
  onExport?: () => void;
  className?: string;
}

/**
 * Format selector for subtitle preview and export.
 */
export function FormatSelector({
  segments,
  format,
  onFormatChange,
  onExport,
  className,
}: FormatSelectorProps) {
  const formatTimeSrt = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    const hundredths = Math.floor((seconds % 1) * 100);
    return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}.${hundredths.toString().padStart(2, '0')}`;
  };

  const formatTimeVtt = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}:${mins.toString().padStart(2, '0')}:${secs.toFixed(3)}`;
  };

  const generateSrt = () => {
    return segments
      .map((seg, index) => {
        return `${index + 1}\n${formatTimeSrt(seg.start)} --> ${formatTimeSrt(seg.end)}\n${seg.text}\n`;
      })
      .join('\n');
  };

  const generateVtt = () => {
    const header = 'WEBVTT\n\n';
    const body = segments
      .map((seg) => {
        return `${formatTimeVtt(seg.start)} --> ${formatTimeVtt(seg.end)}\n${seg.text}\n`;
      })
      .join('\n');
    return header + body;
  };

  const generateAss = () => {
    const header = `[Script Info]
Title: Subtitle
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, AlphaLevel, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;
    const body = segments
      .map((seg) => {
        return `Dialogue: 0,${formatTimeSrt(seg.start)},${formatTimeSrt(seg.end)},Default,,0,0,0,,${seg.text.replace(/\n/g, '\\N')}`;
      })
      .join('\n');
    return header + body;
  };

  const getPreview = () => {
    switch (format) {
      case 'srt':
        return generateSrt();
      case 'vtt':
        return generateVtt();
      case 'ass':
        return generateAss();
      default:
        return generateSrt();
    }
  };

  return (
    <div className={cn('space-y-4', className)}>
      <div className="flex gap-2">
        {(['srt', 'ass', 'vtt'] as SubtitleFormat[]).map((fmt) => (
          <Button
            key={fmt}
            variant={format === fmt ? 'default' : 'outline'}
            size="sm"
            onClick={() => onFormatChange?.(fmt)}
          >
            {fmt.toUpperCase()}
          </Button>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Preview</CardTitle>
        </CardHeader>
        <CardContent>
          <Textarea
            readOnly
            value={getPreview()}
            className="h-64 resize-none font-mono text-xs"
          />
        </CardContent>
      </Card>

      <Button className="w-full" onClick={onExport}>
        Export
      </Button>
    </div>
  );
}