# Frontend — Video Localization AI Studio

Next.js 14 frontend (App Router) for the Video Localization AI Studio.

## Stack

- **Next.js 14** (App Router, Server Components, Server Actions)
- **TypeScript** (strict mode)
- **TailwindCSS** + **shadcn/ui** (Radix primitives)
- **TanStack Query** (server state)
- **Zustand** (client UI state, persisted to localStorage)
- **Axios** with response envelope unwrapping
- **Zod** for runtime schema validation
- **lucide-react** for icons

## Project Structure

```
src/frontend/
├── app/                              # Next.js App Router
│   ├── (dashboard)/                  # Authenticated routes (wrapped in Shell)
│   │   ├── layout.tsx                #   Dashboard layout (Shell wrapper)
│   │   └── dashboard/
│   │       └── page.tsx              #   Dashboard home
│   ├── layout.tsx                    # Root layout (Providers)
│   ├── page.tsx                      # Landing page
│   └── globals.css                   # Tailwind + CSS variables
│
├── components/
│   ├── layout/                       # Sidebar, Header, Shell
│   ├── ui/                           # Reusable primitives (Button, Skeleton, ...)
│   └── error-boundary.tsx            # React error boundary
│
├── lib/
│   ├── api-client.ts                 # Pre-configured Axios + envelope unwrap
│   ├── providers.tsx                 # TanStack Query + future providers
│   └── utils.ts                      # cn(), formatDuration(), formatBytes()
│
├── stores/
│   └── ui-store.ts                   # Zustand: theme, sidebar, selection
│
├── components.json                   # shadcn/ui config
├── tailwind.config.ts
├── postcss.config.js
├── tsconfig.json
├── next.config.js
└── package.json
```

## Scripts

```bash
npm install            # Install dependencies
npm run dev            # Dev server (http://localhost:3000)
npm run build          # Production build
npm run start          # Run production build
npm run lint           # ESLint
npm run type-check     # TypeScript noEmit check
npm run format         # Prettier write
npm run format:check   # Prettier verify
```

## Environment

Copy `.env.example` to `.env.local` and adjust as needed.

| Variable              | Default                 | Description         |
| --------------------- | ----------------------- | ------------------- |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend FastAPI URL |

## Backend Wiring

- `next.config.js` proxies `/api/*` requests to the backend.
- `lib/api-client.ts` uses `NEXT_PUBLIC_API_URL` and unwraps the standard
  `{ success, data, error, meta }` envelope returned by the FastAPI backend.
- Auth tokens (when added) are read from `localStorage["auth_token"]`.

## shadcn/ui

`components.json` is pre-configured. To add a new primitive, run:

```bash
npx shadcn-ui@latest add <component>
```

(Use the official CLI; the resulting component files will be added to
`components/ui/`.)

## Notes

- This is Phase 0.4 (Frontend Foundation). Only the shell, routing,
  state, theming, and base primitives are present. The actual product
  pages (project workspace, transcript editor, subtitle editor, etc.)
  are scheduled for Phase 1+ and will be added in subsequent PRs.
