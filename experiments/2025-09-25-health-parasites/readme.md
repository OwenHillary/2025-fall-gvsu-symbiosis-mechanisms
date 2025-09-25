# 2025-09-25 Health Experiment

## Planning

Just parasites to start? Also mutualists?

Start by focusing on parasites. Then, move on to mutualists in subsequent exploratory experiment.

Parameters to consider:

- PARASITE_CYCLE_LOSS_PROP: 0.75
  - Increasing strengthens selection on hosts that mismatch (escape parasites), but also slows generational turnover when parasites have caught hosts.
- HEALTH_INTERACTION_CHANCE: 0.5, 1.0
- PARASITE_CYCLE_STEAL_MULTIPLIER: 1, 2, 4, 8
  - Increasing strengthens selection pressure for matching on parasites.
- PARASITE_BASE_CYCLE_PROP: 0.25, 0.5, 0.75
  - Increasing gives non-matching parasites more runway to chase hosts. Decreasing benefits parasites that match.