# DecisionFlow AI

AI-assisted configurable decision automation platform demonstrated through
telecom device-upgrade eligibility and risk decisioning.

## Core principle

AI assists with policy authoring, validation and explanation.

The final business decision is produced by a deterministic rule engine.

## Architecture

React
→ FastAPI
→ Application Services
→ Rule Engine and AI Services
→ MySQL

## Repository branches

- `main` — stable and demo-ready
- `feature/backend-rule-engine`
- `feature/ai-policy-studio`
- `feature/frontend-dashboard`
- `feature/integration`

## Current status

Initial project baseline.

## Backend startup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
Frontend startup
cd frontend
npm install
npm run dev
MySQL startup
docker compose up -d mysql
docker compose ps
Local URLs
Frontend: http://localhost:5173
Backend: http://localhost:8000
Swagger: http://localhost:8000/docs
Health: http://localhost:8000/health
Readiness: http://localhost:8000/ready
Documentation

See the docs/ directory.

Security

Never commit .env, API keys, access tokens or production credentials.
