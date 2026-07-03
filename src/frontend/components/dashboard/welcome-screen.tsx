'use client';

import * as React from 'react';
import { Sparkles, Upload, Languages, Film } from 'lucide-react';
import { Button } from '@/components/ui/button';

export interface WelcomeScreenProps {
  onCreateProject?: () => void;
  className?: string;
}

const STEPS = [
  {
    icon: Upload,
    title: 'Upload Video',
    description: 'Import your video from local files or a URL.',
  },
  {
    icon: Languages,
    title: 'Transcribe & Translate',
    description: 'Generate transcripts and translate them automatically.',
  },
  {
    icon: Film,
    title: 'Dub & Export',
    description: 'Generate voice-overs and export your localized video.',
  },
] as const;

export function WelcomeScreen({ onCreateProject, className }: WelcomeScreenProps) {
  return (
    <div className={className}>
      <div className="mb-8 rounded-lg border bg-gradient-to-br from-primary/5 to-background p-8 text-center">
        <div className="mb-4 inline-flex rounded-full bg-primary/10 p-3">
          <Sparkles className="h-6 w-6 text-primary" />
        </div>
        <h1 className="mb-2 text-2xl font-bold">Welcome to Video Localization AI Studio</h1>
        <p className="mb-6 text-sm text-muted-foreground">
          Localize your videos with AI-powered transcription, translation, voice dubbing, and rendering.
        </p>
        <Button onClick={onCreateProject}>Create Your First Project</Button>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {STEPS.map((step) => (
          <div key={step.title} className="rounded-lg border p-4 text-center">
            <div className="mb-3 inline-flex rounded-full bg-muted p-2">
              <step.icon className="h-5 w-5 text-muted-foreground" />
            </div>
            <h3 className="mb-1 font-medium">{step.title}</h3>
            <p className="text-xs text-muted-foreground">{step.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
