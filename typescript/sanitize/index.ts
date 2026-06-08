/**
 * Aira Sanitize — scan text for PII, credentials, and prompt injection.
 *
 * Usage:
 *   npm install aira-sdk
 *   AIRA_API_KEY="aira_live_..." npx tsx index.ts
 */

import { Aira } from "aira-sdk";

const aira = new Aira();

// Redact PII
const result = await aira.sanitizeText({
  content:
    "Customer John Smith (SSN: 123-45-6789) called about loan #4521. " +
    "Email: john.smith@example.com, card: 4532-1234-5678-9010.",
  policy: "default",
  mode: "redact",
});

console.log("Redacted:", result.clean);
console.log("Findings:", result.findings.length);

// Tokenize (reversible)
const tokenized = await aira.sanitizeText({
  content: "Patient Jane Doe, DOB 1985-03-15, diagnosed with type 2 diabetes.",
  policy: "hipaa",
  mode: "tokenize",
});

console.log("\nTokenized:", tokenized.clean);

// Restore
if (tokenized.tokenMapping) {
  const restored = await aira.detokenize({
    content: tokenized.clean,
    tokenMapping: tokenized.tokenMapping,
  });
  console.log("Restored:", restored.content);
}
