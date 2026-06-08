# Aira Examples

Working examples and benchmarks for the [Aira](https://airaproof.com) AI governance platform.

## Benchmarks

```bash
cd benchmarks
pip install cryptography
python benchmark.py
```

Measures Aira's cryptographic primitives — Ed25519 signing, SHA-256 hashing, policy evaluation, Merkle trees, content scanning, drift detection. No server needed.

| Operation | p50 | Throughput |
|-----------|-----|-----------|
| Full receipt mint (policy + sign) | 95μs | 10,500/sec |
| Policy evaluation (3 rules) | 0.5μs | 2M/sec |
| Content scan (6 patterns) | 5.8μs | 171K/sec |
| Gateway overhead on LLM calls | ~15ms | under 1% |

Full results: [docs.airaproof.com/docs/guides/performance](https://docs.airaproof.com/docs/guides/performance)

## Python Examples

| Example | Description |
|---------|-------------|
| [lending-agent](python/lending-agent) | Authorize → execute → notarize a loan decision |
| [langchain-agent](python/langchain-agent) | LangChain agent with Aira callback handler |
| [mcp-server](python/mcp-server) | MCP server exposing Aira tools |
| [governance-lifecycle](python/governance-lifecycle) | Full lifecycle: register agent → authorize → notarize → verify |
| [offline-sync](python/offline-sync) | Queue actions offline, sync when connected |
| [webhook-server](python/webhook-server) | Receive and verify Aira webhook events |

## TypeScript Examples

| Example | Description |
|---------|-------------|
| [lending-agent](typescript/lending-agent) | Authorize → execute → notarize a loan decision |
| [langchain-agent](typescript/langchain-agent) | LangChain.js agent with Aira callback |
| [mcp-server](typescript/mcp-server) | MCP server exposing Aira tools |
| [vercel-ai](typescript/vercel-ai) | Vercel AI SDK middleware integration |
| [offline-sync](typescript/offline-sync) | Queue actions offline, sync when connected |
| [webhook-server](typescript/webhook-server) | Receive and verify Aira webhook events |

## Quick Start

```bash
pip install aira-sdk
export AIRA_API_KEY=aira_live_...

cd python/lending-agent
python agent.py
```

## Links

- [Documentation](https://docs.airaproof.com)
- [API Reference](https://docs.airaproof.com/docs/api-reference)
- [Interactive API (Swagger)](https://api.airaproof.com/docs)
- [Performance Benchmarks](https://docs.airaproof.com/docs/guides/performance)
- [Python SDK on PyPI](https://pypi.org/project/aira-sdk/)
- [TypeScript SDK on npm](https://www.npmjs.com/package/aira-sdk)
