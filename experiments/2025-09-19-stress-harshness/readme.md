# 2025-09-19 Stress experiment

Purpose: try switching to task-profile-strictly-stronger-match.

## Planning

Parameters to consider:
- GRID_X,GRID_Y=100/100, 80/80
- HORIZONTAL_TRANSMISSION_COMPATIBILITY_MODE = task-profile-strictly-stronger-match
- Minimum lifespan: 200/100
  - Minimum lifespan in updates: 50 / 25
- Stress frequency / death chance:
  - *25/0.25
  - *25/0.50
  - *50/0.25
  - *50/0.5
  - *50/0.75
  - *75/0.25
  - *75/0.5
  - *75/0.75
  - *100/0.25
  - *100/0.5
  - *100/0.75
- PARASITE_NUM_OFFSPRING_ON_STRESS_INTERACTION: 4 (to save time -- strict matching is slower because more oust failures)
- Parasite / mutualist


strict matching
stress frequency/death chance: 30/0.30, 20/0.2
syms only first task: 0/1
TODO: make stress ousting behave same way that non-stress ousting behaves

