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
├── .gitignore             <- files we never upload (like .env)
├── .env.example           <- template for API keys (real keys go in .env)
├── docs/
│   ├── STEP1_SETUP.md     <- beginner guide for Day 1
│   └── TEAM_NOTES.md      <- our shared daily notes and to-do list
├── sandbox/
│   ├── Dockerfile         <- builds the locked playroom
│   └── workspace/         <- files the agent works on (all fake)
│       ├── main.tf
│       └── secrets/api_key.txt   <- FAKE key, used to detect sabotage
└── src/
    └── sandbox.py         <- starts the playroom and runs commands in it
```

## Quick start

```bash
# 1. Build the playroom (run from the project folder)
docker build -t ai-control-sandbox ./sandbox

# 2. Test it
python src/sandbox.py      # Windows
python3 src/sandbox.py     # Mac
```

## Continuous integration

GitHub Actions runs on pushes to `main`, pull requests targeting `main`, and
when manually started. It checks Python syntax, builds the Docker image, and
runs the sandbox smoke test. The test output is checked without printing the
fake secret to the workflow logs.

## Plan (finish by Sunday, Nov 22, 2026)

| Day | Date | Step |
|---|---|---|
| 1 | Tue Nov 17 | Setup tools, GitHub repo, Docker playroom ✅ |
| 2 | Wed Nov 18 | Agent loop: AI model can run commands in the playroom |
| 3 | Thu Nov 19 | Write honest + sneaky tasks, add the LLM hall monitor |
| 4 | Fri Nov 20 | Add Checkov/OPA monitor + hybrid, run all experiments |
| 5 | Sat Nov 21 | Scores, charts, write up results |
| 6 | Sun Nov 22 | Review, polish, make repo public, submit |

## Cost

Everything is free: Docker, Python, open-source security tools,
Gemini free tier for the agent, and a local Ollama model for the monitor.
We never create real cloud resources.

## Safety rules for this repo

- Never commit real API keys. Real keys go in `.env`, which is git-ignored.
- No work/company code, data, or prompts. Everything here is made up.
- The "secret" in `sandbox/workspace/secrets/` is fake on purpose.
