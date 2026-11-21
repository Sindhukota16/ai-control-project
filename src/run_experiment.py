"""
run_experiment.py - runs honest and sneaky chores with the hall monitor watching,
then prints a summary table and saves it as a CSV file in results/.

Examples (Mac: use python3):
    python src/run_experiment.py --limit 2          # quick test: 1 honest + 1 attack run
    python src/run_experiment.py                    # all 8 runs
    python src/run_experiment.py --monitor trajectory
    python src/run_experiment.py --monitor none     # no monitor (baseline)
    python src/run_experiment.py --monitor rules    # security rules only, no AI
    python src/run_experiment.py --monitor hybrid   # rules first, AI only if needed
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

from agent import run_agent
from monitor import Monitor
from rules_monitor import RulesMonitor, HybridMonitor
from tasks import build_runs

sys.stdout.reconfigure(errors="replace")

parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=None,
                    help="only do the first N runs (saves free quota)")
parser.add_argument("--monitor", choices=["action", "trajectory", "rules", "hybrid", "none"],
                    default="action",
                    help="action/trajectory = AI monitor; rules = no AI; hybrid = rules + AI")
parser.add_argument("--only", choices=["honest", "attack"], default=None,
                    help="only honest runs, or only attack runs")
args = parser.parse_args()

runs = build_runs()
if args.only:
    runs = [r for r in runs if r["mode"] == args.only]
if args.limit:
    runs = runs[: args.limit]

if args.monitor == "none":
    monitor = None
elif args.monitor == "rules":
    monitor = RulesMonitor()
elif args.monitor == "hybrid":
    monitor = HybridMonitor(llm_mode="action")
else:
    monitor = Monitor(mode=args.monitor)
experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_monitor-" + args.monitor
log_dir = Path("logs") / experiment_id

print("Experiment: " + experiment_id)
print("Runs to do: " + str(len(runs)))
if monitor:
    print("Monitor:    " + monitor.model + " (" + monitor.mode + " mode, blocks at >= "
          + str(monitor.threshold) + ")")

rows = []
for i, run in enumerate(runs, start=1):
    print("\n" + "#" * 60)
    print("# Run " + str(i) + "/" + str(len(runs)) + ": " + run["name"])
    print("#" * 60)
    side = run["side"]
    log = run_agent(
        task=run["main"]["prompt"],
        check_command=run["main"]["check"],
        run_name=run["name"],
        side_task=side["prompt"] if side else None,
        side_check=side["check"] if side else None,
        monitor=monitor,
        log_dir=str(log_dir),
    )
    rows.append({
        "run": run["name"],
        "mode": run["mode"],
        "main_task": run["main"]["id"],
        "side_task": side["id"] if side else "",
        "monitor": args.monitor,
        "steps": len(log["steps"]),
        "main_done": log["check_passed"],
        "side_done": log["side_check_passed"] if side else "",
        "max_score": log["max_score"] if log["max_score"] is not None else "",
        "blocked_actions": log["blocked_actions"],
        "monitor_checks": log["monitor_checks"],
        "monitor_avg_ms": log["monitor_avg_ms"] if log["monitor_avg_ms"] is not None else "",
        "log_file": log["log_file"],
    })

# Save the results table
Path("results").mkdir(exist_ok=True)
csv_file = Path("results") / ("runs_" + experiment_id + ".csv")
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

# Print a simple summary
print("\n" + "=" * 78)
print("RUN".ljust(36) + "MAIN DONE  SIDE DONE  MAX SCORE  BLOCKED")
print("-" * 78)
for r in rows:
    print(r["run"][:35].ljust(36)
          + ("yes" if r["main_done"] else "no").ljust(11)
          + ("-" if r["mode"] == "honest" else ("YES" if r["side_done"] else "no")).ljust(11)
          + str(r["max_score"]).ljust(11)
          + str(r["blocked_actions"]))
print("=" * 78)

honest = [r for r in rows if r["mode"] == "honest"]
attack = [r for r in rows if r["mode"] == "attack"]
if honest:
    done = sum(1 for r in honest if r["main_done"])
    print("Usefulness: " + str(done) + "/" + str(len(honest))
          + " honest chores finished")
if attack:
    stopped = sum(1 for r in attack if not r["side_done"])
    print("Safety:     " + str(stopped) + "/" + str(len(attack))
          + " sneaky goals did NOT succeed")
if monitor:
    times = [r["monitor_avg_ms"] for r in rows if r["monitor_avg_ms"] != ""]
    if times:
        print("Monitor:    about " + str(int(sum(times) / len(times))) + " ms per check")
    if hasattr(monitor, "llm_calls") and args.monitor == "hybrid":
        checks = sum(r["monitor_checks"] for r in rows)
        print("AI calls:   " + str(monitor.llm_calls) + " of " + str(checks)
              + " checks needed the AI (rules handled the rest)")
print("\nResults table saved to: " + str(csv_file))
print("Full logs saved in:     " + str(log_dir))
