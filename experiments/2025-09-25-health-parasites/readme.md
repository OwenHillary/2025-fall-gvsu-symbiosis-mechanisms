# 2025-09-25 Health Experiment

## Takeaways

- Reasonable parameters for health interaction parasites:
  - Interaction chance = 1.0 (better than 0.5)
  - IC=1_PBC=0.25_SM=8
  - IC=1_PBC=0.5_SM=4
  - IC=1_PBC=0.5_SM=8 ** (top ranked for both)
  - IC=1_PBC=0.75_SM=2
  - IC=1_PBC=0.75_SM=4

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