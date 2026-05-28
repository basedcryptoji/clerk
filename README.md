<p align="center">
  <img src="./assets/clerk-banner.png" alt="Clerk — AI-native legal data layer for the agentic economy" />
</p>

# Clerk

**The AI-native legal data layer for the agentic economy.**

Clerk provides permissionless access to **500M+ US federal court records** across **94 federal courts** through **11 data endpoints**. Built on Base, it eliminates subscriptions and API keys by using **x402 micropayments at just $0.001 per query in USDC**. Stack legal intelligence into any AI agent workflow.

Live at [clerk.solvrlabs.ai](https://clerk.solvrlabs.ai) · Built by [Solvr Labs](https://solvrbot.com) · $CLERK holders get up to 80% off

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

**Max discount:** wallets holding **250M+ $CLERK** on Base get **80% off**
every query — the top tier (not free). The protocol auto-detects $CLERK
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

Pay-per-query via x402 micropayments. Or hold **$CLERK on Base** for tiered discounts: 25% off at 2.5M+, 50% off at 25M+, and **80% off (max) at 250M+**.

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

---

## Links

- Product: [clerk.solvrlabs.ai](https://clerk.solvrlabs.ai)
- API Docs: [clerk.solvrlabs.ai/docs](https://clerk.solvrlabs.ai/docs)
- API Reference (in this repo): [ENDPOINTS.md](./ENDPOINTS.md)
- X: [@agent_clerk](https://x.com/agent_clerk)
- Parent project: [Solvr](https://solvrbot.com) · [@solvrbot](https://x.com/solvrbot)

## Support the project

Hold $CLERK on Base for up to 80% off queries, or trade on DEXScreener.

`0x20EabA9d6818529cfFFA2c1C63B97A02a0049bA3`

[DEXScreener](https://dexscreener.com/base/0x4bacc9d57e57b8361d5d31e83daef1ddae57d2992227a5ae7fefa09c19f2ab19)

---

<p align="center">
  <img src="./assets/clerk-full.png" alt="Clerk — Court Records, On Demand" width="320" />
</p>

<p align="center">
  <em>Clerk — The Permissionless Legal Data Layer for the Agent Economy.</em>
</p>
