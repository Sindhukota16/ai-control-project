"""
sandbox.py - start the Docker "playroom", run commands inside it, and clean up.

Run it with:
    Windows:  python src/sandbox.py
    Mac:      python3 src/sandbox.py
"""

import subprocess

IMAGE_NAME = "ai-control-sandbox"
CONTAINER_NAME = "ai-control-sandbox-run"


def start():
    """Start a fresh playroom with no internet and limited memory/CPU."""
    stop()  # remove any old copy first, so every run starts clean
    subprocess.run(
        [
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "--network", "none",   # no internet: secrets can't really leave
            "--memory", "512m",    # can't eat all your RAM
            "--cpus", "1",         # can't eat all your CPU
            IMAGE_NAME,
        ],
        capture_output=True,
        text=True,
        check=True,
    )


def run_command(command, timeout=30):
    """Run one bash command inside the playroom and return what it printed."""
    try:
        result = subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "bash", "-c", command],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "output": "Command took too long and was stopped."}

    output = (result.stdout + result.stderr)[-4000:]  # keep it short
    return {"exit_code": result.returncode, "output": output}


def write_file(path, content):
    """Create or replace a file inside the playroom (path is relative to /workspace)."""
    result = subprocess.run(
        [
            "docker", "exec", "-i", CONTAINER_NAME,
            "bash", "-c",
            'd="${1%/*}"; if [ "$d" != "$1" ]; then mkdir -p "$d"; fi; cat > "$1"',
            "_", path,
        ],
        input=content,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return {"exit_code": 0, "output": "Saved " + path}
    return {"exit_code": result.returncode, "output": result.stderr[-2000:]}


def stop():
    """Throw the playroom away."""
    subprocess.run(
        ["docker", "rm", "-f", CONTAINER_NAME],
        capture_output=True,
        text=True,
    )


if __name__ == "__main__":
    test_commands = [
        "whoami",
        "pwd",
        "ls -R",
        "cat main.tf",
        "cat secrets/api_key.txt",
        # This SHOULD fail, because the playroom has no internet:
        "timeout 5 bash -c 'echo > /dev/tcp/1.1.1.1/80' 2>/dev/null "
        "&& echo 'WARNING: internet is ON' || echo 'Good: no internet inside the sandbox'",
    ]

    print("Starting the sandbox...")
    start()

    for cmd in test_commands:
        result = run_command(cmd)
        print("\n$ " + cmd)
        print(result["output"].strip())
        print("(exit code: " + str(result["exit_code"]) + ")")

    stop()
    print("\nSandbox stopped and removed. Step 1 works!")
