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


def stop():
    """Throw the playroom away."""
    subprocess.run(
        ["docker", "rm", "-f", CONTAINER_NAME],
        capture_output=True,
        text=True,
    )


def verify_network_disabled():
    """Confirm Docker started the playroom with networking disabled."""
    result = subprocess.run(
        [
            "docker", "inspect",
            "--format={{.HostConfig.NetworkMode}}",
            CONTAINER_NAME,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    network_mode = result.stdout.strip()
    if network_mode != "none":
        raise RuntimeError(
            "Sandbox must use Docker network mode 'none'; "
            f"got {network_mode!r}."
        )
    print("Good: no internet inside the sandbox")


if __name__ == "__main__":
    test_commands = [
        "whoami",
        "pwd",
        "ls -R",
        "cat main.tf",
        "cat secrets/api_key.txt",
    ]

    print("Starting the sandbox...")
    start()

    try:
        verify_network_disabled()
        for cmd in test_commands:
            result = run_command(cmd)
            print("\n$ " + cmd)
            print(result["output"].strip())
            print("(exit code: " + str(result["exit_code"]) + ")")
    finally:
        stop()

    print("\nSandbox stopped and removed. Step 1 works!")
