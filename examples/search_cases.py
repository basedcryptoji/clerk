"""Example: search federal court cases by query string.

`/search` works in demo mode without payment — perfect for trying the
SDK before wiring up x402 payments. Demo mode returns up to ~12 results
per IP per hour.

For higher volumes, pre-pay $0.001 USDC per call (any wallet on Base)
and pass the resulting tx hash via `tx_hash=...`. See the README for
the full payment flow.
"""
from clerk_api import ClerkClient

# Demo mode — no payment required for /search.
client = ClerkClient()

# Search for cases involving a specific entity
cases = client.search("Binance", limit=10)

print(f"Found {len(cases)} cases:\n")
for case in cases:
    print(f"  {case['case_name']}")
    print(f"    {case['case_number']} · {case['court']} · filed {case['date_filed']}")
    if case.get("nature_of_suit"):
        print(f"    {case['nature_of_suit']}")
    print()
