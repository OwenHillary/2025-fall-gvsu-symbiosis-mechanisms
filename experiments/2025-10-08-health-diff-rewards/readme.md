# 2025-10-08 - Health differential rewards

Purpose: Try health mutualist vs. health parasite vs no-sym with differential rewards.

## Planning

- Using 1, 2, 4, 8, 16 reward distribution
  - Hosts/parasites share task rewards
- Controlling rate of reproduction
  - HOST_REPRO_RES: 256
  - SYM_HORIZ_TRANS_RES: 128
  - HOST_MIN_CYCLES_BEFORE_REPRO: 64
  - SYM_MIN_CYCLES_BEFORE_REPRO: 64
  - CYCLES_PER_UPDATE: 16
- Health parameters
  - PARASITE_CYCLE_LOSS_PROP: 0.75
  - MUTUALIST_CYCLE_GAIN_PROP: 0.75
  - HEALTH_INTERACTION_CHANCE: 1.0
  - PARASITE_CYCLE_STEAL_MULTIPLIER: 1, 2, 4, 8, 16
  - MUTUALIST_CYCLE_DONATE_MULTIPLIER: 1, 2, 4, 8, 16
  - PARASITE_BASE_CYCLE_PROP: 0.5
  - HEALTH_MODE: parasite, mutualist

Thoughts:
- Health mode w/mutualists ends up with hosts executing potentially _many_ instructions/update. (>> potential for generational turnover)
- Health mode w/parasites: parasites potentially execute _many_ instructions/update. (>> potential for generational turnover)
