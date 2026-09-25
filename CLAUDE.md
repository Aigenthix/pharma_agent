# PharmaAssist AI — Project Handbook

## What this project is

**PharmaAssist AI** is a demo pharma product-intelligence assistant for small pharmacy retailers and distributors. It lets users ask questions about medicines from a local product catalog via an AI chat interface, search for products, view inventory dashboards, identify low-stock items, and get AI-generated product summaries. This is a catalog/business tool for pharma retail, not a clinical or diagnostic tool.

## Current status

Pre-implementation. Only `plan.md` exists — a detailed MVP specification. No backend, frontend, data, Docker, tests, or CI/CD infrastructure have been written yet. This directory is not currently a git repository. The authoritative design is in `plan.md` (sections 1–16); don't restate it here.

## Who is using it / what they think it does

Not yet deployed. This is a prototype in planning stage.

## What is broken or unfinished

Everything. The entire application, tests, and CI/CD pipeline are yet to be built. See `plan.md` for the implementation roadmap.

## What not to touch without asking

**Do not expand V1 scope.** The plan explicitly marks these as "Not in V1":
- Authentication
- PostgreSQL / relational database
- Vector databases or semantic search
- LangChain / LangGraph
- Redis

The goal is to keep this a small, simple demo: FastAPI + Gemini + flat JSON data file, locally runnable with `docker compose up --build`, deployable to AWS App Runner. Growing scope beyond the MVP risks converting it into an AI infrastructure project. If you want to add anything in the above categories, ask first.

**Never commit `.env`** (with `GEMINI_API_KEY`). Commit `.env.example` as the template instead, and ensure `.env` is in `.gitignore`.

## How to run and test

Not runnable yet. Once the backend, frontend, and data files are scaffolded per `plan.md` §7:

**Local dev:**
```bash
docker compose up --build
```
Then open http://localhost:8000.

**Tests:**
```bash
pytest
```

**CI/CD:** See `plan.md` §11–12 for the intended GitHub Actions workflow and AWS deployment flow.
