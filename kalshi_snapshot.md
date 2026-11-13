# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.0)
**Timestamp:** `2026-11-13T18:22:41.205360+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `LIVE_KALSHI_PORTFOLIO_API (Live=$1016.18; SizingFloor=$200.00)`
* **Effective Sizing Bankroll:** `$1016.18`
* **Max Dollar Risk Per Pick (5% Cap):** `$50.81` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$152.43`
* **Dry Powder Reserve (85% Min):** `$863.75`

## 2. Scanner Diagnostics Funnel
* **Open Non-Parlay Markets Scanned:** `9846`
* **In Expiration Window (8h - 168h):** `202`
* **Passed Preliminary Two-Sided Quote Gate:** `36`
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `36`
* **Passed Spread (2c-15c) & Book Depth Gate:** `9`
* **Passed Strike-vs-Oracle Tail Gate:** `3`

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** `SKIP BUCKET` — No contract currently meets two-sided spread (2c-15c), book depth, and oracle tail distance gates.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXWTI-26NOV1614-T90.99`](https://kalshi.com/markets/kxwti-26nov1614) — Will the WTI crude oil settlement price be above 90.99 USD/Bbl on Nov 16, 2026? (Above $90.99)  
  * **Action:** Buy No (Limit) @ **84c** x **60 contracts** (Risk `$50.40` to win `$9.60` / `+19.05%`)  
  * **Book:** Yes Bid `13c` / No Bid `83c` | Spread `4c` | Book Depth `25241` | Expires `73.12h`  
  * **Oracle Proof:** Tail longshot bid at 13c Yes (event consensus peak 97c Yes across 30 market(s)); verified two-sided book.
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** `SKIP BUCKET` — No contract currently meets two-sided spread (2c-15c), book depth, and oracle tail distance gates.

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXWTI-26NOV1614-T90.99](https://kalshi.com/markets/kxwti-26nov1614) | BUCKET_B_MACRO_ENERGY_COMMODITY | 13c | 83c | **84c** | **60** (`$50.40`) | 4c | 25241 | +19.05% | 73.12h |
| 2 | [KXWTI-26NOV1614-T92.49](https://kalshi.com/markets/kxwti-26nov1614) | BUCKET_B_MACRO_ENERGY_COMMODITY | 4c | 92c | **93c** | **54** (`$50.22`) | 4c | 14580 | +7.53% | 73.12h |
