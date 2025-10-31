# 2025-10-23 - Health mode with evolvable interactions + differential task rewards

Replicating 2025-10-17 evolvable interaction experiment but with differential task rewards.


## Planning

Parameters to vary:

- SYM_INT: -2 (random starting)
- HEALTH_TYPE: interaction-value
- VERTICAL_TRANSMISSION: 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
- MUTUALIST_CYCLE_DONATE_MULTIPLIER/PARASITE_CYCLE_STEAL_MULTIPLIER:
  - 1, 2, 4, 8

Use `environment-diff-rewards.json`.
Switch CYCLES_PER_UPDATE, min cycles before reproduction, and reproduction resource
requirements to what they were for 2025-10-08-health-diff-rewards experiment.