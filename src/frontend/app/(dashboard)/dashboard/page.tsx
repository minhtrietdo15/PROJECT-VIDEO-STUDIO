import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ProjectGridSkeleton } from '@/components/ui/loading-skeleton';
import { Plus, FolderOpen } from 'lucide-react';

/**
 * Dashboard home page (placeholder).
 * Real project list / create-project dialog will be implemented in
 * Phase 2.1 (Dashboard) once the backend Project CRUD API is available.
 */
export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <header className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Quản lý project video bản địa hóa của bạn
          </p>
        </div>
        <Button asChild>
          <Link href="/projects/new">
            <Plus className="h-4 w-4" />
            Tạo project mới
          </Link>
        </Button>
      </header>

      <div className="rounded-lg border border-dashed p-12 text-center">
        <FolderOpen className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
        <h2 className="mb-2 text-lg font-semibold">Chưa có project nào</h2>
        <p className="mb-4 text-sm text-muted-foreground">
          Bắt đầu bằng cách tạo project đầu tiên và upload video của bạn.
        </p>
        <Button asChild>
          <Link href="/projects/new">
            <Plus className="h-4 w-4" />
            Tạo project mới
          </Link>
        </Button>
      </div>

      {/* Visual placeholder for the future project list (loading state). */}
      <section>
        <h2 className="mb-4 text-xl font-semibold">Recent projects</h2>
        <ProjectGridSkeleton count={6} />
      </section>
    </div>
  );
}
