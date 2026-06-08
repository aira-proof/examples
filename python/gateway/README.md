# Aira Gateway — Transparent LLM Proxy

Route LLM calls through Aira for policy enforcement and cryptographic receipts. ~15ms overhead.

```bash
pip install aira-sdk openai
export AIRA_API_KEY="aira_live_..."
export OPENAI_API_KEY="sk-..."
python proxy.py
```

## How it works

1. Your code creates an OpenAI client with `aira.gateway_openai_kwargs()`
2. Calls go to Aira Gateway instead of OpenAI directly
3. Gateway authorizes the call, evaluates policies
4. Forwards to the upstream LLM provider
5. Notarizes the response — receipt minted
6. Returns the response in the same format as direct OpenAI

## Supported providers

- OpenAI (via `gateway_openai_kwargs()`)
- Anthropic (via `gateway_anthropic_kwargs()`)
