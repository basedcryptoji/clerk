# Changelog

All notable changes to `clerk-api` will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-05-23

Metadata polish — no API or code changes. Existing 0.1.0 installs unaffected.

### Changed
- Package summary now reads "AI-native legal data layer for the agentic economy. 500M+ US federal court records via x402 on Base." (was: generic "Python SDK for Clerk")
- Added structured `project_urls`: `Source` (GitHub), `Documentation` (clerk.solvrlabs.ai/docs), `Issues` (GitHub)
- Added `author_email`: `hello@solvrbot.com`

## [0.1.0] - 2026-05-20

Initial public release.

### Added
- `ClerkClient` — Python client for the Clerk API at `clerk.solvrlabs.ai`
- x402 payment header support via `tx_hash` or pre-encoded `payment_header`
  constructor args; works in demo mode for `/search` without payment
- Endpoint coverage:
  - `search(query, court, date_after, date_before, limit, source)` — case search
  - `docket(docket_id)` — full docket details
  - `parties(name, limit)` — entity lookup
  - `judges(name)` — judicial profile
  - `citations(query, court, date_after, date_before)` — opinion search
  - `opinion(opinion_id)` — full opinion text
  - `filings(docket_id)` — docket timeline
  - `oral_arguments(query)` — oral argument transcripts
  - `document(doc_id)` — court document download URL
  - `court(court_id)` — court metadata
- `examples/`:
  - `search_cases.py` — demo-mode case search
  - `party_lookup.py` — paid entity lookup
  - `judge_history.py` — paid judge profile
  - `register_delegates.py` — batch delegated-signer registration
- `ENDPOINTS.md` — full API reference matching `clerk.solvrlabs.ai/`
- `CONTRIBUTING.md` — PR + issue guidance
- `docs/quickstart.md` — fuller getting-started walkthrough
- Brand assets under `assets/`

### Security
- All examples load wallet private keys from environment variables. The
  `register_delegates.py` script enforces this with an early-exit if
  `CLERK_MAIN_WALLET_KEY` is unset.
- Delegated signer pattern documented end-to-end as the recommended
  production approach.

[0.1.0]: https://github.com/basedcryptoji/clerk/releases/tag/v0.1.0
