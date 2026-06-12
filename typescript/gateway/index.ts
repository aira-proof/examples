/**
 * Aira Gateway — transparent LLM proxy with policy enforcement.
 *
 * Usage:
 *   npm install aira-sdk openai
 *   AIRA_API_KEY="aira_live_..." OPENAI_API_KEY="sk-..." npx tsx index.ts
 */

import { Aira } from "aira-sdk";
import { gatewayOpenAIConfig } from "aira-sdk/gateway";
import OpenAI from "openai";

const aira = new Aira();
const config = gatewayOpenAIConfig({ airaApiKey: process.env.AIRA_API_KEY! });

const client = new OpenAI(config);

const response = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "What is the capital of Germany?" },
  ],
});

console.log("Response:", response.choices[0].message.content);
console.log("\nCheck your dashboard: https://airaproof.com/dashboard/actions");
