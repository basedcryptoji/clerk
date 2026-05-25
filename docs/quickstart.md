# Quickstart

A 10-minute walkthrough from zero to your first paid Clerk query, with
the delegated-signer pattern for production agents.

## What Clerk is

Clerk is the AI-native legal data layer for the agentic economy.
Permissionless access to **500M+ US federal court records** across
**94 federal courts** through **11 data endpoints**. Built on Base.
No subscriptions, no API keys, no forms — payment is x402 micropayments
at $0.001 USDC per query.

Hold 1B+ $CLERK on Base to unlock free unlimited queries.

## 1. Install

```bash
pip install clerk-api
```

Need only Python 3.10+ and `httpx`. The `examples/` folder uses
`requests` and `eth-account` — install via `pip install clerk-api[examples]`
if you want to run them.

## 2. Free demo (no payment)

The `/search` endpoint has a demo mode that returns up to ~12 cases
per IP per hour without any payment. Try it:

```python
from clerk_api import ClerkClient

client = ClerkClient()  # no auth — demo
cases = client.search("SEC v Ripple", limit=5)

for c in cases:
    print(f"{c['case_name']} — {c['court']} — {c['date_filed']}")
```

That's it. No wallet, no signup. The same call works in a serverless
function, a notebook, or your agent loop.

## 3. Paid queries (any endpoint)

Endpoints beyond `/search` require x402 payment. The flow is two-step:

**Step A — Send USDC externally.** Use any wallet on Base (MetaMask,
Bankr, a server-side `web3.py` flow, your CDP-Pay setup, etc.) to send
`$0.001 USDC` to Clerk's payment wallet. Capture the resulting
transaction hash. Example with `web3.py`:

```python
import os
from web3 import Web3
from eth_account import Account

USDC_BASE = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"  # USDC on Base
CLERK_PAYMENT_WALLET = "0x8c84608E4b89a67203a16F02e68d3659659CCDed"
AMOUNT = 1000  # 0.001 USDC = 1000 (6 decimals)

w3 = Web3(Web3.HTTPProvider("https://mainnet.base.org"))
account = Account.from_key(os.environ["WALLET_PRIVATE_KEY"])

# Minimal ERC-20 transfer ABI
usdc = w3.eth.contract(address=USDC_BASE, abi=[{
    "constant": False, "inputs":[{"name":"_to","type":"address"},
    {"name":"_value","type":"uint256"}], "name":"transfer",
    "outputs":[{"name":"","type":"bool"}], "type":"function"
}])

tx = usdc.functions.transfer(CLERK_PAYMENT_WALLET, AMOUNT).build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 100_000,
    "gasPrice": w3.eth.gas_price,
})
signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction).hex()
print(f"Payment sent: 0x{tx_hash}")
```

**Step B — Pass the tx hash to Clerk.** The SDK encodes it as an
x402 payment header. Clerk's server validates the payment on-chain and
returns the data.

```python
from clerk_api import ClerkClient

client = ClerkClient(tx_hash="0x...your-payment-tx-hash...")

docket = client.docket("67614382")
parties = client.parties("Binance", limit=10)
judge = client.judges("Hellerstein")[0]
```

Each successful query consumes a fresh payment. For agent workflows
doing many queries, see the **delegated signer** section below — it
amortizes payment across a single $CLERK-holding wallet.

## 4. Free tier via $CLERK

Holding **1B+ $CLERK** on Base unlocks unlimited free queries on every
endpoint. The protocol auto-detects $CLERK balance from the payment
context and skips the per-call payment.

Token contract: `0x20EabA9d6818529cfFFA2c1C63B97A02a0049bA3` (Base)
[DEXScreener](https://dexscreener.com/base/0x4bacc9d57e57b8361d5d31e83daef1ddae57d2992227a5ae7fefa09c19f2ab19)

## 5. Delegated signer pattern (recommended for production)

**Never put your main $CLERK-holding wallet in a production agent.**

Instead, delegate signing authority to a fresh "agent wallet" funded
only with enough ETH for gas. The agent wallet does the day-to-day
signing in code; your main wallet stays cold.

Register one or more delegate wallets:

```bash
export CLERK_MAIN_WALLET_KEY="0x..."  # your 1B+ $CLERK wallet's key
python examples/register_delegates.py --csv my_agents.csv
```

Once registered, the delegate wallet inherits your $CLERK tier
benefits when it signs Clerk payments. Your main wallet is never
exposed to the runtime.

See [`examples/register_delegates.py`](../examples/register_delegates.py)
for the full registration script.

## 6. Composing with other intel

Clerk is one layer in the Solvr stack:

- [`solvrbot.com/intels/clerk-search`](https://solvrbot.com/intels) —
  agent recipe that composes Clerk litigation data with on-chain intel
  for crypto compliance / risk analysis
- Pair Clerk with `solvr_intel(ca)` to cross-reference a token's deployer
  with court cases against the same entity
- Pair Clerk with `solvr_security_scan` — every flag pattern becomes a
  Clerk search target

## 7. Error handling

The SDK raises three exception types:

```python
from clerk_api import ClerkClient, ClerkError, PaymentRequired

try:
    cases = client.search("Binance")
except PaymentRequired as e:
    # 402 — payment header missing or invalid
    print("Need to pay or top up:", e)
except ClerkError as e:
    # Other 4xx / 5xx
    print(f"API error {e.status_code}: {e}")
```

`PaymentRequired` subclasses `ClerkError`, so catching `ClerkError`
alone is sufficient if you don't need to distinguish.

## 8. Limits

- Federal courts only (94 districts + appellate). State courts not covered.
- Sealed dockets are not exposed.
- Surfaces public records only. Not legal advice — interpretation
  requires a licensed attorney.

## Next steps

- Run [`examples/search_cases.py`](../examples/search_cases.py) for a
  zero-config demo
- Read [`ENDPOINTS.md`](../ENDPOINTS.md) for the full API surface
- File issues at [github.com/basedcryptoji/clerk/issues](https://github.com/basedcryptoji/clerk/issues)
