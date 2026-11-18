# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-18T07:18:27.734071+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `DEFAULT_SIZING_FLOOR ($200.00)`
* **Effective Sizing Bankroll:** `$200.00`
* **Max Dollar Risk Per Pick (5% Cap):** `$10.00` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$30.00`
* **Dry Powder Reserve (85% Min):** `$170.00`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `9403`
* **In Expiration Window (8h - 168h):** `1834` (Bucket A: `66`, Bucket B: `81`, Bucket C: `1687`)
* **Passed Preliminary Two-Sided Quote Gate:** `207` (A: `12`, B: `15`, C: `180`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `207`
* **Passed Bucket Spread & Depth Gate:** `74` (A: `3`, B: `5`, C: `66`)
* **Passed Strike-vs-Oracle Tail Gate:** `72` (A: `1`, B: `5`, C: `66`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXLOWTCHI-26NOV18-B37.5`](https://kalshi.com/markets/kxlowtchi-26nov18) — Will the minimum temperature be 37-38° on Nov 18, 2026? (37° to 38°)  
  * **Action:** Buy No (Limit) @ **89c** x **11 contracts** (Risk `$9.79` to win `$1.21` / `+12.36%`)  
  * **Book:** Yes Bid `4c` / No Bid `88c` | Spread `8c` | Book Depth `2865` | Expires `36.69h`  
  * **Oracle Proof:** NWS KMDW forecast low (2026-11-18) is 41.0F; bracket 37.0F-38.0F sits -3.0F below forecast.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXWTI-26NOV1914-T84.99`](https://kalshi.com/markets/kxwti-26nov1914) — Will the WTI crude oil settlement price be above 84.99 USD/Bbl on Nov 19, 2026? (Above $84.99)  
  * **Action:** Buy No (Limit) @ **83c** x **12 contracts** (Risk `$9.96` to win `$2.04` / `+20.48%`)  
  * **Book:** Yes Bid `14c` / No Bid `82c` | Spread `4c` | Book Depth `33990` | Expires `36.19h`  
  * **Oracle Proof:** Independent longshot bid at 14c Yes (82c No bid, 4c two-sided spread across 30 event market(s)).
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXNETFLIXRANKMOVIE-26NOV23-THE`](https://kalshi.com/markets/kxnetflixrankmovie-26nov23) — Will The Gospel of Christmas be Top US Netflix Movie on Nov 23, 2026? (The Gospel of Christmas)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `17c` / No Bid `81c` | Spread `2c` | Book Depth `42270` | Expires `151.69h`  
  * **Oracle Proof:** Independent longshot bid at 17c Yes (81c No bid, 2c two-sided spread across 10 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXLOWTCHI-26NOV18-B37.5](https://kalshi.com/markets/kxlowtchi-26nov18) | BUCKET_A_WEATHER_ATMOSPHERIC | 4c | 88c | **89c** | **11** (`$9.79`) | 8c | 2865 | +12.36% | 36.69h |
| 2 | [KXWTI-26NOV1914-T84.99](https://kalshi.com/markets/kxwti-26nov1914) | BUCKET_B_MACRO_ENERGY_COMMODITY | 14c | 82c | **83c** | **12** (`$9.96`) | 4c | 33990 | +20.48% | 36.19h |
| 3 | [KXWTI-26NOV1914-T85.49](https://kalshi.com/markets/kxwti-26nov1914) | BUCKET_B_MACRO_ENERGY_COMMODITY | 10c | 86c | **87c** | **11** (`$9.57`) | 4c | 17351 | +14.94% | 36.19h |
| 4 | [KXNETFLIXRANKMOVIE-26NOV23-THE](https://kalshi.com/markets/kxnetflixrankmovie-26nov23) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 81c | **82c** | **12** (`$9.84`) | 2c | 42270 | +21.95% | 151.69h |
| 5 | [KXDENSUPERLIGAGAME-26NOV22VIBRAN-RAN](https://kalshi.com/markets/kxdensuperligagame-26nov22vibran) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 17169 | +21.95% | 104.69h |
| 6 | [KXTFF1LIGGAME-26NOV22BATMUG-MUG](https://kalshi.com/markets/kxtff1liggame-26nov22batmug) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 13135 | +21.95% | 102.19h |
| 7 | [KXNETFLIXRANKSHOWGLOBAL2-26NOV23-BLA](https://kalshi.com/markets/kxnetflixrankshowglobal2-26nov23) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 82c | **83c** | **12** (`$9.96`) | 2c | 1285 | +20.48% | 151.69h |
| 8 | [KXNETFLIXTOPVIEWSMOVIE-26NOV23-21](https://kalshi.com/markets/kxnetflixtopviewsmovie-26nov23) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 10263 | +20.48% | 151.69h |
| 9 | [KXLIGUE1SPREAD-26NOV22FCLREN-REN2](https://kalshi.com/markets/kxligue1spread-26nov22fclren) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 40102 | +21.95% | 108.94h |
| 10 | [KXLIGAMXSPREAD-26NOV21PUMMON-MON2](https://kalshi.com/markets/kxligamxspread-26nov21pummon) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 31748 | +21.95% | 93.69h |
| 11 | [KXF1FP2FASTLAP-LASV26-LEC](https://kalshi.com/markets/kxf1fp2fastlap-lasv26) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 9c | 88c | **89c** | **11** (`$9.79`) | 3c | 1272 | +12.36% | 50.69h |
| 12 | [KXSERIEATOTAL-26NOV22JUVVEN-5](https://kalshi.com/markets/kxserieatotal-26nov22juvven) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 31215 | +21.95% | 104.19h |
| 13 | [KXLIGAMXSPREAD-26NOV21PUMMON-PUM2](https://kalshi.com/markets/kxligamxspread-26nov21pummon) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **12** (`$9.96`) | 4c | 21851 | +20.48% | 93.69h |
| 14 | [KXLIGAMXSPREAD-26NOV21PACTOL-PAC2](https://kalshi.com/markets/kxligamxspread-26nov21pactol) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **12** (`$9.96`) | 4c | 23195 | +20.48% | 91.53h |
| 15 | [KXBUNDESLIGASPREAD-26NOV22SVWHSV-SVW3](https://kalshi.com/markets/kxbundesligaspread-26nov22svwhsv) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 12363 | +20.48% | 109.19h |
| 16 | [KXBRASILEIROGAME-26NOV21CHACRU-CHA](https://kalshi.com/markets/kxbrasileirogame-26nov21chacru) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 80c | **82c** | **12** (`$9.84`) | 8c | 60166 | +21.95% | 91.69h |
| 17 | [KXSERIEATOTAL-26NOV22ACMFRO-6](https://kalshi.com/markets/kxserieatotal-26nov22acmfro) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 84c | **85c** | **11** (`$9.35`) | 2c | 46264 | +17.65% | 109.69h |
| 18 | [KXBOLPDIVGAME-26NOV21ORPIND-IND](https://kalshi.com/markets/kxbolpdivgame-26nov21orpind) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 82c | **83c** | **12** (`$9.96`) | 7c | 18099 | +20.48% | 91.19h |
| 19 | [KXHNLGAME-26NOV22DINIST-TIE](https://kalshi.com/markets/kxhnlgame-26nov22dinist) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 10c | 85c | **86c** | **11** (`$9.46`) | 5c | 11515 | +16.28% | 105.69h |
| 20 | [KXBELGIANPLGAME-26NOV22RSCOHL-OHL](https://kalshi.com/markets/kxbelgianplgame-26nov22rscohl) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **11** (`$9.46`) | 2c | 34526 | +16.28% | 109.19h |
| 21 | [KXSLGREECEGAME-26NOV22PANOFI-TIE](https://kalshi.com/markets/kxslgreecegame-26nov22panofi) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 10c | 86c | **87c** | **11** (`$9.57`) | 4c | 11274 | +14.94% | 107.19h |
| 22 | [KXLIGUE1TOTAL-26NOV22FCLREN-5](https://kalshi.com/markets/kxligue1total-26nov22fclren) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 85c | **86c** | **11** (`$9.46`) | 3c | 19878 | +16.28% | 108.94h |
| 23 | [KXINDSLGAME-26NOV22CHUMOH-CHU](https://kalshi.com/markets/kxindslgame-26nov22chumoh) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 10c | 83c | **84c** | **11** (`$9.24`) | 7c | 9778 | +19.05% | 105.69h |
| 24 | [KXHORMUZMAX-26NOV22-NOV22](https://kalshi.com/markets/kxhormuzmax-26nov22) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 84c | **85c** | **11** (`$9.35`) | 3c | 23782 | +17.65% | 151.69h |
| 25 | [KXTFF1LIGGAME-26NOV22BURSIV-TIE](https://kalshi.com/markets/kxtff1liggame-26nov22bursiv) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 9c | 85c | **86c** | **11** (`$9.46`) | 6c | 11224 | +16.28% | 107.69h |
