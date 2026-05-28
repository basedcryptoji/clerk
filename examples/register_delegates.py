"""Batch-register agent wallets as delegates under a main $CLERK wallet.

The delegated signer pattern lets a single $CLERK-holding wallet authorize
multiple "agent wallets" to access Clerk at the discounted rate (under the
250M+ $CLERK max-discount tier, 80% off) without ever putting the main wallet in production code.
Each agent wallet is funded with only gas; the main wallet stays cold.

Security: this script loads the main wallet's private key from the
CLERK_MAIN_WALLET_KEY environment variable. Never hardcode the key in
source. Use a .env file (gitignored) or a secrets manager for production.

Usage:
    pip install eth-account requests

    export CLERK_MAIN_WALLET_KEY="0x..."   # never commit this

    # Inline list (edit AGENT_WALLETS below):
    python register_delegates.py

    # CSV file (one address per line, header optional):
    python register_delegates.py --csv wallets.csv

    # Remove delegates instead of adding:
    python register_delegates.py --remove
    python register_delegates.py --csv wallets.csv --remove

Signatures include a fresh timestamp and are valid for 10 minutes.
Re-run the script to re-register — do not store signatures.
"""

import argparse
import csv
import os
import time
import requests
from eth_account import Account
from eth_account.messages import encode_defunct

# ── Config ────────────────────────────────────────────────────────────────────

# Load from env, never hardcode.
MAIN_WALLET_PRIVATE_KEY = os.environ.get("CLERK_MAIN_WALLET_KEY", "")

AGENT_WALLETS = [
    "0x...",  # agent 1
    "0x...",  # agent 2
    # add more here, or use --csv
]

API_BASE = "https://clerk.solvrlabs.ai"

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_wallets_from_csv(path: str) -> list[str]:
    wallets = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            val = row[0].strip()
            if val.lower() == "address" or val.lower() == "wallet":
                continue  # skip header
            if val.startswith("0x") and len(val) == 42:
                wallets.append(val)
    return wallets


def sign_delegate(private_key: str, delegate_wallet: str, ts: int) -> tuple[str, str]:
    account = Account.from_key(private_key)
    message = f"Register delegate for Clerk: {delegate_wallet.lower()} ts:{ts}"
    signed = account.sign_message(encode_defunct(text=message))
    return account.address, signed.signature.hex()


# ── Main ──────────────────────────────────────────────────────────────────────

def run(wallets: list[str], remove: bool = False):
    account = Account.from_key(MAIN_WALLET_PRIVATE_KEY)
    main_address = account.address

    action = "Removing" if remove else "Registering"
    print(f"Main wallet : {main_address}")
    print(f"{action}  : {len(wallets)} delegates\n")

    ok, fail = 0, 0
    for wallet in wallets:
        wallet = wallet.strip()
        if not wallet or wallet == "0x...":
            print(f"  SKIP  {wallet}  (placeholder)")
            continue

        ts = int(time.time())
        _, sig = sign_delegate(MAIN_WALLET_PRIVATE_KEY, wallet, ts)

        payload = {
            "main_wallet": main_address,
            "delegate_wallet": wallet,
            "signature": sig,
            "timestamp": ts,
        }

        try:
            if remove:
                resp = requests.delete(f"{API_BASE}/api/delegate", json=payload, timeout=15)
            else:
                resp = requests.post(f"{API_BASE}/api/delegate", json=payload, timeout=15)

            if resp.status_code == 200:
                print(f"  OK    {wallet}")
                ok += 1
            else:
                body = resp.json() if "application/json" in resp.headers.get("content-type", "") else resp.text
                print(f"  FAIL  {wallet}  [{resp.status_code}] {body}")
                fail += 1

        except Exception as e:
            print(f"  ERR   {wallet}  {e}")
            fail += 1

    print(f"\nDone. {ok} {'removed' if remove else 'registered'}, {fail} failed.")
    if ok and not remove:
        print(f"\nVerify: GET {API_BASE}/api/delegations?wallet={main_address}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch-register Clerk delegate wallets")
    parser.add_argument("--csv", metavar="FILE", help="CSV file with one wallet address per line")
    parser.add_argument("--remove", action="store_true", help="Remove delegates instead of adding")
    args = parser.parse_args()

    if not MAIN_WALLET_PRIVATE_KEY:
        print("ERROR: CLERK_MAIN_WALLET_KEY env var is not set.")
        print("       export CLERK_MAIN_WALLET_KEY=\"0x...\"  (your $CLERK holder wallet's private key)")
        print("       Never hardcode the key in source.")
        raise SystemExit(1)

    if args.csv:
        wallets = load_wallets_from_csv(args.csv)
        print(f"Loaded {len(wallets)} wallets from {args.csv}\n")
    else:
        wallets = [w for w in AGENT_WALLETS if w != "0x..."]

    if not wallets:
        print("No wallets to process.")
    else:
        run(wallets, remove=args.remove)
