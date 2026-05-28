# Clerk API Endpoints

All endpoints live under `https://clerk.solvrlabs.ai/`.

Authentication: x402 micropayments on Base. Pay $0.001 USDC per query.
Hold **$CLERK** on Base → up to 80% off (max tier at 250M+).

## Discovery

### `GET /`

Root manifest. Returns API metadata + endpoint list + current price.

```json
{
  "name": "Clerk",
  "version": "0.1.0",
  "endpoints": { ... },
  "payment": {
    "method": "x402",
    "currency": "USDC",
    "chain": "Base"
  }
}
```

### `GET /health`

Health check. No payment required. Returns `{"status": "ok"}`.

---

## Search

### `GET /search?q={query}`

Federal case search.

**Query params:**
- `q` (required) — search query (party name, case name, or case number)
- `court` — court code (e.g. `cacd` = Central District of California)
- `date_filed_after` — `YYYY-MM-DD`
- `date_filed_before` — `YYYY-MM-DD`
- `limit` — max results (1-50, default 20)

**Response:**
```json
{
  "results": [
    {
      "case_name": "Shankar (PS) v. Binance",
      "case_number": "1:25-cv-01249",
      "court": "D. Colo.",
      "court_id": "cod",
      "date_filed": "2025-04-18",
      "date_terminated": "2025-06-03",
      "status": "",
      "nature_of_suit": "375 Other Statutes: False Claims Act",
      "source": "clerk"
    }
  ],
  "count": 1,
  "demo": false
}
```

Demo mode: works without payment. Returns up to ~12 results per IP per hour.

---

## Docket detail

### `GET /docket/{docket_id}`

Full docket including parties, attorneys, and timeline.

**Response:**
```json
{
  "docket": {
    "id": 67614382,
    "case_name": "...",
    "court": "...",
    "parties": [{ "name": "...", "role": "plaintiff" }],
    "attorneys": [{ "name": "...", "party": "..." }],
    "date_filed": "...",
    "date_terminated": "..."
  }
}
```

---

## Party search

### `GET /parties?name={name}`

Look up entities (companies, individuals) and their court appearances.

**Query params:**
- `name` (required) — party name
- `limit` — max results (1-50, default 20)

---

## Judges

### `GET /judges?name={name}`

Judicial profile and case history.

**Query params:**
- `name` (required) — judge name

---

## Citations

### `GET /citations?q={query}`

Search opinions and precedents.

**Query params:**
- `q` (required) — citation query
- `court` — filter by court code
- `date_after` / `date_before` — YYYY-MM-DD

---

## Opinion

### `GET /opinion/{opinion_id}`

Full opinion text.

---

## Filings

### `GET /filings/{docket_id}`

Docket entries and timeline.

---

## Oral arguments

### `GET /oral-arguments?q={query}`

Search oral argument transcripts.

---

## Document

### `GET /document/{doc_id}`

Document metadata + download URL.

---

## Court metadata

### `GET /court/{court_id}`

Court info: full name, jurisdiction, citation style.

---

## Delegation

### `POST /api/delegate`

Register a delegate wallet under a main $CLERK wallet. Lets a fresh agent
wallet (funded with only gas) inherit your $CLERK tier privileges.

**Body:**
```json
{
  "main_wallet": "0x...",
  "delegate_wallet": "0x...",
  "signature": "0x...",
  "timestamp": 1700000000
}
```

Signature is an EIP-191 personal_sign of:
```
Register delegate for Clerk: {delegate_wallet.lower()} ts:{timestamp}
```

Valid for 10 minutes. Re-run to refresh.

### `DELETE /api/delegate`

Remove a delegate. Same payload shape as POST.

### `GET /api/delegations?wallet={main_wallet}`

List all delegates for a main wallet.

---

## x402 payment flow

1. Client calls `GET /endpoint`
2. Server returns `402 Payment Required` with challenge JSON
3. Client signs USDC transfer to Clerk's payment wallet (Base)
4. Client retries call with `X-PAYMENT` header containing the signed payment
5. Server validates payment + returns the data

The [`clerk_api` Python SDK](./clerk_api/) handles this automatically.

For top-tier (250M+) $CLERK holders: the server detects your wallet's $CLERK balance and applies the 80% max discount automatically.

---

## Notes

- Federal courts only (94 district + appellate). State courts not covered.
- Sealed dockets are not exposed.
- Surfaces public records. Not legal advice — interpretation requires a licensed attorney.
