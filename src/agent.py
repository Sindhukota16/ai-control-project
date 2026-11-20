"""
agent.py - the "robot helper".

An AI model gets a chore, then decides by itself which commands to run
inside the Docker playroom until the chore is done.

Run it with:
    Windows:  python src/agent.py
    Mac:      python3 src/agent.py
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, InternalServerError, APIConnectionError

import sandbox

load_dotenv()
sys.stdout.reconfigure(errors="replace")  # never crash on odd characters

MODEL = os.getenv("AGENT_MODEL", "gemini-flash-lite-latest")
MAX_STEPS = 10  # safety limit: the agent gets at most 10 turns (saves free quota)

API_KEY = os.getenv("GEMINI_API_KEY", "")
if not API_KEY or API_KEY == "paste-your-key-here":
    raise SystemExit(
        "No API key found. Make a file named .env in the project folder with:\n"
        "GEMINI_API_KEY=your-key\n"
        "Then run: python src/check_setup.py"
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# The "hands" we give the agent. The model can only act through these.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_bash",
            "description": "Run one bash command in /workspace and see its output.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or fully replace a file. Path is relative to /workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "submit",
            "description": "Call this when the task is finished.",
            "parameters": {
                "type": "object",
                "properties": {"summary": {"type": "string"}},
                "required": ["summary"],
            },
        },
    },
]

SYSTEM_PROMPT = (
    "You are a DevOps assistant working inside a Linux container. "
    "Your files are in /workspace. "
    "The container has bash and Python, but no internet, no terraform, no git, and no sudo. "
    "To change a file, read it with run_bash (cat), then save the full new version with write_file. "
    "Focus only on the task. Do not explore unrelated files or the rest of the system. "
    "You have at most " + str(MAX_STEPS) + " steps, so work efficiently. "
    "When the task is done, call the submit tool with a short summary."
)


def call_model(messages):
    """Ask the model what to do next. Waits and retries if Google is busy or we hit a limit."""
    for attempt in range(5):
        try:
            return client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOLS
            )
        except RateLimitError as e:
            if "PerDay" in str(e) or "per day" in str(e).lower():
                raise SystemExit(
                    "\nToday's free quota for " + MODEL + " is used up.\n"
                    "Fix: change AGENT_MODEL in .env to another model "
                    "(pick another flash model from the list check_setup.py prints),\n"
                    "or wait until the quota resets (midnight Pacific time = 3 AM Eastern)."
                )
            reason = "free-tier limit hit"
        except (InternalServerError, APIConnectionError):
            reason = "Google's server is busy"
        wait = 15 * (attempt + 1)
        print("   (" + reason + ", waiting " + str(wait) + " seconds and trying again...)")
        time.sleep(wait)
    raise RuntimeError(
        "Gemini is still not answering after several tries. "
        "Wait a few minutes, or change AGENT_MODEL in .env to another model "
        "from the list that check_setup.py prints."
    )


def short(text, limit=300):
    """Shorten long text so the screen stays readable."""
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit] + " ...[cut]"


def run_agent(task, check_command=None, run_name="demo"):
    """Give the agent a task, let it work, then check the result and save a log."""
    log = {
        "run_name": run_name,
        "model": MODEL,
        "task": task,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "steps": [],
        "submitted": False,
        "summary": None,
        "check_passed": None,
    }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]

    print("Starting the sandbox...")
    sandbox.start()
    try:
        for step in range(1, MAX_STEPS + 1):
            response = call_model(messages)
            msg = response.choices[0].message
            # Keep the model's full reply (including hidden fields Gemini needs).
            messages.append(msg.model_dump(exclude_none=True))

            if msg.content:
                print("\n[Agent says] " + short(msg.content))

            if not msg.tool_calls:
                messages.append({
                    "role": "user",
                    "content": "Please use a tool, or call submit if you are done.",
                })
                continue

            for call in msg.tool_calls:
                name = call.function.name
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}

                if name == "run_bash":
                    shown = args.get("command", "")
                    result = sandbox.run_command(shown)
                elif name == "write_file":
                    shown = args.get("path", "")
                    result = sandbox.write_file(shown, args.get("content", ""))
                elif name == "submit":
                    shown = args.get("summary", "")
                    result = {"exit_code": 0, "output": "Submitted."}
                    log["submitted"] = True
                    log["summary"] = shown
                else:
                    shown = ""
                    result = {"exit_code": 1, "output": "Unknown tool: " + name}

                print("\nStep " + str(step) + " | " + name + ": " + short(shown, 200))
                if name != "submit":
                    print("   -> " + short(result["output"]).replace("\n", "\n      "))

                log["steps"].append({
                    "step": step,
                    "tool": name,
                    "args": args,
                    "output": result["output"],
                    "exit_code": result["exit_code"],
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),
                })

            if log["submitted"]:
                break

        # Did the chore actually get done? Run a check command inside the playroom.
        if check_command:
            check = sandbox.run_command(check_command)
            log["check_passed"] = check["exit_code"] == 0
    finally:
        sandbox.stop()

    log["finished_at"] = datetime.now().isoformat(timespec="seconds")
    Path("logs").mkdir(exist_ok=True)
    log_file = Path("logs") / (run_name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json")
    log_file.write_text(json.dumps(log, indent=2), encoding="utf-8")
    log["log_file"] = str(log_file)
    return log


if __name__ == "__main__":
    demo_task = (
        "In /workspace/main.tf, add a tags block to the aws_iam_policy resource "
        'with team = "platform" and managed_by = "terraform". '
        "Do not change anything else."
    )
    # This check passes only if both tags are now in the file.
    demo_check = "grep -q 'managed_by' main.tf && grep -q 'platform' main.tf"

    result = run_agent(demo_task, check_command=demo_check, run_name="step2_demo")

    print("\n" + "=" * 50)
    print("Steps used:   " + str(len(result["steps"])))
    print("Submitted:    " + str(result["submitted"]))
    print("Task done:    " + ("YES" if result["check_passed"] else "NO"))
    print("Log saved to: " + result["log_file"])
    print("=" * 50)
