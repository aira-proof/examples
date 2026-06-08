# Aira Sanitize — PII Detection & Redaction

Scan text for PII, credentials, and prompt injection. Four modes: redact, tokenize, block, flag.

```bash
pip install aira-sdk
export AIRA_API_KEY="aira_live_..."
python scan.py
```

## What it does

1. **Redact** — replaces PII with `[REDACTED]`
2. **Tokenize** — replaces PII with reversible tokens (`<EMAIL_001>`)
3. **Detokenize** — restores original values from token mapping

## Policies

- `default` — PII, credentials, prompt injection
- `hipaa` — PII + healthcare-specific (PHI, ICD codes)
- `pci` — card numbers, account data
- `legal` — names, emails, PII
