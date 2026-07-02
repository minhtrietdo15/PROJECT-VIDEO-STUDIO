'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useUIStore } from '@/stores/ui-store';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  FolderKanban,
  Languages,
  Mic,
  Type,
  Video,
  Settings,
  Sparkles,
  Youtube,
} from 'lucide-react';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/projects', label: 'Projects', icon: FolderKanban },
  { href: '/transcripts', label: 'Transcripts', icon: Mic },
  { href: '/translations', label: 'Translations', icon: Languages },
  { href: '/dubbing', label: 'Voice Dubbing', icon: Type },
  { href: '/subtitles', label: 'Subtitles', icon: Sparkles },
  { href: '/render', label: 'Render & Export', icon: Video },
  { href: '/publish', label: 'YouTube', icon: Youtube },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const sidebarOpen = useUIStore((s) => s.sidebarOpen);

  return (
    <aside
      className={cn(
        'hidden h-screen shrink-0 border-r bg-card transition-all duration-200 md:flex md:flex-col',
        sidebarOpen ? 'w-60' : 'w-16'
      )}
    >
      <div className="flex h-14 items-center border-b px-4">
        {sidebarOpen ? (
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <Video className="h-5 w-5 text-primary" />
            <span>VideoStudio</span>
          </Link>
        ) : (
          <Link href="/" className="mx-auto">
            <Video className="h-5 w-5 text-primary" />
          </Link>
        )}
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto p-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive =
            pathname === item.href || pathname?.startsWith(`${item.href}/`);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition',
                isActive
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground',
                !sidebarOpen && 'justify-center'
              )}
              title={!sidebarOpen ? item.label : undefined}
            >
              <Icon className="h-4 w-4 shrink-0" />
              {sidebarOpen && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="border-t p-4 text-xs text-muted-foreground">
        {sidebarOpen && <div>v1.0.0 — Video Localization AI Studio</div>}
      </div>
    </aside>
  );
}
