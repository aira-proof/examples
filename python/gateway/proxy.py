"""Aira Gateway — transparent LLM proxy with policy enforcement.

The gateway sits between your code and the LLM provider. Every call is
authorized, policy-checked, and notarized — with ~15ms overhead.

Usage:
    pip install aira-sdk openai
    export AIRA_API_KEY="aira_live_xxx"
    export OPENAI_API_KEY="sk-..."
    python proxy.py
"""

from openai import OpenAI
from aira import Aira

aira = Aira()

# Get gateway config — returns the URL and headers to route through Aira
config = aira.gateway_openai_kwargs()

# Create OpenAI client pointing to Aira Gateway instead of OpenAI directly
client = OpenAI(**config)

# This call goes: your code → Aira Gateway → policy check → OpenAI → response → receipt
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of Germany?"},
    ],
)

print(f"Response: {response.choices[0].message.content}")
print(f"Model: {response.model}")

# The gateway automatically:
# 1. Created an action (authorize)
# 2. Evaluated policies
# 3. Forwarded to OpenAI
# 4. Notarized the response (receipt minted)
# 5. Returned the response — same format as direct OpenAI

# Check the action in the dashboard or via API
print(f"\nCheck your dashboard: https://airaproof.com/dashboard/actions")

aira.close()
