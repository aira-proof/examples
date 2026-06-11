# Approval Flow — Human-in-the-Loop Agent

A complete example showing how an agent handles the approval flow:

1. Agent requests authorization for a wire transfer
2. Policy requires human approval → agent waits
3. Human approves via email, Slack, or dashboard
4. Agent detects approval (polling), executes the transfer
5. Agent notarizes the outcome with a cryptographic receipt

## Key concepts

- **`authorize()` is the only call that triggers policy evaluation.** Called once per action.
- **`get_action()` is a read operation.** No policy evaluation, no risk of infinite loops.
- **The agent never executes before approval.** It polls until approved, denied, or timed out.

## Run

```bash
pip install aira-sdk
export AIRA_API_KEY="aira_live_..."
python agent.py
```

## What happens

```
1. Requesting authorization...
   Status: pending_approval
   Action UUID: abc-123...

2. Pending human approval
   Approvers notified via email and/or Slack.
   Waiting for approval (polling every 5s, max 300s)...

   ⏳ Still waiting... (15s elapsed)
   ✅ Approved! (waited 23s)
   Approved by: admin@company.com

3. Executing transfer (approved)...
   💸 Executing transfer: $50,000.00 to Acme Corp

4. Notarizing outcome...
   Receipt: rec-xyz...

5. Verifying receipt (public)...
   Valid: True
```

## Flow diagram

```
Agent                     Aira                      Human
  |                         |                         |
  |-- authorize() --------->|                         |
  |                         |-- evaluate policies --->|
  |                         |                         |
  |<-- pending_approval ----|                         |
  |                         |-- email/Slack --------->|
  |                         |                         |
  |-- get_action() -------->|                     [reviews]
  |<-- pending_approval ----|                         |
  |                         |                         |
  |-- get_action() -------->|<------ approve ---------|
  |<-- approved ------------|                         |
  |                         |                         |
  |-- [execute transfer] -->|                         |
  |                         |                         |
  |-- notarize() ---------->|                         |
  |<-- receipt -------------|                         |
```
