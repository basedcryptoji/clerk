# Clerk

**US federal court records. Permissionless. Pay-per-query.**

500M+ cases · $0.001 USDC per query via x402 on Base · 1B+ $CLERK = free unlimited

Live at [clerk.solvrlabs.ai](https://clerk.solvrlabs.ai) · Built by [Solvr Labs](https://solvrbot.com)

---

## What is Clerk?

Clerk is an x402-paid API that exposes US federal court records to AI agents.
No API keys to manage. No subscriptions. No forms. Agents call the endpoint,
the 402 response triggers a USDC payment, the call retries automatically,
and the agent receives JSON.

> The agent calls. The 402 fires. The agent pays. The data returns. No keys, no forms, no humans in the loop.

## Install

```bash
pip install clerk-api
```

Requires Python 3.10+. One dependency: `httpx` (or `requests` as a fallback).

## Quick start

`/search` works in demo mode without payment — perfect for trying the SDK first:

```python
from clerk_api import ClerkClient

client = ClerkClient()  # no auth — demo mode

cases = client.search("SEC v Ripple")
for case in cases:
    print(f"{case['case_name']} — {case['court']} — {case['date_filed']}")
```

For full access on paid endpoints, you send USDC externally first (any
wallet on Base — MetaMask, Bankr, web3.py, etc.) to Clerk's payment
wallet, then pass the resulting transaction hash to the client:

```python
import os
from clerk_api import ClerkClient

# 1. Send $0.001 USDC to the Clerk payment wallet on Base (you do this
#    out-of-band using any web3 client). Capture the resulting tx hash.
# 2. Pass the tx_hash to the SDK. The client encodes it as an x402
#    payment header that the server validates against the on-chain tx.
client = ClerkClient(tx_hash=os.environ["CLERK_PAYMENT_TX"])

docket = client.docket("67614382")
print(docket)
```

**Free unlimited access:** wallets holding **1B+ $CLERK** on Base
bypass per-call payment entirely. The protocol auto-detects $CLERK
balance from the payment context.

## Endpoints

| Endpoint | What | Price |
|---|---|---|
| `GET /search?q=...` | Federal case search | $0.001 USDC |
| `GET /docket/{id}` | Full docket details | $0.001 |
| `GET /parties?name=...` | Entity lookup | $0.001 |
| `GET /judges?name=...` | Judicial profile | $0.001 |
| `GET /citations?q=...` | Opinions / precedents | $0.001 |
| `GET /opinion/{id}` | Full opinion text | $0.001 |
| `GET /filings/{docket_id}` | Docket timeline | $0.001 |
| `GET /oral-arguments?q=...` | Oral argument transcripts | $0.001 |
| `GET /document/{doc_id}` | Document + download URL | $0.001 |
| `GET /court/{court_id}` | Court metadata | $0.001 |
| `GET /health` | Health check | free |

Full API reference: [`ENDPOINTS.md`](./ENDPOINTS.md)

## $CLERK token

Pay-per-query via x402 micropayments. Or hold **1B+ $CLERK on Base** to unlock unlimited free queries on every endpoint.

The protocol auto-detects $CLERK balance from your signing wallet on each request.

## Delegated signer pattern (production)

For agent ops at scale, never put your main $CLERK-holding wallet in a script.
Instead, delegate signing to a fresh wallet funded only with gas.

```bash
python examples/register_delegates.py --csv my_agents.csv
```

Your main wallet stays cold; agent wallets do all the signing. See
[`examples/register_delegates.py`](./examples/register_delegates.py).

## Demo mode

`/search` works without payment in demo mode (limited results per IP per hour).
Use it to test the integration before wiring up x402.

```python
client = ClerkClient()  # no key — demo mode
results = client.search("Binance", limit=5)
```

## Limits

- Federal courts only (94 district courts + appellate). State courts not covered.
- Sealed dockets are not exposed.
- Surfaces public records only. Not legal advice — interpretation requires a licensed attorney.

## License

MIT
