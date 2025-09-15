# 2025-09-05-health-parasite-sweep

Purpose: exploratory parameter sweep for health parasites

## Lessons learned

Paused runs. Too many combinations of parameters to complete in reasonable period of time for exploratory experiments. Changed important model details, motivating new (more focused) runs.

## Planning


Explore these variables:

- Parasites
  - TODO: run HOST_SYM_COMPATIBILITY_MODE = task-stronger-match / strict matching
  - VT = 0
  - cycle loss prop = 0.1, 0.3, 0.5, 0.9
  - interaction chance = 1.0, 0.5
  - start moi = 1
  - HOST_REPRO_RES = 10 (default), 50, 100
  - SYM_HORIZ_TRANS_RES = 0 (default), 10, 50, 100
- No symbionts control
  - Start moi = 0

Fixed:

- ENABLE_HEALTH 1
- HORIZ_TRANS = 1
- VERTICAL_TRANSMISSION = 0
- GRID_X = 60
- GRID_Y = 60
- Updates = 500000
- VT_TASK_MATCH = 0
- TASK_PROFILE_MODE = parent-first
- HOST_SYM_COMPATIBILITY_MODE = task-stronger-match
- SGP_MUT_PER_BIT_RATE = 0.005
- SYM_VERT_TRANS_RES = 0
- GRID = 0
- OUSTING 1
- CYCLES_PER_UPDATE 4
- FIND_NEIGHBOR_HOST_ATTEMPTS 4