"""
Aira Approval Flow — Complete agent example with human-in-the-loop.

Demonstrates:
1. Agent requests authorization for a high-risk action
2. Policy requires human approval → agent waits (polls)
3. Human approves via email/Slack/dashboard
4. Agent detects approval, executes the action
5. Agent notarizes the outcome with a cryptographic receipt

This is how a production agent handles the approval flow.
No infinite loops — authorize() is called once, then the agent polls
get_action() which is a read operation (no policy evaluation).

Usage:
    pip install aira-sdk
    export AIRA_API_KEY="aira_live_xxx"
    python agent.py
"""

import json
import os
import sys
import time

from aira import Aira, AiraError

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

AIRA_API_KEY = os.environ.get("AIRA_API_KEY")
AIRA_BASE_URL = os.environ.get("AIRA_BASE_URL", "https://api.airaproof.com")
AGENT_SLUG = "payment-agent"
POLL_INTERVAL = 5  # seconds between status checks
MAX_WAIT = 300  # 5 minutes max wait

if not AIRA_API_KEY:
    print("Error: Set AIRA_API_KEY environment variable")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Simulated business logic
# ---------------------------------------------------------------------------

def execute_transfer(recipient: str, amount: float) -> dict:
    """Simulate a wire transfer. In production, this calls your bank API."""
    print(f"   💸 Executing transfer: ${amount:,.2f} to {recipient}")
    return {
        "transfer_id": "TXN-2026-00847",
        "recipient": recipient,
        "amount": amount,
        "currency": "USD",
        "status": "completed",
    }


# ---------------------------------------------------------------------------
# Main agent flow
# ---------------------------------------------------------------------------

def main():
    print("\n" + "=" * 60)
    print("  Aira Approval Flow — Human-in-the-Loop Agent")
    print("=" * 60 + "\n")

    aira = Aira(api_key=AIRA_API_KEY, base_url=AIRA_BASE_URL)

    # The action we want to perform
    transfer = {
        "recipient": "Acme Corp",
        "recipient_account": "DE89 3704 0044 0532 0130 00",
        "amount": 50_000.00,
        "currency": "USD",
        "reason": "Q2 vendor payment — invoice INV-2026-0847",
        "risk_level": "high",
    }

    # ──────────────────────────────────────────────────────────
    # Step 1: Request authorization
    # ──────────────────────────────────────────────────────────
    # This is the ONLY call that triggers policy evaluation.
    # Everything after this is either polling (read) or notarizing.

    print("1. Requesting authorization...")
    print(f"   Action: wire_transfer")
    print(f"   Amount: ${transfer['amount']:,.2f} to {transfer['recipient']}")
    print()

    try:
        auth = aira.authorize(
            action_type="wire_transfer",
            details=json.dumps(transfer, indent=2),
            agent_id=AGENT_SLUG,
            # require_approval=True,  # Force approval (or let policy decide)
        )
    except AiraError as e:
        if e.code == "POLICY_DENIED":
            print(f"   ❌ Policy denied: {e.message}")
            print(f"   The action was blocked by policy. No transfer executed.")
            aira.close()
            return
        raise

    action_uuid = auth.action_uuid
    print(f"   Status: {auth.status}")
    print(f"   Action UUID: {action_uuid}")
    print()

    # ──────────────────────────────────────────────────────────
    # Step 2: Handle the response
    # ──────────────────────────────────────────────────────────

    if auth.status == "authorized":
        # No approval needed — execute immediately
        print("2. Authorized — no approval needed")
        result = execute_transfer(transfer["recipient"], transfer["amount"])

    elif auth.status == "pending_approval":
        # Human approval required — wait for it
        print("2. Pending human approval")
        print(f"   Approvers have been notified via email and/or Slack.")
        print(f"   Waiting for approval (polling every {POLL_INTERVAL}s, max {MAX_WAIT}s)...")
        print()

        # ──────────────────────────────────────────────────────
        # Step 3: Poll for approval
        # ──────────────────────────────────────────────────────
        # get_action() is a READ operation — it does NOT trigger
        # policy evaluation. No infinite loop risk.

        start = time.time()
        while time.time() - start < MAX_WAIT:
            action = aira.get_action(action_uuid)
            status = action.status

            if status == "approved":
                print(f"   ✅ Approved! (waited {int(time.time() - start)}s)")
                if action.authorizations:
                    approver = action.authorizations[0]
                    print(f"   Approved by: {approver.authorizer_email}")
                print()
                break

            elif status == "denied_by_human":
                print(f"   ❌ Denied by human reviewer.")
                print(f"   No transfer executed. Exiting.")
                aira.close()
                return

            elif status == "pending_approval":
                elapsed = int(time.time() - start)
                print(f"   ⏳ Still waiting... ({elapsed}s elapsed)", end="\r")
                time.sleep(POLL_INTERVAL)

            else:
                print(f"   ⚠️  Unexpected status: {status}")
                aira.close()
                return
        else:
            print(f"\n   ⏰ Timed out after {MAX_WAIT}s. No approval received.")
            print(f"   The action is still pending — approve from the dashboard.")
            aira.close()
            return

        # ──────────────────────────────────────────────────────
        # Step 4: Execute the action (only after approval)
        # ──────────────────────────────────────────────────────

        print("3. Executing transfer (approved)...")
        result = execute_transfer(transfer["recipient"], transfer["amount"])

    else:
        print(f"   Unknown status: {auth.status}")
        aira.close()
        return

    # ──────────────────────────────────────────────────────────
    # Step 5: Notarize the outcome
    # ──────────────────────────────────────────────────────────
    # This mints a cryptographic receipt — Ed25519 signature,
    # RFC 3161 timestamp, tamper-evident.

    print()
    print("4. Notarizing outcome...")
    receipt = aira.notarize(
        action_uuid=action_uuid,
        outcome="completed",
        outcome_details=json.dumps(result),
    )
    print(f"   Receipt: {receipt.receipt_uuid}")
    print(f"   Signature: {receipt.signature[:40]}...")
    print()

    # ──────────────────────────────────────────────────────────
    # Step 6: Verify the receipt (public, no auth needed)
    # ──────────────────────────────────────────────────────────

    print("5. Verifying receipt (public)...")
    verification = aira.verify_action(action_uuid)
    print(f"   Valid: {verification.valid}")
    print(f"   Message: {verification.message}")
    print()

    print("=" * 60)
    print(f"  Transfer complete. Receipt: {receipt.receipt_uuid}")
    print(f"  Verify: curl {AIRA_BASE_URL}/api/v1/verify/action/{action_uuid}")
    print("=" * 60 + "\n")

    aira.close()


if __name__ == "__main__":
    main()
