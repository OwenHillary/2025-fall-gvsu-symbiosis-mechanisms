#!/usr/bin/env bash

REPLICATES=20
EXP_SLUG=2025-10-17-health-evolvable-interaction
SEED_OFFSET=80000
JOB_TIME=24:00:00
JOB_MEM=8G
PROJECT_NAME=2025-fall-gvsu-symbiosis-mechanisms
RUNS_PER_SUBDIR=950
USERNAME=lalejini
ACCOUNT=devolab
# HPC_ENV_FILE=clipper-hpc-env.sh
HPC_ENV_FILE=msu-hpc-env.sh

REPO_DIR=/Users/lalejina/devo_ws/${PROJECT_NAME}
HOME_EXP_DIR=${REPO_DIR}/experiments/${EXP_SLUG}

DATA_DIR=${HOME_EXP_DIR}/hpc/test/data
JOB_DIR=${HOME_EXP_DIR}/hpc/test/jobs
CONFIG_DIR=${HOME_EXP_DIR}/hpc/config
HPC_ENV_FILEPATH=${REPO_DIR}/hpc-env/${HPC_ENV_FILE}

# (1) Activate appropriate Python virtual environment
source ${REPO_DIR}/pyenv/bin/activate

# (2) Generate slurm script
#   - This will generate an events file for each run
python3 gen-slurm.py \
  --runs_per_subdir ${RUNS_PER_SUBDIR} \
  --time_request ${JOB_TIME} \
  --mem ${JOB_MEM} \
  --data_dir ${DATA_DIR} \
  --config_dir ${CONFIG_DIR} \
  --repo_dir ${REPO_DIR} \
  --replicates ${REPLICATES} \
  --job_dir ${JOB_DIR} \
  --seed_offset ${SEED_OFFSET} \
  --hpc_account ${ACCOUNT} \
  --hpc_env_file ${HPC_ENV_FILEPATH}