'''
Aggregate data.
This script generates the following output files:
- A summary file with one line per-replicate.
'''

import argparse
import os
import sys
import pathlib
from scipy.stats import entropy

# Add scripts directory to path, import utilities from scripts directory.
sys.path.append(
    os.path.join(
        pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parents[2],
        "scripts"
    )
)
import utilities as utils

run_identifier = "RUN_"

# Run configuration fields to keep as fields in summary output file.
run_cfg_fields_summary = {
    "VERTICAL_TRANSMISSION",
    "GRID_X",
    "GRID_Y",
    "UPDATES",
    "HORIZ_TRANS",
    "GRID",
    "OUSTING",
    "SYM_VERT_TRANS_RES",
    "ENABLE_STRESS",
    "STRESS_TYPE",
    "ENABLE_HEALTH",
    "HEALTH_TYPE",
    "PARASITE_CYCLE_LOSS_PROP",
    "HEALTH_INTERACTION_CHANCE",
    "PARASITE_CYCLE_STEAL_MULTIPLIER",
    "PARASITE_BASE_CYCLE_PROP",
    "MUTUALIST_CYCLE_DONATE_MULTIPLIER",
    "MUTUALIST_CYCLE_GAIN_PROP",
    "ENABLE_NUTRIENT",
    "HOST_ONLY_FIRST_TASK_CREDIT",
    "SYM_ONLY_FIRST_TASK_CREDIT",
    "SGP_MUT_PER_BIT_RATE",
    "VT_TASK_MATCH",
    "CYCLES_PER_UPDATE",
    "HOST_MIN_CYCLES_BEFORE_REPRO",
    "SYM_MIN_CYCLES_BEFORE_REPRO",
    "HOST_REPRO_RES",
    "SYM_HORIZ_TRANS_RES",
    "STRESS_FREQUENCY",
    "PARASITE_DEATH_CHANCE",
    "PARASITE_NUM_OFFSPRING_ON_STRESS_INTERACTION",
    "START_MOI",
    "BASE_DEATH_CHANCE",
    "SEED"
}

run_cfg_fields_time_series = {
    "START_MOI",
    "SEED",
    "CYCLES_PER_UPDATE",
    "HOST_MIN_CYCLES_BEFORE_REPRO",
    "HOST_REPRO_RES",
    "HOST_ONLY_FIRST_TASK_CREDIT"
}

org_counts_fields_time_series = {
    "host_count",
    "hosted_sym_count"
}

cur_update_info_fields_time_series = {
    "NOT_in_host_profile_counts",
    "NAND_in_host_profile_counts",
    "OR_NOT_in_host_profile_counts",
    "AND_in_host_profile_counts",
    "OR_in_host_profile_counts",
    "AND_NOT_in_host_profile_counts",
    "NOR_in_host_profile_counts",
    "XOR_in_host_profile_counts",
    "EQU_in_host_profile_counts",
    "NOT_in_sym_profile_counts",
    "NAND_in_sym_profile_counts",
    "OR_NOT_in_sym_profile_counts",
    "AND_in_sym_profile_counts",
    "OR_in_sym_profile_counts",
    "AND_NOT_in_sym_profile_counts",
    "NOR_in_sym_profile_counts",
    "XOR_in_sym_profile_counts",
    "EQU_in_sym_profile_counts",
    "NOT_in_host_parent_org_counts",
    "NAND_in_host_parent_org_counts",
    "OR_NOT_in_host_parent_org_counts",
    "AND_in_host_parent_org_counts",
    "OR_in_host_parent_org_counts",
    "AND_NOT_in_host_parent_org_counts",
    "NOR_in_host_parent_org_counts",
    "XOR_in_host_parent_org_counts",
    "EQU_in_host_parent_org_counts",
    "NOT_in_sym_parent_org_counts",
    "NAND_in_sym_parent_org_counts",
    "OR_NOT_in_sym_parent_org_counts",
    "AND_in_sym_parent_org_counts",
    "OR_in_sym_parent_org_counts",
    "AND_NOT_in_sym_parent_org_counts",
    "NOR_in_sym_parent_org_counts",
    "XOR_in_sym_parent_org_counts",
    "EQU_in_sym_parent_org_counts"
}

transmission_rates_fields_time_series = {

}

def extract_summary_data(data, target_update, fields, prefix=None):
        info = {}

        # Grab the data line that matches the target update for this run
        summary_data = [
            line
            for line in data
            if (target_update is None) or (int(line["update"]) == target_update)
        ][-1]

        # Add specified fields to run summary data
        for field in summary_data:
            if field in fields:
                if prefix is None:
                    info[field] = summary_data[field]
                else:
                    info[f"{prefix}_{field}"] = summary_data[field]

        return info

def add_time_series_info(
    time_series_data,
    run_data,
    fields,
    prefix = None
):
    # For each relevant line in run data, add relevant fields to time_series_data
    for line in run_data:
        # Skip over updates we don't want to sample
        line_update = int(line["update"])
        if not line_update in time_series_data:
            continue
        for field in line:
            if field in fields:
                if prefix is None:
                    time_series_data[line_update][field] = line[field]
                else:
                    time_series_data[line_update][f"{prefix}_{field}"] = line[field]


def main():
    parser = argparse.ArgumentParser(description = "Run submission script.")
    parser.add_argument("--data_dir", type=str, help="Where is the base output directory for each run?")
    parser.add_argument("--dump_dir", type=str, help="Where to dump this?", default=".")
    parser.add_argument("--summary_update", type=int, help="Update to pull summary data for?")
    parser.add_argument("--time_series_units", type=str, default="interval", choices=["interval", "total"], help="Unit for resolution of time series")
    parser.add_argument("--time_series_resolution", type=int, default=1, help="What resolution should we collect time series data at?")

    args = parser.parse_args()
    data_dir = args.data_dir
    dump_dir = args.dump_dir
    target_update = args.summary_update
    time_series_units = args.time_series_units
    time_series_resolution = args.time_series_resolution

    if not os.path.exists(data_dir):
        print("Unable to find data directory.")
        exit(-1)

    # Verify time series resolution >= 1
    if time_series_resolution < 1:
        print("Time series resolution must be >= 1")
        exit(-1)

    utils.mkdir_p(dump_dir)

    # Aggregate run directories.
    run_dirs = [run_dir for run_dir in os.listdir(data_dir) if run_identifier in run_dir]
    print(f"Found {len(run_dirs)} run directories.")

    # Create file to hold time series data
    time_series_content = []    # This will hold all the lines to write out for a single run; written out for each run.
    time_series_header = None   # Holds the time series file header (verified for consistency across runs)
    time_series_fpath = os.path.join(dump_dir, f"time_series.csv")

    with open(time_series_fpath, "w") as fp:
        fp.write("")

    # For each run directory...
    # summary_header = None
    summary_content_lines = []
    incomplete_runs = []
    for run_dir_i in range(len(run_dirs)):
        run_dir = run_dirs[run_dir_i]
        print(f"...({run_dir_i + 1}/{len(run_dirs)}) aggregating from {run_dir}")
        run_path = os.path.join(data_dir, run_dir)

        run_summary_info = {} # Hold summary information about this run.
        time_series_info = {} # Hold time series information. Indexed by update.

        ########################################
        # Extract run parameters
        ########################################
        run_cfg_path = os.path.join(run_path, "output", "run_config.csv")
        if not os.path.isfile(run_cfg_path):
            print("Run did not finish, skipping")
            incomplete_runs.append(run_dir)
            continue

        run_cfg_data = utils.read_csv(run_cfg_path)
        run_params = {}
        for line in run_cfg_data:
            param = line["parameter"]
            value = line["value"]
            run_params[param] = value
            # Add a subset of parameters to summary information for this run.
            if param in run_cfg_fields_summary:
                run_summary_info[param] = value

        max_pop_size = 0
        if run_params["POP_SIZE"] == "-1":
            max_pop_size = int(run_params["GRID_X"]) * int(run_params["GRID_Y"])
        else:
            max_pop_size = int(run_params["POP_SIZE"])

        run_summary_info["max_pop_size"] = max_pop_size

        ########################################
        # Extract data from OrganismCounts.csv
        ########################################
        org_counts_path = os.path.join(run_path, "output", "OrganismCounts.csv")
        org_counts_data = utils.read_csv(org_counts_path)

        # --- Analyze updates represented, setup time series info --
        # Grab list of updates represented in data
        updates = [int(row["update"]) for row in org_counts_data]
        if len(updates) == 0:
            continue

        # Did run finish with respect to target update?
        run_finished_target = target_update in updates

        # Extract time series updates (only if run reached target)
        time_series_updates = utils.filter_time_points(
            updates,
            method = time_series_units,
            resolution = time_series_resolution
        ) if run_finished_target else []
        time_series_updates = set(time_series_updates)
        # Add run cfg information to time_series info
        time_series_info = {
            update:{field:run_params[field] for field in run_cfg_fields_time_series}
            for update in time_series_updates
        }
        for update in time_series_updates:
            time_series_info[update]["update"] = update

        run_target_update = utils.nearest(target_update, updates)
        run_summary_info["update"] = run_target_update
        run_summary_info["reached_target_update"] = run_finished_target
        # ---

        # Extract summary info
        org_counts_fields = set(org_counts_data[0].keys())
        org_counts_fields.remove("update")
        run_summary_info.update(
            extract_summary_data(
                data = org_counts_data,
                target_update = run_target_update,
                fields = org_counts_fields,
                prefix = "OrgCounts"
            )
        )

        # Extract time series info
        if run_finished_target:
            add_time_series_info(
                time_series_data = time_series_info,
                run_data = org_counts_data,
                fields = org_counts_fields_time_series,
                prefix = "OrgCounts"
            )

        del org_counts_data

        ########################################
        # Extract data from CurrentUpdateInfo.csv
        ########################################
        cur_update_info_path = os.path.join(run_path, "output", "CurrentUpdateInfo.csv")
        cur_update_info_data = utils.read_csv(cur_update_info_path)

        # Extract summary info
        cur_update_info_fields = set(cur_update_info_data[0].keys())
        cur_update_info_fields.remove("update")
        run_summary_info.update(
            extract_summary_data(
                data = cur_update_info_data,
                target_update = run_target_update,
                fields = cur_update_info_fields,
                prefix = "CurUpdate"
            )
        )

        # Extract time series info
        if run_finished_target:
            add_time_series_info(
                time_series_data = time_series_info,
                run_data = cur_update_info_data,
                fields = cur_update_info_fields_time_series,
                prefix = "CurUpdate"
            )

        ########################################
        # Extract data from TransmissionRates.csv
        ########################################
        transmission_rates_path = os.path.join(run_path, "output", "TransmissionRates.csv")
        transmission_rates_data = utils.read_csv(transmission_rates_path)

        # Extract summary info
        transmission_rates_fields = set(transmission_rates_data[0].keys())
        transmission_rates_fields.remove("update")
        run_summary_info.update(
            extract_summary_data(
                data = transmission_rates_data,
                target_update = run_target_update,
                fields = transmission_rates_fields,
                prefix = "TransmissionRates"
            )
        )

        # Extract time series info
        if run_finished_target:
            add_time_series_info(
                time_series_data = time_series_info,
                run_data = transmission_rates_data,
                fields = transmission_rates_fields_time_series,
                prefix = "TransmissionRates"
            )

        ########################################
        # Add summary info to summary content lines
        summary_content_lines.append(run_summary_info)

        ############################################################
        # Output time series data for this run
        if run_finished_target:
            # Order the updates
            time_series_update_order = list(time_series_updates)
            time_series_update_order.sort()
            # Order the fields
            time_series_fields = list(time_series_info[time_series_update_order[0]].keys())
            time_series_fields.sort()
            # If we haven't written the header, write it.
            write_header = False
            if time_series_header == None:
                write_header = True
                time_series_header = ",".join(time_series_fields)
            elif time_series_header != ",".join(time_series_fields):
                print("Time series header mismatch!")
                exit(-1)

            # Write time series content line-by-line
            time_series_content = []
            for u in time_series_update_order:
                time_series_content.append(",".join([str(time_series_info[u][field]) for field in time_series_fields]))
            with open(time_series_fpath, "a") as fp:
                if write_header:
                    fp.write(time_series_header)
                fp.write("\n")
                fp.write("\n".join(time_series_content))
            time_series_content = []
        ############################################################
    # Write summary info out
    summary_path = os.path.join(dump_dir, "summary.csv")
    utils.write_csv(summary_path, summary_content_lines)

    # print incomplete runs
    print("Incomplete runs:")
    print("\n".join(incomplete_runs))


if __name__ == "__main__":
    main()