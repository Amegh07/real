# Reality Simulator Master Architecture

This repository is not a hand-authored "5,000,000 feature" simulator. The practical target is a generative simulation stack that can express millions of meaningful configurations through a smaller number of orthogonal systems.

## Core Rule

A feature is only worth adding if it has:

- A mechanism
- A measurable state space
- Interactions with other systems
- Failure modes
- A believable implementation path

## The 12 Master Dimensions

The engine now treats the simulation as a dimensional space rather than a flat list of stats.

1. `biophysical`
2. `cognitive`
3. `affective`
4. `social`
5. `economic`
6. `institutional`
7. `environmental`
8. `temporal`
9. `pathology`
10. `material`
11. `communication`
12. `causal`

These live in [backend/ontology/dimensions.py](/c:/Users/amegh/OneDrive/Desktop/real/backend/ontology/dimensions.py:1).

## Current Engine Shape

- `backend/agents/agent.py`: compact agent state plus derived dimensional profile
- `backend/agents/agent_manager.py`: spawning, lifecycle, social interactions, execution routing
- `backend/decisions/decision_engine.py`: rule-first decision scoring with optional AI escalation
- `backend/economy/economy.py`: jobs, wages, spending, inflation, treasury flow
- `backend/simulation/world_state.py`: time, weather, environment, aggregate dimensional snapshot
- `backend/api/app.py`: dashboard endpoints plus ontology exposure
- `frontend/src`: live monitoring UI

## What Was Added In This Pass

- A formal ontology module with:
  - master dimensions
  - feature specification template
  - derived agent dimensional state
  - derived world dimensional state
- A feature registry with seeded specs across the 12 master dimensions
- A structured causal ledger for machine-readable cause tracking
- Agent snapshots now expose richer state under `dimensions`
- World snapshots now expose aggregate dimensional telemetry
- A new `/api/ontology` endpoint publishes the ontology and feature template
- New `/api/features` and `/api/causal` endpoints publish feature specs and causal records
- Decision scoring now uses dimensional pressure instead of only raw hunger/energy/money

## How To Scale From Here

### Stage 1: Feature Registry

Add a persistent registry of generated feature specifications:

- feature id
- taxonomy labels
- mechanism
- upstream and downstream links
- update cadence
- validation references

### Stage 2: System Families

Expand one dimension at a time into modular systems:

- biophysical: sleep debt, infection progression, injury recovery
- cognitive: attention budget, memory salience, planning depth
- affective: stress accumulation, regulation strategies, grief and recovery
- social: trust, reciprocity, kinship, institutional ties
- economic: debt, consumption classes, production chains, price elasticity

### Stage 3: Causal Graph

Every major state change should emit machine-readable causal edges:

- cause id
- source system
- target feature
- delay
- confidence
- reversibility

### Stage 4: Observer Limits

Different observers should see partial and noisy slices of reality:

- local knowledge only
- delayed updates
- costly information gathering
- deception and uncertainty

## Non-Goals

- Hand-writing millions of leaf features
- Perfect medical, psychological, or economic realism in a single iteration
- A single monolithic god object that knows everything about everyone

## Standard For New Features

Before merging a new subsystem, answer:

1. What real mechanism does this represent?
2. How is it measured?
3. What three systems affect it?
4. What three systems does it affect?
5. What happens when it breaks?
6. Can the current scheduler update it cheaply?
