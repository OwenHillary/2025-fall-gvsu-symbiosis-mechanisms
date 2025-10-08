# 2025-10-02 - No symbiont + Different task values

Goal:
- Can we see EQU evolution in absence of symbionts with differential task rewards?

Ideas:
- Preferential replacement? (more resources means more defense against replacement for hosts)

## Next steps

- Run with mutualists / parasites
- Think about

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

- CPU=16,MC=64,HRR=256
  - NOT (rew=1): Need to do 256 NOT => 768 cycles => 48 updates
  - NOR (rew=8): Need to do 32 NOR => 224 cycles => 14 udpates
  - EQU (rew=16): Need to do 16 EQU => ~160 cycles (@10 insts) => 10 updates