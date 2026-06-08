/**
 * Generate an EU AI Act Article 12 technical file for the last 30 days.
 *
 * Run:
 *   npm install aira-sdk
 *   AIRA_API_KEY=aira_live_... npx tsx generate-article12-report.ts
 */

import { writeFileSync } from "node:fs";
import { Aira } from "aira-sdk";

async function main(): Promise<void> {
  const apiKey = process.env.AIRA_API_KEY;
  if (!apiKey) {
    console.error("AIRA_API_KEY env var is required");
    process.exit(1);
  }

  const aira = new Aira({
    apiKey,
    baseUrl: process.env.AIRA_BASE_URL ?? "https://api.airaproof.com",
  });

  const end = new Date();
  const start = new Date(end.getTime() - 30 * 24 * 3600 * 1000);

  console.log(`Requesting Article 12 report for ${start.toISOString()} -- ${end.toISOString()}`);
  const report = await aira.createComplianceReport({
    framework: "eu_ai_act_art12",
    periodStart: start.toISOString(),
    periodEnd: end.toISOString(),
  });

  console.log("  status:", report.status);
  console.log("  receipts covered:", report.receipt_count);
  console.log("  pdf size:", report.pdf_size_bytes, "bytes");
  console.log("  content_hash:", report.content_hash);
  console.log("  signature:", report.signature);

  const pdf = await aira.downloadComplianceReport(report.id);
  const out = `aira-art12-${report.id}.pdf`;
  writeFileSync(out, pdf);
  console.log("  saved to:", out);

  const verification = await aira.verifyComplianceReport(report.id);
  console.log("  signature valid:", verification.valid);
  console.log("  checks:", verification.checks);
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
