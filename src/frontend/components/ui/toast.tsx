'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { X, AlertCircle, AlertTriangle, Info, CheckCircle } from 'lucide-react';

export type ToastVariant = 'default' | 'destructive' | 'success' | 'warning' | 'info';

export interface Toast {
  id: string;
  title?: string;
  description?: string;
  variant?: ToastVariant;
  action?: {
    label: string;
    onClick: () => void;
  };
}

interface ToastProps extends Toast {
  onClose: () => void;
}

const variantStyles: Record<ToastVariant, string> = {
  default: 'bg-background border-border',
  destructive: 'bg-destructive text-destructive-foreground',
  success: 'bg-green-500 text-white',
  warning: 'bg-yellow-500 text-white',
  info: 'bg-blue-500 text-white',
};

const variantIcons: Record<ToastVariant, React.ReactNode> = {
  default: <Info className="h-4 w-4" />,
  destructive: <AlertCircle className="h-4 w-4" />,
  success: <CheckCircle className="h-4 w-4" />,
  warning: <AlertTriangle className="h-4 w-4" />,
  info: <Info className="h-4 w-4" />,
};

export function ToastComponent({ id, title, description, variant = 'default', action, onClose }: ToastProps) {
  return (
    <div
      className={cn(
        'pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-lg border p-4 shadow-lg',
        variantStyles[variant]
      )}
    >
      <div className="flex-shrink-0">{variantIcons[variant]}</div>
      <div className="flex-1">
        {title && <div className="font-semibold">{title}</div>}
        {description && <div className="mt-1 text-sm">{description}</div>}
        {action && (
          <button
            type="button"
            onClick={action.onClick}
            className="mt-2 text-sm underline underline-offset-2"
          >
            {action.label}
          </button>
        )}
      </div>
      <button
        type="button"
        onClick={onClose}
        className="flex-shrink-0 rounded p-1 hover:bg-black/10"
      >
        <X className="h-3 w-3" />
        <span className="sr-only">Close</span>
      </button>
    </div>
  );
}

// Toast context and provider
interface ToastContextValue {
  toasts: Toast[];
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
}

const ToastContext = React.createContext<ToastContextValue | null>(null);

export function useToast() {
  const context = React.useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<Toast[]>([]);

  const addToast = React.useCallback((toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).slice(2);
    setToasts((prev) => [...prev, { ...toast, id }]);
  }, []);

  const removeToast = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
      {children}
      <div className="pointer-events-none fixed top-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map((toast) => (
          <ToastComponent
            key={toast.id}
            {...toast}
            onClose={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </ToastContext.Provider>
  );
}