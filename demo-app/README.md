# Aira Interactive Demo

A visual, no-code walkthrough of the Aira platform. Non-technical users can click through the complete flow — register an agent, notarize actions, verify receipts, and seal evidence.

## How to Run

Just open the HTML file in a browser:

```bash
open index.html
```

Or serve it:

```bash
npx serve .
```

## What It Demonstrates

| Step | Feature | What Happens |
|------|---------|-------------|
| 1 | **Register Agent** | Creates a verifiable AI agent identity with capabilities |
| 2 | **Notarize Action** | Notarizes a loan decision — returns Ed25519 signature + receipt |
| 3 | **Chain of Custody** | Links a follow-up email to the original decision |
| 4 | **Public Verification** | Verifies the receipt without authentication — anyone can do this |
| 5 | **Compliance Snapshot** | Records EU AI Act compliance attestation |
| 6 | **Seal Evidence** | Bundles all actions into a tamper-proof evidence package |

## Requirements

- An Aira API key — get one free at https://app.airaproof.com/dashboard/api-keys
- A modern browser (Chrome, Firefox, Safari, Edge)
- No build step, no dependencies, no framework

## Screenshot

Enter your API key at the top, then click through each step. Each step shows the full API response including cryptographic signatures and hashes.
