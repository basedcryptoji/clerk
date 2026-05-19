"""Example: look up an entity (company or person) across federal courts.

Useful for compliance + risk research: "has this issuer been sued?"

Requires payment ($0.001 USDC via x402, or 1B+ $CLERK held). Send
USDC to Clerk's payment wallet on Base before running this script,
then export the resulting tx hash:

    export CLERK_PAYMENT_TX="0x..."
    python party_lookup.py
"""
import os
from clerk_api import ClerkClient

tx_hash = os.environ.get("CLERK_PAYMENT_TX")
if not tx_hash:
    raise SystemExit(
        "CLERK_PAYMENT_TX env var is not set.\n"
        "Send $0.001 USDC to Clerk's payment wallet on Base first, then "
        "export CLERK_PAYMENT_TX=\"0x...\" with the resulting tx hash.\n"
        "See README for the full x402 payment flow."
    )

client = ClerkClient(tx_hash=tx_hash)

# Look up an entity by name
parties = client.parties("Coinbase", limit=10)

print(f"Found {len(parties)} parties:\n")
for party in parties:
    name = party.get("name", "(unknown)")
    case_count = party.get("case_count", "?")
    role = party.get("role", "")
    print(f"  {name} — {case_count} cases · {role}")
