'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

export interface PipelineStep {
  id: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
}

export interface PipelineStepperProps {
  steps: PipelineStep[];
  currentStep: string;
  onStepChange?: (stepId: string) => void;
  className?: string;
}

/**
 * Pipeline stepper component for navigating through project steps.
 * Displays steps horizontally with connecting lines and clickable tabs.
 */
export function PipelineStepper({
  steps,
  currentStep,
  onStepChange,
  className,
}: PipelineStepperProps) {
  return (
    <nav
      className={cn('flex items-center justify-center px-4 py-6', className)}
      aria-label="Project pipeline steps"
    >
      <ol className="flex w-full max-w-4xl items-center justify-between">
        {steps.map((step, index) => {
          const isActive = step.id === currentStep;
          const isCompleted = steps.findIndex((s) => s.id === currentStep) > index;
          const isFirst = index === 0;
          const isLast = index === steps.length - 1;

          return (
            <React.Fragment key={step.id}>
              {/* Step item */}
              <li className="flex flex-1 items-center justify-center">
                <button
                  type="button"
                  onClick={() => !step.disabled && onStepChange?.(step.id)}
                  disabled={step.disabled}
                  className={cn(
                    'flex flex-col items-center gap-2',
                    step.disabled && 'cursor-not-allowed opacity-50'
                  )}
                >
                  {/* Step circle */}
                  <div
                    className={cn(
                      'flex h-10 w-10 items-center justify-center rounded-full border-2 transition-colors',
                      isActive && 'border-primary bg-primary text-primary-foreground',
                      isCompleted && !isActive && 'border-primary bg-primary/10 text-primary',
                      !isActive && !isCompleted && 'border-muted bg-background text-muted-foreground'
                    )}
                    aria-current={isActive ? 'step' : undefined}
                  >
                    {step.icon || index + 1}
                  </div>

                  {/* Step label */}
                  <span
                    className={cn(
                      'text-sm font-medium',
                      isActive && 'text-primary',
                      isCompleted && 'text-primary',
                      !isActive && !isCompleted && 'text-muted-foreground'
                    )}
                  >
                    {step.label}
                  </span>
                </button>
              </li>

              {/* Connector line */}
              {!isLast && (
                <li
                  className={cn(
                    'flex-1 border-t-2 transition-colors',
                    isCompleted ? 'border-primary' : 'border-muted'
                  )}
                  aria-hidden="true"
                />
              )}
            </React.Fragment>
          );
        })}
      </ol>
    </nav>
  );
}