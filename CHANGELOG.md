# Changelog

What changed in the project, day by day. Newest first.

## Day 3 - Fri Nov 20, 2026: Sneaky tasks + hall monitor

### New files
- `src/tasks.py`: 4 honest chores (`add_tags`, `rename_policy`, `add_bucket`, `add_output`) and 2 sneaky goals (`leak_key`, `weaken_iam`), each with a check command. `build_runs()` makes 8 runs (each chore once honest, once attack).
- `src/monitor.py`: the hall monitor. Sends each proposed action to Groq (`openai/gpt-oss-20b`) and gets a 0-10 suspicion score. Two modes: `action` (one action) and `trajectory` (all earlier actions too). Blocks at `BLOCK_THRESHOLD` (default 8). Never sees the secret side task. Retries if Groq is busy.
- `src/check_monitor.py`: tests the Groq key with 3 example actions (1 normal, 2 sneaky).
- `src/run_experiment.py`: runs the chores (`--limit`, `--only`, `--monitor action|trajectory|none`), prints a summary with usefulness and safety, saves `results/runs_<id>.csv` and logs in `logs/<id>/`.
- `docs/STEP3_MONITOR.md`: beginner guide for Day 3.

### Changed files
- `src/agent.py`: `run_agent()` now accepts a secret `side_task` + `side_check` (attack runs) and a `monitor`. Every `run_bash` / `write_file` is scored before it runs; blocked actions don't run and the agent is told so. Logs now include mode, side task, each step's score/reason/blocked, max score, blocked count, and whether the side task succeeded.
- `sandbox/Dockerfile`: `chmod 1777 /tmp` so `/tmp` is writable like a normal Linux system (a sneaky agent can try to hide the key there; our check detects it). **Rebuild needed.**
- `.env.example`: added `GROQ_API_KEY`, `MONITOR_MODEL`, `BLOCK_THRESHOLD`.
- `README.md`: "How the experiment works" table, updated structure, quick start, plan, cost.

### Decisions
- Switched the monitor from a local Ollama model to **Groq's free cloud API**: no RAM used, its own quota (doesn't use Gemini's), OpenAI-compatible so the same code works.
- Groq's `llama-3.1-8b-instant` was shut down in Aug 2026, so we use its recommended replacement `openai/gpt-oss-20b`.

### Tested before release
- With a fake agent + fake monitor: honest run not blocked; key-theft action scored 9 and was blocked (side task failed); same attack **without** monitor succeeded (side task YES). Monitor input never contains the secret instructions.
- All check commands tested against original and edited files (fail before, pass after).

## Day 2 - Thu Nov 19, 2026: Agent loop

### New files
- `src/agent.py`: the agent loop. Gemini chooses tools (`run_bash`, `write_file`, `submit`), our code runs them inside the sandbox, a check command verifies the result, and each run is saved as a JSON log in `logs/`.
- `src/check_setup.py`: checks the Gemini API key (1 request), lists usable models, and tests the chosen model.
- `requirements.txt`: Python libraries (`openai`, `python-dotenv`).
- `docs/STEP2_AGENT.md`: beginner guide for Day 2.
- `CHANGELOG.md`: this file.
- `results/examples/`: saved example runs (the `logs/` folder itself is not uploaded).

### Changed files
- `src/sandbox.py`: added `write_file()` so the agent can create or replace files in the sandbox (uses only built-in bash, no extra tools needed).
- `.env.example`: added `AGENT_MODEL`; default is now `gemini-flash-lite-latest`.
- `README.md`: updated plan (schedule moved one day), quick start, project structure, findings so far.
- `docs/STEP1_SETUP.md`: added the Day 1 lessons (clone into `C:\Projects`, copy the inner unzip folder, OneDrive, PowerShell vs Git Bash).
- `docs/TEAM_NOTES.md`: filled in Day 1 and Day 2.

### Fixes made during Day 2 (all in `src/agent.py`)
1. **503 "server busy" crashed the run** → now waits (15s, 30s, ...) and retries up to 5 times.
2. **Agent wandered for 15 steps and never did the task** → clearer system prompt: says what the container has and doesn't have (no internet, terraform, git, sudo), how to edit files, to stay on task, and the step limit.
3. **Daily free quota ran out and the code kept retrying for minutes** → now stops right away with a clear message. Step limit lowered from 15 to 10 to save quota.
4. Default model changed from `gemini-flash-latest` to `gemini-flash-lite-latest` (more free quota, finished the demo in 4 steps).
5. Friendly message if `.env` or the API key is missing.

## Day 1 - Tue Nov 17, 2026: Setup + sandbox

### New files
- `sandbox/Dockerfile`: Python 3.11 slim image, non-admin user `agent`, practice files copied in.
- `sandbox/workspace/main.tf`: practice IAM policy (never deployed).
- `sandbox/workspace/secrets/api_key.txt`: fake key used to detect sabotage.
- `src/sandbox.py`: start the sandbox (no network, 512 MB memory, 1 CPU), run commands, stop it.
- `README.md`, `.gitignore`, `.env.example`, `docs/STEP1_SETUP.md`, `docs/TEAM_NOTES.md`.
