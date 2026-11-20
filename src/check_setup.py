"""
check_setup.py - checks that your Gemini API key works before running the agent.

Run it with:
    Windows:  python src/check_setup.py
    Mac:      python3 src/check_setup.py
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY", "")
model = os.getenv("AGENT_MODEL", "gemini-flash-lite-latest")

# 1. Is there a key at all?
if not api_key or api_key == "paste-your-key-here":
    print("No API key found.")
    print("Make a file named .env in the project folder and add:  GEMINI_API_KEY=your-key")
    sys.exit(1)
print("1. Found your API key (starts with " + api_key[:6] + "...)")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which "flash" models can this key use?
try:
    names = sorted(m.id.replace("models/", "") for m in client.models.list())
    flash = [n for n in names if "flash" in n]
    print("2. Your key works. Flash models you can use:")
    for n in flash:
        print("     " + n)
except Exception as e:
    print("2. Could not list models. The key may be wrong.")
    print("   Error: " + str(e)[:300])
    sys.exit(1)

# 3. Can the chosen model actually answer?
try:
    reply = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello in five words."}],
    )
    print("3. Model '" + model + "' says: " + reply.choices[0].message.content.strip())
    print("\nAll good! You're ready to run the agent.")
except Exception as e:
    print("3. The model '" + model + "' did not answer.")
    print("   Error: " + str(e)[:300])
    print("   Fix: pick a name from the list above and put it in .env as AGENT_MODEL=that-name")
    sys.exit(1)
