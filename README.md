# Reality Simulator

Reality Simulator is a local multi-agent world prototype with a Python/FastAPI backend and a React dashboard. The current codebase is not a finished "5 million feature" engine; it is the beginnings of a generative simulation platform designed to grow through interacting dimensions instead of flat stat lists.

## What It Does Today

- Simulates a population of agents with needs, jobs, money, memory, relationships, illness, marriage, births, and death
- Includes a disease subsystem with named illnesses, contagion, treatment, and recovery
- Runs an economy with wages, spending, inflation, and treasury flow
- Exposes live world, agent, event, job, and ontology data over FastAPI
- Renders the simulation in a React dashboard
- Supports optional Groq-backed reasoning for selected high-complexity decisions

## What Was Added In This Pass

- A formal ontology layer in `backend/ontology`
- The 12 master simulation dimensions as first-class repo concepts
- Derived dimensional state on each agent snapshot
- Aggregate world-dimensional telemetry on `/api/world`
- A new `/api/ontology` endpoint for feature-generation workflows
- A seeded feature registry persisted in `backend/data/feature_registry.json`
- A structured causal ledger exposed over `/api/causal`
- Documentation for the master architecture and feature template in `docs/`

## Repository Layout

```text
backend/
  agents/         Agent model, lifecycle, and execution
  api/            FastAPI application and endpoints
  decisions/      Rule-based and AI-assisted action selection
  economy/        Wages, jobs, inflation, spending
  events/         Event bus and history
  memory/         Memory bank and relationship graph
  ontology/       Master dimensions and feature-generation scaffolding
  simulation/     Tick loop and world state
frontend/
  src/            React dashboard
docs/
  MASTER_ARCHITECTURE.md
  FEATURE_GENERATION_TEMPLATE.md
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py --server
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Start Both

From the repo root:

```bash
python start.py
```

## Key Endpoints

- `/api/world`
- `/api/agents`
- `/api/agents/{agent_id}`
- `/api/events`
- `/api/jobs`
- `/api/economy/history`
- `/api/ontology`
- `/api/features`
- `/api/causal`
- `/api/health`

## Design Direction

The scaling strategy is:

1. Keep the runtime engine compact.
2. Derive richer dimensional state from that runtime.
3. Add new systems as modular feature families.
4. Expose causal links and measurement rules, not just raw values.

## Important Files

- [backend/ontology/dimensions.py](/c:/Users/amegh/OneDrive/Desktop/real/backend/ontology/dimensions.py:1)
- [backend/api/app.py](/c:/Users/amegh/OneDrive/Desktop/real/backend/api/app.py:1)
- [backend/agents/agent.py](/c:/Users/amegh/OneDrive/Desktop/real/backend/agents/agent.py:1)
- [docs/MASTER_ARCHITECTURE.md](/c:/Users/amegh/OneDrive/Desktop/real/docs/MASTER_ARCHITECTURE.md:1)

## Next Good Expansions

- Persistent feature registry
- Disease progression systems
- Debt and production chains
- Richer communication acts
- Explicit causal graph storage
- Observer-limited information flow
