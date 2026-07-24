# DecisionFlow AI — Frontend

React admin dashboard for the DecisionFlow AI hackathon POC (telecom eligibility decisioning).

## Quick start

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

## Mock mode (default)

The app runs with `VITE_USE_MOCK_API=true` — no backend required.

## Real API mode

Set in `.env`:

```text
VITE_USE_MOCK_API=false
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_BACKEND_BASE_URL=http://localhost:8000
```

## Pages

- **Dashboard** — stats, charts, recent activity
- **AI Policy Studio** — natural-language policy generation
- **Policies** — list and detail
- **Decision Center** — customer evaluation with presets
- **Analytics** — distribution and trends
- **Audit Logs** — governance trail
- **Settings** — environment info

## Demo flow

1. Dashboard → overview
2. AI Policy Studio → generate premium upgrade policy
3. Save draft → activate
4. Decision Center → eligible customer → APPROVE
5. Decision Center → high fraud preset → REJECT
6. Audit → view records
