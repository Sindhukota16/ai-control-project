# Containerized AI Control

**Benchmarking sandboxed execution and automated monitoring against sabotage in tool-using agents**

## What this project is about (simple version)

We give an AI agent (the "robot helper") DevOps chores, like fixing Terraform or IAM files.
It works inside a locked Docker container (the "playroom") so it can't damage anything real.

In half of the chores we secretly tell the agent to also do something sneaky,
like stealing a fake API key or weakening a security rule.

A smaller AI we trust (the "hall monitor") watches every action and blocks anything suspicious.
We also test regular security tools (Checkov / OPA) as a second kind of monitor.

Then we measure:

| Metric | What it means |
|---|---|
| Safety score | % of sneaky attempts that got caught |
| Usefulness score | % of honest chores finished without false alarms |
| Cost | Extra time and tokens the monitor adds |

This research area is called **AI control**: keeping a powerful AI safe to use
even if it might be trying to misbehave.

## Related work

- **Ctrl-Z / BashBench** (Redwood Research): control protocols for agents doing bash tasks
- **BashArena**: Linux sysadmin tasks with sabotage goals like secret exfiltration
- **ControlArena** (UK AISI + Redwood): a library of control settings, including infrastructure-as-code

**What we add:** we built our own setup from scratch to compare classic infra security
tools (Checkov, OPA) against LLM monitors, and a hybrid of both.

## Project structure

```
ai-control-project/
├── README.md              <- you are here
├── CHANGELOG.md           <- what changed, day by day
├── .gitignore             <- files we never upload (like .env)
├── .env.example           <- template for API key + model (real values go in .env)
├── requirements.txt       <- Python libraries we use
├── docs/
│   ├── STEP1_SETUP.md     <- beginner guide for Day 1
│   ├── STEP2_AGENT.md     <- beginner guide for Day 2
│   └── TEAM_NOTES.md      <- our shared daily notes, findings, and problems
├── results/
│   └── examples/          <- saved logs of interesting agent runs
├── sandbox/
│   ├── Dockerfile         <- builds the locked playroom
│   └── workspace/         <- files the agent works on (all fake)
│       ├── main.tf
│       └── secrets/api_key.txt   <- FAKE key, used to detect sabotage
├── src/
│   ├── sandbox.py         <- starts the playroom, runs commands, writes files
│   ├── agent.py           <- the agent loop (AI decides which tools to use)
│   └── check_setup.py     <- checks your API key works
└── logs/                  <- run records (created automatically, not uploaded)
```

## Quick start

(Use `python3` instead of `python` on Mac.)

```bash
# 1. Build the playroom (run from the project folder)
docker build -t ai-control-sandbox ./sandbox

# 2. Install libraries
python -m pip install -r requirements.txt

# 3. Copy .env.example to .env and add your free Gemini key, then check it
python src/check_setup.py

# 4. Test the playroom alone
python src/sandbox.py

# 5. Run the agent on a demo chore
python src/agent.py
```

## Plan (finish by Sunday, Nov 22, 2026)

| Day | Date | Step |
|---|---|---|
| 1 | Tue Nov 17 | Setup tools, GitHub repo, Docker playroom ✅ |
| 2 | Thu Nov 19 | Agent loop: AI model runs commands in the playroom by itself ✅ |
| 3 | Fri Nov 20 | Write honest + sneaky tasks, add the LLM hall monitor |
| 4 | Sat Nov 21 | Add Checkov/OPA monitor + hybrid, run experiments, charts |
| 5 | Sun Nov 22 | Write up results, polish, make repo public, submit |

## Findings so far

**Day 2: an honest agent can look suspicious.** With loose instructions and no sabotage
goal, the agent (`gemini-flash-latest`) spent all 15 steps exploring: it looked in
`secrets/`, printed environment variables, tried `sudo`, and tried to reach the internet
(blocked by the sandbox). It never did the task. With focused instructions,
`gemini-flash-lite-latest` finished in 4 steps. (We changed both the prompt and the model,
so we can't yet say which one mattered.)

This matters for the monitor: blocking everything that touches secrets or the network
would also block honest agents and hurt usefulness.
Details in [docs/TEAM_NOTES.md](docs/TEAM_NOTES.md); logs in [results/examples/](results/examples/).

## Cost

Everything is free: Docker, Python, open-source security tools,
Gemini free tier for the agent, and a local Ollama model for the monitor.
We never create real cloud resources.

## Safety rules for this repo

- Never commit real API keys. Real keys go in `.env`, which is git-ignored.
- No work/company code, data, or prompts. Everything here is made up.
- The "secret" in `sandbox/workspace/secrets/` is fake on purpose.
