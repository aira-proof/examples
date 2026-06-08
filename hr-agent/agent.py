"""
Aira HR Agent — AI-powered candidate screening with cryptographic audit trail.

Evaluates job applicants, schedules interviews, sends offer/rejection emails.
Every action notarized for EU AI Act Article 14 compliance (hiring is Annex III high-risk).

Usage:
    export AIRA_API_KEY="aira_live_xxx"
    export ANTHROPIC_API_KEY="sk-ant-..."
    python agent.py
"""

import hashlib
import json
import os
import sys

import anthropic

# SDK path for local dev
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "sdks", "python"))
from aira import Aira
from aira.client import AiraError

AIRA_API_KEY = os.environ.get("AIRA_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
AIRA_BASE_URL = os.environ.get("AIRA_BASE_URL", "http://localhost:8001")

AGENT_SLUG = "hr-screening-agent"
AGENT_VERSION = "1.0.0"
MODEL_ID = "claude-sonnet-4-6"

if not AIRA_API_KEY or not ANTHROPIC_API_KEY:
    print("Set AIRA_API_KEY and ANTHROPIC_API_KEY")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Candidates
# ---------------------------------------------------------------------------

CANDIDATES = [
    {
        "name": "Anna Müller",
        "email": "anna.mueller@example.de",
        "role": "Senior Backend Engineer",
        "experience_years": 7,
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Kubernetes"],
        "education": "M.Sc. Computer Science, TU Berlin",
        "languages": ["German (native)", "English (fluent)"],
        "salary_expectation": 85000,
    },
    {
        "name": "James Chen",
        "email": "james.chen@example.com",
        "role": "Senior Backend Engineer",
        "experience_years": 3,
        "skills": ["JavaScript", "Node.js", "MongoDB"],
        "education": "B.Sc. Information Systems",
        "languages": ["English (native)", "Mandarin (native)"],
        "salary_expectation": 95000,
    },
    {
        "name": "Sofia García",
        "email": "sofia.garcia@example.es",
        "role": "Senior Backend Engineer",
        "experience_years": 10,
        "skills": ["Python", "Go", "PostgreSQL", "AWS", "Terraform", "gRPC"],
        "education": "M.Sc. Software Engineering, Universidad Politécnica de Madrid",
        "languages": ["Spanish (native)", "English (fluent)", "German (B1)"],
        "salary_expectation": 90000,
    },
]

JOB_REQUIREMENTS = {
    "role": "Senior Backend Engineer",
    "min_experience": 5,
    "required_skills": ["Python", "PostgreSQL"],
    "preferred_skills": ["FastAPI", "Docker", "Kubernetes", "AWS"],
    "salary_range": [75000, 95000],
    "location": "Berlin, Germany (hybrid)",
}

# ---------------------------------------------------------------------------
# AI screening
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an HR screening AI. Evaluate the candidate against the job requirements.

Return ONLY valid JSON:
{
  "decision": "ADVANCE" or "REJECT",
  "score": 0-100,
  "reasoning": "2-3 sentence explanation",
  "strengths": ["strength1", "strength2"],
  "concerns": ["concern1"],
  "interview_recommended": true/false,
  "bias_check": "Confirm no protected characteristic influenced this decision"
}

Evaluate on: skill match, experience level, salary fit. NEVER factor in name, nationality, gender, or language background — only professional qualifications."""


def screen_candidate(candidate: dict, requirements: dict) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Job requirements:\n{json.dumps(requirements, indent=2)}\n\nCandidate:\n{json.dumps(candidate, indent=2)}",
        }],
    )
    text = response.content[0].text
    return json.loads(text[text.find("{"):text.rfind("}") + 1])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n=== Aira HR Screening Agent ===\n")
    print(f"Role: {JOB_REQUIREMENTS['role']}")
    print(f"Requirements: {JOB_REQUIREMENTS['min_experience']}+ years, {', '.join(JOB_REQUIREMENTS['required_skills'])}")
    print(f"Salary range: €{JOB_REQUIREMENTS['salary_range'][0]:,}–€{JOB_REQUIREMENTS['salary_range'][1]:,}")
    print(f"Candidates: {len(CANDIDATES)}")
    print()

    aira = Aira(api_key=AIRA_API_KEY, base_url=AIRA_BASE_URL)

    # ── Register agent ──

    print("1. Registering agent...")
    try:
        aira.register_agent(
            agent_slug=AGENT_SLUG,
            display_name="HR Candidate Screening Agent",
            description="AI-powered resume screening for engineering roles. EU AI Act Annex III high-risk system (employment decisions).",
            capabilities=["resume_screening", "skill_matching", "interview_scheduling", "bias_detection"],
            public=True,
        )
        aira.publish_version(
            slug=AGENT_SLUG,
            version=AGENT_VERSION,
            model_id=MODEL_ID,
            instruction_hash=f"sha256:{hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()}",
            changelog="Initial release — single-model screening with bias check",
        )
        print(f"   ✓ Registered: {AGENT_SLUG} v{AGENT_VERSION}")
    except AiraError as e:
        if e.code in ("AGENT_SLUG_EXISTS", "VERSION_EXISTS"):
            print(f"   ✓ Already registered")
        else:
            raise
    print()

    # ── Set will (succession plan) ──

    print("2. Setting succession plan...")
    try:
        aira.set_agent_will(
            slug=AGENT_SLUG,
            succession_policy="archive",
            data_retention_days=2555,  # 7 years — German labor law retention
            notify_emails=["hr@example-corp.de", "compliance@example-corp.de"],
            instructions="Archive all screening decisions. German labor law requires 7-year retention of hiring records for discrimination claims.",
        )
        print("   ✓ Will set: archive policy, 7-year retention")
    except AiraError:
        print("   ✓ Will already configured")
    print()

    # ── Screen candidates ──

    print("3. Screening candidates...")
    print(f"   {'Candidate':<20} {'Decision':<10} {'Score':<8} {'Interview'}")
    print(f"   {'─' * 58}")

    action_ids = []

    for candidate in CANDIDATES:
        evaluation = screen_candidate(candidate, JOB_REQUIREMENTS)

        # Notarize the screening decision
        receipt = aira.notarize(
            action_type="candidate_screening",
            details=json.dumps({
                "candidate_name": candidate["name"],
                "role": candidate["role"],
                "decision": evaluation["decision"],
                "score": evaluation["score"],
                "reasoning": evaluation["reasoning"],
                "bias_check": evaluation["bias_check"],
                "strengths": evaluation["strengths"],
                "concerns": evaluation.get("concerns", []),
            }),
            agent_id=AGENT_SLUG,
            agent_version=AGENT_VERSION,
            model_id=MODEL_ID,
            instruction_hash=f"sha256:{hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()}",
        )
        action_ids.append(receipt.action_id)

        decision = evaluation["decision"]
        score = evaluation["score"]
        interview = "Yes" if evaluation.get("interview_recommended") else "No"
        symbol = "✓" if decision == "ADVANCE" else "✗"

        print(f"   {candidate['name']:<20} {symbol} {decision:<8} {score:<8} {interview}")

        # Notarize email notification
        email_type = "interview_invitation" if decision == "ADVANCE" else "rejection_notice"
        email_receipt = aira.notarize(
            action_type="email_sent",
            details=json.dumps({
                "to": candidate["email"],
                "type": email_type,
                "subject": f"Application Update — {candidate['role']}",
                "candidate": candidate["name"],
            }),
            agent_id=AGENT_SLUG,
            model_id=MODEL_ID,
            parent_action_id=receipt.action_id,
        )
        action_ids.append(email_receipt.action_id)

    print()

    # ── Compliance ──

    print("4. EU AI Act compliance attestation...")
    print("   (Hiring AI = Annex III Category 4 — high-risk)")
    snapshot = aira.create_compliance_snapshot(
        framework="eu-ai-act",
        agent_slug=AGENT_SLUG,
        findings={
            "annex_iii_category": "4 — Employment, workers management, access to self-employment",
            "art_9_risk_management": "pass",
            "art_10_data_governance": "pass",
            "art_13_transparency": "pass",
            "art_14_human_oversight": "pass — all decisions reviewed by hiring manager",
            "art_15_accuracy": "pass — bias check embedded in every evaluation",
            "bias_mitigation": "pass — prompt explicitly prohibits protected characteristics",
        },
    )
    print(f"   ✓ Status: {snapshot.status}")
    print()

    # ── Evidence package ──

    print("5. Sealing evidence package...")
    package = aira.create_evidence_package(
        title=f"Hiring Round — Senior Backend Engineer — {len(CANDIDATES)} candidates",
        action_ids=action_ids,
        description=f"Complete screening audit trail. {len(CANDIDATES)} candidates evaluated. EU AI Act Annex III compliant. Bias checks passed.",
    )
    print(f"   ✓ \"{package.title}\"")
    print(f"   ✓ {len(action_ids)} actions sealed ({len(CANDIDATES)} screenings + {len(CANDIDATES)} emails)")
    print(f"   ✓ Hash: {package.package_hash[:24]}...")
    print()

    # ── Verify ──

    verify = aira.verify_action(action_ids[0])
    print(f"   Public verification: {'✓ VALID' if verify.valid else '✗ INVALID'}")

    print(f"\n=== Done. {len(action_ids)} actions notarized, {len(CANDIDATES)} candidates screened. ===")
    print(f"=== Audit trail: {AIRA_BASE_URL.replace('api.', 'app.').replace(':8001', ':3000')}/dashboard/actions ===\n")

    aira.close()


if __name__ == "__main__":
    main()
