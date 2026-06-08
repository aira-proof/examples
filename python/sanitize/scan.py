"""Aira Sanitize — scan text for PII, credentials, and prompt injection.

Usage:
    pip install aira-sdk
    export AIRA_API_KEY="aira_live_xxx"
    python scan.py
"""

from aira import Aira

aira = Aira()

# Redact PII from text
result = aira.sanitize_text(
    content="Customer John Smith (SSN: 123-45-6789) called about loan #4521. "
            "His email is john.smith@example.com and card is 4532-1234-5678-9010.",
    policy="default",
    mode="redact",
)

print("Original → Clean:")
print(f"  {result['clean']}")
print(f"  Findings: {len(result['findings'])}")
for f in result["findings"]:
    print(f"    - {f['entity_type']}: {f['severity']} ({f['count']} match)")

# Tokenize (reversible)
result = aira.sanitize_text(
    content="Patient Jane Doe, DOB 1985-03-15, diagnosed with type 2 diabetes.",
    policy="hipaa",
    mode="tokenize",
)

print("\nTokenized:")
print(f"  {result['clean']}")
print(f"  Mapping: {result.get('token_mapping', {})}")

# Reverse tokenization
if result.get("token_mapping"):
    original = aira.detokenize(
        content=result["clean"],
        token_mapping=result["token_mapping"],
    )
    print(f"  Restored: {original['content']}")

aira.close()
