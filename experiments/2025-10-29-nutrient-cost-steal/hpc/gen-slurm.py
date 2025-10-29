'''
Generate slurm job submission scripts - one per condition
'''

import argparse
import os
import sys
import pathlib
from pyvarco import CombinationCollector

# Add scripts directory to path, import utilities from scripts directory.
sys.path.append(
    os.path.join(
        pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parents[2],
        "scripts"
    )
)
import utilities as utils

# Default configuration values
default_seed_offset = 1000
default_account = None
default_num_replicates = 30
default_job_time_request = "8:00:00"
default_job_mem_request = "8G"

executable = "symbulation_sgp"

base_slurm_script_fpath = "./base_slurm_script.txt"

# Create combos
combos = CombinationCollector()

# Parameters that do not change across treatments for this experiment.
fixed_parameters = {
    "DATA_INT": "100",
    "GRID_X": "80",
    "GRID_Y": "80",
    "POP_SIZE": "-1",
    "UPDATES": "200000",
    "HORIZ_TRANS": "1",
    "GRID": "0",
    "OUSTING": "1",
    "SYM_VERT_TRANS_RES": "0",
    "ENABLE_STRESS": "0",
    "ENABLE_HEALTH": "0",
    "ENABLE_NUTRIENT": "1",
    "TASK_ENV_CFG_PATH": "environment-diff-rewards.json",
    "SYM_ONLY_FIRST_TASK_CREDIT": "0",
    "SGP_MUT_PER_BIT_RATE": "0.005",
    "FIND_NEIGHBOR_HOST_ATTEMPTS": "5",
    "VT_TASK_MATCH": "1",
    "TASK_PROFILE_MODE": "self-all",
    "TASK_PROFILE_COMPATIBILITY_MODE": "task-any-match",
    "HORIZONTAL_TRANSMISSION_COMPATIBILITY_MODE": "task-profile-strictly-stronger-match",
    "CYCLES_PER_UPDATE": "4",
    "HOST_ONLY_FIRST_TASK_CREDIT": "1",
    "START_MOI": "1",
    
    # Important 
    "SYM_MIN_CYCLES_BEFORE_REPRO": "100",  
    "SYM_HORIZ_TRANS_RES": "40",
    
    "HOST_AGE_MAX": "-1",
    "NUTRIENT_INTERACTION_MULTIPLIER": "7",
    "PARASITE_BASE_TASK_VALUE_PROP": "0.2"
}

special_decorators = [
    "__COPY_OVER"
]

# "HOST_REPRO_RES": "40",
# "HOST_MIN_CYCLES_BEFORE_REPRO": "200",
# "NUTRIENT_STEAL_PROP": "0.5",


combos.register_var("NUTRIENT_STEAL_PROP")
combos.register_var("HOST_MIN_CYCLES_BEFORE_REPRO")
combos.register_var("SYM_MIN_CYCLES_BEFORE_REPRO")


combos.add_val(
    "HOST_MIN_CYCLES_BEFORE_REPRO",
    ["160", "320", "640"]
)

combos.add_val(
    "NUTRIENT_STEAL_PROP",
    [".6", ".8", "1.0"]
)

combos.add_val(
    "HOST_REPRO_RES"
    ["20","40", "80", "160"]
)


def main():
    # Configure command line arguments
    parser = argparse.ArgumentParser(description="Generate SLURM submission scripts.")
    parser.add_argument("--data_dir", type=str, help="Where is the base output directory for each run?")
    parser.add_argument("--config_dir", type=str, help="Where is the configuration directory for experiment?")
    parser.add_argument("--replicates", type=int, default=default_num_replicates, help="How many replicates should we run of each condition?")
    parser.add_argument("--job_dir", type=str, default=None, help="Where to output these job files? If none, put in 'jobs' directory inside of the data_dir")
    parser.add_argument("--seed_offset", type=int, default=default_seed_offset, help="Value to offset random number seeds by")
    parser.add_argument("--time_request", type=str, default=default_job_time_request, help="How long to request for each job on hpc?")
    parser.add_argument("--mem", type=str, default=default_job_mem_request, help="How much memory to request for each job?")
    parser.add_argument("--runs_per_subdir", type=int, default=-1, help="How many replicates to clump into job subdirectories")
    parser.add_argument("--repo_dir", type=str, help="Where is the repository for this experiment?")
    parser.add_argument("--hpc_env_file", type=str, default=None, help="Bash script that loads correct hpc modules")

    args = parser.parse_args()

    # Load in the base slurm file
    base_slurm_script = ""
    with open(base_slurm_script_fpath, "r") as fp:
        base_slurm_script = fp.read()

    # Get list of all combinations to run
    combo_list = combos.get_combos()
    for c in combo_list:
        print(c)

    # Calculate how many total jobs we have, and what the last id will be
    num_jobs = args.replicates * len(combo_list)

    # Echo chosen options
    print(f'Generating {num_jobs} jobs across {len(combo_list)} slurm files!')
    print(f' - Data directory: {args.data_dir}')
    print(f' - Config directory: {args.config_dir}')
    print(f' - Repository directory: {args.repo_dir}')
    print(f' - Job directory: {args.job_dir}')
    print(f' - Replicates: {args.replicates}')
    print(f' - Time Request: {args.time_request}')
    print(f' - Memory: {args.mem}')
    print(f' - Seed offset: {args.seed_offset}')

    # If no job_dir provided, default to data_dir/jobs
    if args.job_dir == None:
        args.job_dir = os.path.join(args.data_dir, "jobs")

    # Create a job file for each condition
    cur_job_id = 0
    cond_i = 0
    cur_subdir_run_cnt = 0
    cur_run_subdir_id = 0

    # Localize some commandline args for convenience ( less typing :) )
    config_dir = args.config_dir
    data_dir = args.data_dir
    job_dir = args.job_dir
    repo_dir = args.repo_dir

    # -- Generate slurm script for each condition --
    for condition_info in combo_list:
        # print(condition_info)
        # Calc current seed (all runs should have a unique random seed).
        cur_seed = args.seed_offset + (cur_job_id * args.replicates)
        filename_prefix = f'RUN_C{cond_i}'
        file_str = base_slurm_script
        file_str = file_str.replace("<<TIME_REQUEST>>", args.time_request)
        file_str = file_str.replace("<<ARRAY_ID_RANGE>>", f"1-{args.replicates}")
        file_str = file_str.replace("<<MEMORY_REQUEST>>", args.mem)
        file_str = file_str.replace("<<JOB_NAME>>", f"C{cond_i}")
        file_str = file_str.replace("<<CONFIG_DIR>>", config_dir)
        file_str = file_str.replace("<<REPO_DIR>>", repo_dir)
        file_str = file_str.replace("<<EXEC>>", executable)
        file_str = file_str.replace("<<JOB_SEED_OFFSET>>", str(cur_seed))
        

        if args.hpc_env_file is None:
            file_str = file_str.replace("<<SETUP_HPC_ENV>>", "")
        else:
            file_str = file_str.replace("<<SETUP_HPC_ENV>>", f"source {args.hpc_env_file}")

        # Configure run directory
        run_dir = os.path.join(data_dir, f"{filename_prefix}_"+"${SEED}")
        file_str = file_str.replace("<<RUN_DIR>>", run_dir)

        # -- Build command line parameters --
        # Start by adding in fixed parameters
        cmd_line_params = {param:fixed_parameters[param] for param in fixed_parameters}
        cmd_line_params["SEED"] = "${SEED}"
        # Then, add condition-specific parameters (starting with non-__COPY_OVER params)
        for param in condition_info:
            if any([dec in param for dec in special_decorators]):
                continue
            cmd_line_params[param] = condition_info[param]

        # Build command line parameter string (including any 'copy_over' parameters)
        params = list(cmd_line_params.keys())
        params.sort()
        set_params = [f"-{param} {cmd_line_params[param]}" for param in params]
        copy_params = [condition_info[key] for key in condition_info if "__COPY_OVER" in key]
        run_param_str = " ".join(set_params + copy_params)

        run_cmds = []
        run_cmds.append(f'RUN_PARAMS="{run_param_str}"')
        run_cmds.append('echo "./${EXEC} ${RUN_PARAMS}" > cmd.log')
        run_cmds.append('./${EXEC} ${RUN_PARAMS} > run.log')
        run_cmds_str = "\n".join(run_cmds)

        file_str = file_str.replace("<<RUN_CMDS>>", run_cmds_str)

        # -- Build run configuration copy commands --
        config_cp_cmds = []
        config_cp_cmds.append("cp ${CONFIG_DIR}/*.cfg .")
        config_cp_cmds.append("cp ${CONFIG_DIR}/*.json .")
        config_cp_cmds_str = "\n".join(config_cp_cmds)
        file_str = file_str.replace("<<CONFIG_CP_CMDS>>", config_cp_cmds_str)

        # -- Write job submission file --
        cur_job_dir = job_dir if args.runs_per_subdir == -1 else os.path.join(job_dir, f"job-set-{cur_run_subdir_id}")
        utils.mkdir_p(cur_job_dir)
        with open(os.path.join(cur_job_dir, f'{filename_prefix}.sb'), 'w') as fp:
            fp.write(file_str)

        # Update condition id and current job id
        cur_job_id += 1
        cond_i += 1
        cur_subdir_run_cnt += args.replicates
        if cur_subdir_run_cnt > (args.runs_per_subdir - args.replicates):
            cur_subdir_run_cnt = 0
            cur_run_subdir_id += 1

if __name__ == "__main__":
    main()