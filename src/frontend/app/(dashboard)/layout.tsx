import { Shell } from '@/components/layout/shell';

/**
 * Layout for authenticated dashboard routes.
 * Wraps all dashboard pages in the application shell (sidebar + header).
 */
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <Shell>{children}</Shell>;
}
