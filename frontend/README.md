# AI Portfolio — Frontend

Interactive AI portfolio for Noorullah Zamindar (AI Engineer & Data Scientist).
Visitors ask a chat assistant about his projects, skills, experience, and
contact details; the assistant answers from the backend and the UI renders
matching cards (projects carousel, skills, experience timeline, contact).

## Stack

- React 19 + TypeScript + Vite
- Tailwind CSS 4, Framer Motion, lucide-react
- Fluid-cursor canvas effect (`src/components/FluidCursor.tsx`)

## Structure

- `src/App.tsx` — landing view, chat view, project/info modals, offline
  fallback replies used when the backend is unreachable
- `src/components/` — `FluidCursor`, `ExperienceTimeline`
- `src/data/` — `projects.ts`, `skills.ts`, `experience.ts` (content shown
  by the chat cards)
- `src/hooks/` — `useTypewriterPlaceholder`, `use-FluidCursor`

## Run locally

```bash
cd frontend
npm install
npm run dev
```

Other scripts: `npm run build` (type-check + production build),
`npm run lint`, `npm run preview`.

## Configuration

The chat calls the backend at `VITE_API_URL` (defaults to
`http://localhost:8000` when unset):

```env
VITE_API_URL=http://localhost:8000
```

The backend lives in `../backend` (FastAPI + Groq). When it is unreachable
or has no API key, the frontend answers from its built-in offline replies
instead of failing.
