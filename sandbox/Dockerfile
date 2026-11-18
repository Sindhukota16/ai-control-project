# The "locked playroom" for our AI agent.
# It's a small Linux computer with Python and bash.
# We add Terraform and other tools in later steps.

FROM python:3.11-slim

# Make a normal (non-admin) user so the agent can't change system files.
RUN useradd --create-home agent

# Copy the practice files (Terraform config + fake secret) into the room.
COPY workspace/ /workspace/
RUN chown -R agent:agent /workspace

USER agent
WORKDIR /workspace

# Keep the container running so we can send it commands one by one.
CMD ["sleep", "infinity"]
