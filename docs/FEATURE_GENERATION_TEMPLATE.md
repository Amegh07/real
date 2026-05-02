# Feature Generation Template

Use this template whenever you add a new generated feature family to the simulator.

## Required Fields

- `feature_name`
- `domain`
- `scale`
- `timescale`
- `observability`
- `reversibility`
- `emergence_class`
- `mechanism`
- `state_space`
- `measurement`
- `upstream_causes`
- `downstream_effects`
- `interaction_rules`
- `pathological_extremes`
- `real_world_validation`
- `implementation_notes`

## Authoring Rules

- Do not model important systems as bare booleans when a continuum or vector is more honest.
- Do not add magic constants without naming or documenting their origin.
- Do not assume relationships are symmetric.
- Do not allow perfect information unless the observer explicitly earned it.
- Do not add a feature that cannot fail, degrade, or conflict with another system.

## Minimal Example

```yaml
feature_name: stress_load
domain: Affective
scale: Organism
timescale: Hours
observability: Latent/inferential
reversibility: Partially reversible
emergence_class: Synergistic
mechanism: Accumulated physiological and social pressure reduces adaptive capacity.
state_space: Continuous scalar from 0 to 100.
measurement: Derived from deprivation, illness burden, low energy, and social conflict.
upstream_causes:
  - hunger_deficit
  - sleep_debt
  - rivalry_pressure
downstream_effects:
  - decision_clarity
  - distress
  - illness_vulnerability
interaction_rules:
  - stress_load(t+1) = stress_load(t) * decay + incoming_pressure - recovery
pathological_extremes:
  - High values trigger paralysis, desperation, conflict, and health decline.
real_world_validation:
  - Chronic stress predicts impaired cognition and worsened physical health.
implementation_notes:
  - Agent-local derived value, updated every tick.
```
