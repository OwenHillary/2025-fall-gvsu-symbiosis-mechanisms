# 2025-09-17 Experiment

## Planning

Focus on settings from 2025-09-15-stress-parasite experiment that had the highest average number of different tasks evolve in hosts: SF=30_PDC=0.5_PO=8

- Stress frequency 30, parasite death chance 0.5, parasite stress offspring 8

Goal: see if we can get some higher complexity tasks evolving. E.g., more consistently see the evolution of NOR, XOR, EQU?

It looked like a potential issue with previous experiments was that parasites have trouble evolving tasks beyond AND_NOT/OR

Need to maintain strong selection pressure for parasites to chase hosts and for hosts to escape parasites. Simultaneously need to minimize penalty to evolving higher-complexity tasks that take more cpu cycles to express without increasing the reward for high complexity tasks (beyond as an escape path for hosts).
To minimize penalty to expressing high-complexity tasks, try increasing minimum lifespan + lowering resources required for hosts to reproduce (so that they don't need to do as many repeated high-complexity tasks).

Parameters:
- Bigger population: GRID_X=100, GRID_Y=100
- Keep mutation rate the same: SGP_MUT_PER_BIT_RATE=0.005
- More opportunities for sym offspring to infect a host: FIND_NEIGHBOR_HOST_ATTEMPTS: 20
- Allow syms to be generalist:
  - SYM_ONLY_FIRST_TASK_CREDIT: 0
- Increase lifespans: SYM_MIN_CYCLES_BEFORE_REPRO / HOST_MIN_CYCLES_BEFORE_REPRO:
  - 100/50, 150/75, 200/100
- Lower resources required for hosts to reproduce: HOST_REPRO_RES=10
- Stress
  - STRESS_FREQUENCY: 30
  - PARASITE_DEATH_CHANCE: 0.5
  - PARASITE_NUM_OFFSPRING_ON_STRESS_INTERACTION: 8

Parameters to consider:

- population size: GRID_X=100 GRID_Y=100
- SGP_MUT_PER_BIT_RATE: 0.0025, 0.005, 0.01
- SYM_ONLY_FIRST_TASK_CREDIT: 0, 1
- SYM_MIN_CYCLES_BEFORE_REPRO: 10, 25, 50
- HOST_MIN_CYCLES_BEFORE_REPRO: 50, 100, 150