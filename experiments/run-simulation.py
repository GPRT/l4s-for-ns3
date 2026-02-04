import os
import subprocess
import time

# ================= CONFIG ========================
NS3_SCRIPT = "scratch/code"
OUTPUT_BASE = "exps/results"
NUM_RUNS = 30
# =================================================

def main():
    print(f"--- PHASE 1: EXECUTION ({NUM_RUNS} Runs) ---")
    print("Compiling ns-3...")
    try:
        subprocess.run(["./ns3", "build"], check=True)
    except subprocess.CalledProcessError:
        print("Compilation error! Aborting.")
        return

    start_time = time.time()

    for run_n in range(NUM_RUNS):
        output_dir = os.path.join(OUTPUT_BASE, f"run_{run_n}")
        os.makedirs(output_dir, exist_ok=True)

        # Check if this run was already completed (by checking if a key file exists)
        if os.path.exists(os.path.join(output_dir, "throughput.csv")):
            print(f"Run {run_n} already exists. Skipping...")
            continue

        print(f"Running Simulation {run_n + 1}/{NUM_RUNS}...")

        cmd = [
            "./ns3", "run",
            f"{NS3_SCRIPT} --pathOut={output_dir} --RngRun={run_n}"
        ]

        # Define the seed
        env = os.environ.copy()
        env["NS_GLOBAL_VALUE"] = f"RngRun={run_n}"

        try:
            # capture_output=False allows viewing ns-3 log in terminal if an error occurs
            subprocess.run(cmd, env=env, check=True)
        except subprocess.CalledProcessError as e:
            print(f"!!! Run {run_n} Failed !!!")
            # Don't stop the loop, try the next one

    elapsed = time.time() - start_time
    print(f"\n--- End of Simulations. Total time: {elapsed/60:.2f} min ---")

if __name__ == "__main__":
    main()