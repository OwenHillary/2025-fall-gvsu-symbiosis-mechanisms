# 2025-09-15 Experiment

Purpose: Explore effect of num offspring on stress interaction.

## Lessons

Extinctions:

- When no symbionts, hosts all die when:
  - BASE_DEATH_CHANCE: 0.5, STRESS FREQ: 30,
  - BASE_DEATH_CHANCE: 0.75, STRESS FREQ: 30, 50, 100
  - In ~50% of replicates,
    - death chance is 0.5 and frequency is 50 updates
    - death chance is 0.75 and frequency is 100 updates
- _Most_ replicates with symbionts have hosts and syms still around at end of run.

Top num diff tasks evolved:
- SF=30_PDC=0.5_PO=8
- SF=50_PDC=0.75_PO=8
- SF=30_PDC=0.5_PO=4

## Next steps:

- Looks like parasites aren't able to keep pushing hosts to doing XORs / EQUs.
  - Increase population size.
  - Run for longer?
  - Decrease mutation rate?
  - Force syms to run for more cycles before reproducing.

## Planning

Parameters:
- Stress type: parasite
- STRESS_FREQUENCY: 30, 50, 100
- PARASITE_DEATH_CHANCE: 0.5, 0.75
- PARASITE_NUM_OFFSPRING_ON_STRESS_INTERACTION: 1, 4, 8


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
