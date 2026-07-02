import type { ReactNode } from 'react';
import { Sidebar } from './sidebar';
import { Header } from './header';
import { ErrorBoundary } from '@/components/error-boundary';

/**
 * Application shell.
 * Composed of: Sidebar (left) + Header (top) + Main content.
 * Wrapped in ErrorBoundary so an error in the page doesn't take the whole
 * chrome down with it.
 */
export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          <ErrorBoundary>{children}</ErrorBoundary>
        </main>
      </div>
    </div>
  );
}
