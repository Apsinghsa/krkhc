# Agent Guidelines for krkhc

## Project Overview
Full-stack application with Next.js 16 (frontend) and FastAPI (backend).

## Build Commands

### Frontend (Next.js)
```bash
cd frontend
npm run dev      # Start development server
npm run build    # Production build
npm run start    # Start production server
npm run lint     # Run ESLint
```

### Backend (FastAPI)
```bash
cd backend
uv run main.py   # Run development server
uv sync          # Install dependencies
```

## Code Style

### TypeScript (Frontend)
- **Strict mode enabled** - always define types explicitly
- Use `type` for object shapes, `interface` for extensible contracts
- Prefer functional components with explicit return types
- Use path alias `@/*` for imports from project root

```typescript
// Good
import { useState } from "react";
import { Button } from "@/components/Button";

interface UserProps {
  name: string;
  age: number;
}

export function UserCard({ name, age }: UserProps): JSX.Element {
  return <div>{name}</div>;
}
```

### Python (Backend)
- Python 3.14+ required
- Use type hints on all function signatures
- Prefer Pydantic models for request/response validation
- Use `uv` for package management (not pip)

```python
from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.get("/users/{user_id}")
def get_user(user_id: int) -> User:
    return User(name="John", age=30)
```

### Naming Conventions
- **Files**: kebab-case (`user-profile.tsx`, `data_utils.py`)
- **Components**: PascalCase (`UserProfile`)
- **Functions/Variables**: camelCase (TS), snake_case (Python)
- **Constants**: UPPER_SNAKE_CASE
- **Types/Interfaces**: PascalCase with descriptive names

## Import Order

### TypeScript
1. React/Next.js imports
2. Third-party libraries
3. Absolute imports (`@/*`)
4. Relative imports
5. Type-only imports last

### Python
1. Standard library
2. Third-party (FastAPI, Pydantic)
3. Local modules

## Error Handling

### TypeScript
- Use try/catch for async operations
- Prefer early returns over nested conditionals
- Never use `any` - use `unknown` with type guards

### Python
- Use FastAPI's HTTPException for API errors
- Validate with Pydantic before business logic
- Log errors with context, never swallow exceptions

## Styling (Tailwind v4)
- Use CSS variables for theming (defined in `globals.css`)
- Prefer semantic class names over arbitrary values
- Support dark mode with `dark:` prefix
- Mobile-first responsive design

## Testing
No test framework configured. To add tests:
- Frontend: Install Jest or Vitest
- Backend: Use pytest with `uv add --dev pytest`

## Git
- Never commit `.env`, `node_modules/`, `__pycache__/`, `.venv/`
- Never commit secrets or API keys

## Pre-commit Checklist
1. Run `npm run lint` in frontend
2. Verify TypeScript compiles (`npx tsc --noEmit`)
3. Test backend starts without errors
