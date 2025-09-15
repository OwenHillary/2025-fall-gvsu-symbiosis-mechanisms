# 2025-09-15 Experiment

Purpose: Explore effect of num offspring on stress interaction.

## Planning

Parameters:
- Stress type: parasite
- STRESS_FREQUENCY: 30, 50, 100
- PARASITE_DEATH_CHANCE: 0.5, 0.75
- PARASITE_NUM_OFFSPRING_ON_STRESS_INTERACTION: 4, 8


Parameters to consider:

- STRESS_TYPE: parasite, mutualist
- STRESS_FREQUENCY: 50, 100, 200, 400
- PARASITE_DEATH_CHANCE: 0.5, 0.75, 0.9
- MUTUALIST_DEATH_CHANCE: 0.0
- BASE_DEATH_CHANCE:
  - Parasites: 0.0
  - Mutualists: 0.5, 0.75, 0.9, 1.0
  - No symbionts: 0.5, 0.75, 0.9
- PARASITE_NUM_OFFSPRING_ON_STRESS_INTERACTION: 1, 2, 4, 8
- SYM_ONLY_FIRST_TASK_CREDIT: "1",

+ No symbiont control

## Thoughts

- At something like 90% death rate, not enough surviving hosts for parasite offspring to land in. Likely extreme symbiont bottleneck every stress event, resulting in loss of diversity.