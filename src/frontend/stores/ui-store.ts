import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

/**
 * UI state store (Zustand).
 *
 * Holds purely client-side UI state: theme, sidebar open/close, current
 * project being edited, selected segment, etc. Persisted to localStorage
 * for user preferences (theme, sidebar).
 */
export type Theme = 'light' | 'dark' | 'system';

interface UIState {
  // Theme
  theme: Theme;
  setTheme: (theme: Theme) => void;

  // Sidebar
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;

  // Active project context
  activeProjectId: string | null;
  setActiveProjectId: (id: string | null) => void;

  // Selected segment (used in transcript / subtitle editor)
  selectedSegmentIndex: number | null;
  setSelectedSegmentIndex: (index: number | null) => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      theme: 'system',
      setTheme: (theme) => set({ theme }),

      sidebarOpen: true,
      toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
      setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),

      activeProjectId: null,
      setActiveProjectId: (activeProjectId) => set({ activeProjectId }),

      selectedSegmentIndex: null,
      setSelectedSegmentIndex: (selectedSegmentIndex) =>
        set({ selectedSegmentIndex }),
    }),
    {
      name: 'videostudio-ui',
      storage: createJSONStorage(() =>
        typeof window !== 'undefined'
          ? window.localStorage
          : (undefined as never)
      ),
      // Only persist user preferences, not transient selection
      partialize: (state) => ({
        theme: state.theme,
        sidebarOpen: state.sidebarOpen,
      }),
    }
  )
);
