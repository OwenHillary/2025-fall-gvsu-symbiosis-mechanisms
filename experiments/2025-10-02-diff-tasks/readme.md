# 2025-10-02 - No symbiont + Different task values

Goal:
- Can we see EQU evolution in absence of symbionts with differential task rewards?

Ideas:
- Preferential replacement? (more resources means more defense against replacement for hosts)

## Planning

- START_MOI=0
  - Just do no symbionts for this first exploration
- HOST_REPRO_RES = 128, 256
- HOST_AGE_MAX = -1
  - Eliminate maximum age for now
- CYCLES_PER_UPDATE = 4, 8, 16, 32
- HOST_MIN_CYCLES_BEFORE_REPRO = 128, 256
- HOST_ONLY_FIRST_TASK_CREDIT = 0, 1

Task reward distribution

- NAND/NOT: 1 (4/3 instructions)
  - RES=128,CYC=4: 128 tasks per repro
- OR_NOT/AND: 2 (5/5 instructions)
  - RES=128,CYC=4: 64 tasks per repro
- OR/AND_NOT: 4 (6/6 instructions)
  - RES=128,CYC=4: 32 tasks per repro
- NOR/XOR: 8 (7/8 instructions)
  - RES=128,CYC=4: 16 tasks per repro
- EQU: 16 (9 instructions)
  - RES=128,CYC:4: 8 tasks per repro
