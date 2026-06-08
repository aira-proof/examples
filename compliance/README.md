# Compliance Examples

Two related concepts, two different artifacts. Most teams produce both.

| Artifact | What it is | Format | Who reads it |
|---|---|---|---|
| **Compliance Bundle** | Cryptographic snapshot of every receipt in a period | JSON (Merkle-rooted, signed, self-contained) | Auditors, machines |
| **Compliance Report** | Same data, rendered as a document | PDF (signed, framework-mapped) | Regulators, board members, humans |

The examples in this directory:

- `generate_article12_report.py` — Python: generate, download, verify a
  Compliance Report PDF for the last 30 days.
- `generate-article12-report.ts` — TypeScript: same flow.

Compliance Bundles have their own SDK methods
(`client.create_compliance_bundle` / `aira.createComplianceBundle`) and
their own examples in `examples/`. See
[the docs](https://docs.airaproof.com/docs/guides/sub-products) for the
full taxonomy of Aira's five sub-products and when to reach for which.
