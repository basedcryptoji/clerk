"""Example: look up a federal judge + their case history.

Useful when forecasting how a pending case might be decided based on
the presiding judge's prior rulings.

Requires payment ($0.001 USDC via x402, or 1B+ $CLERK held). Send
USDC to Clerk's payment wallet on Base before running this script,
then export the resulting tx hash:

    export CLERK_PAYMENT_TX="0x..."
    python judge_history.py
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

# Search judges by name
judges = client.judges("Alvin Hellerstein", limit=5)

print(f"Found {len(judges)} judges:\n")
for judge in judges:
    name = judge.get("name", "(unknown)")
    court = judge.get("court", "")
    appointed = judge.get("date_appointed", "")
    print(f"  {name}")
    print(f"    {court} · appointed {appointed}")
    if judge.get("bio"):
        print(f"    {judge['bio'][:160]}...")
    print()
