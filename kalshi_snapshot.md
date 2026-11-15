# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-15T06:20:18.265599+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `DEFAULT_SIZING_FLOOR ($200.00)`
* **Effective Sizing Bankroll:** `$200.00`
* **Max Dollar Risk Per Pick (5% Cap):** `$10.00` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$30.00`
* **Dry Powder Reserve (85% Min):** `$170.00`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `12749`
* **In Expiration Window (8h - 168h):** `5162` (Bucket A: `85`, Bucket B: `377`, Bucket C: `4700`)
* **Passed Preliminary Two-Sided Quote Gate:** `759` (A: `13`, B: `58`, C: `688`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `759`
* **Passed Bucket Spread & Depth Gate:** `279` (A: `2`, B: `5`, C: `272`)
* **Passed Strike-vs-Oracle Tail Gate:** `278` (A: `1`, B: `5`, C: `272`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXHIGHDEN-26NOV15-B60.5`](https://kalshi.com/markets/kxhighden-26nov15) — Will the maximum temperature be 60-61° on Nov 15, 2026? (60° to 61°)  
  * **Action:** Buy No (Limit) @ **90c** x **11 contracts** (Risk `$9.90` to win `$1.10` / `+11.11%`)  
  * **Book:** Yes Bid `9c` / No Bid `89c` | Spread `2c` | Book Depth `6714` | Expires `37.66h`  
  * **Oracle Proof:** NWS KDEN forecast high (2026-11-15) is 56.0F; bracket 60.0F-61.0F sits +4.0F above forecast.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXAAAGASCDID-26NOV15-MC`](https://kalshi.com/markets/kxaaagascdid-26nov15) — Will gas prices show a minimal change? (Minimal change)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `16c` / No Bid `80c` | Spread `4c` | Book Depth `1972` | Expires `8.66h`  
  * **Oracle Proof:** Tail longshot bid at 16c Yes (mutually exclusive event modal peak 81c Yes across 5 slices); 4c spread.
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXUEFANLFTTS-26NOV15FRATUR-TUR`](https://kalshi.com/markets/kxuefanlftts-26nov15fratur) — Will Turkiye record the first goal of the game? (Turkiye)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `17c` / No Bid `80c` | Spread `3c` | Book Depth `6477` | Expires `16.41h`  
  * **Oracle Proof:** Independent longshot bid at 17c Yes (80c No bid, 3c two-sided spread across 3 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXHIGHDEN-26NOV15-B60.5](https://kalshi.com/markets/kxhighden-26nov15) | BUCKET_A_WEATHER_ATMOSPHERIC | 9c | 89c | **90c** | **11** (`$9.90`) | 2c | 6714 | +11.11% | 37.66h |
| 2 | [KXAAAGASCDID-26NOV15-MC](https://kalshi.com/markets/kxaaagascdid-26nov15) | BUCKET_B_MACRO_ENERGY_COMMODITY | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 1972 | +21.95% | 8.66h |
| 3 | [KXAAAGASCDVA-26NOV15-LD](https://kalshi.com/markets/kxaaagascdva-26nov15) | BUCKET_B_MACRO_ENERGY_COMMODITY | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 1593 | +21.95% | 8.66h |
| 4 | [KXAAAGASCDDE-26NOV15-SD](https://kalshi.com/markets/kxaaagascdde-26nov15) | BUCKET_B_MACRO_ENERGY_COMMODITY | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 1488 | +21.95% | 8.66h |
| 5 | [KXAAAGASCDIA-26NOV15-SD](https://kalshi.com/markets/kxaaagascdia-26nov15) | BUCKET_B_MACRO_ENERGY_COMMODITY | 10c | 82c | **83c** | **12** (`$9.96`) | 8c | 193 | +20.48% | 8.66h |
| 6 | [KXJOBLESSCLAIMS-26NOV19-210000](https://kalshi.com/markets/kxjoblessclaims-26nov19) | BUCKET_B_MACRO_ENERGY_COMMODITY | 2c | 93c | **94c** | **10** (`$9.40`) | 5c | 2430 | +6.38% | 104.64h |
| 7 | [KXUEFANLFTTS-26NOV15FRATUR-TUR](https://kalshi.com/markets/kxuefanlftts-26nov15fratur) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **12** (`$9.84`) | 3c | 6477 | +21.95% | 16.41h |
| 8 | [KXUEFANLSCORE-26NOV16GIBMLT-GIB0MLT1](https://kalshi.com/markets/kxuefanlscore-26nov16gibmlt) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 82c | **83c** | **12** (`$9.96`) | 2c | 8418 | +20.48% | 40.41h |
| 9 | [KXUEFANLTOTAL-26NOV17POLSWE-5](https://kalshi.com/markets/kxuefanltotal-26nov17polswe) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 81c | **82c** | **12** (`$9.84`) | 2c | 90070 | +21.95% | 65.41h |
| 10 | [KXSVK2LGAME-26NOV16FTPZVO-TIE](https://kalshi.com/markets/kxsvk2lgame-26nov16ftpzvo) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 15176 | +21.95% | 36.66h |
| 11 | [KXUEFANLSCORE-26NOV16LTULIE-LTU1LIE0](https://kalshi.com/markets/kxuefanlscore-26nov16ltulie) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 83c | **84c** | **11** (`$9.24`) | 2c | 8810 | +19.05% | 37.66h |
| 12 | [KXUEFANLTOTAL-26NOV17ISRAUT-5](https://kalshi.com/markets/kxuefanltotal-26nov17israut) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **12** (`$9.84`) | 3c | 69908 | +21.95% | 65.41h |
| 13 | [KXUEFANLSCORE-26NOV16LTULIE-LTU2LIE0](https://kalshi.com/markets/kxuefanlscore-26nov16ltulie) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 8755 | +21.95% | 37.66h |
| 14 | [KXUEFANLTEAMTOTAL-26NOV16GERNED-NED3](https://kalshi.com/markets/kxuefanlteamtotal-26nov16gerned) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 25438 | +21.95% | 40.41h |
| 15 | [KXUEFANLSPREAD-26NOV16GIBMLT-MLT3](https://kalshi.com/markets/kxuefanlspread-26nov16gibmlt) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 83c | **84c** | **11** (`$9.24`) | 2c | 48739 | +19.05% | 41.41h |
| 16 | [KXUEFANLTOTAL-26NOV17IRLKOS-4](https://kalshi.com/markets/kxuefanltotal-26nov17irlkos) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 81c | **82c** | **12** (`$9.84`) | 2c | 90537 | +21.95% | 65.41h |
| 17 | [KXUEFANLTEAMTOTAL-26NOV15BELITA-ITA3](https://kalshi.com/markets/kxuefanlteamtotal-26nov15belita) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **11** (`$9.46`) | 2c | 20698 | +16.28% | 16.41h |
| 18 | [KXUEFANLSPREAD-26NOV17UKRGEO-UKR2](https://kalshi.com/markets/kxuefanlspread-26nov17ukrgeo) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **12** (`$9.84`) | 3c | 32080 | +21.95% | 65.41h |
| 19 | [KXUEFANLSCORE-26NOV16ESTBUL-EST1BUL0](https://kalshi.com/markets/kxuefanlscore-26nov16estbul) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 83c | **84c** | **11** (`$9.24`) | 3c | 9190 | +19.05% | 37.66h |
| 20 | [KXSVK2LGAME-26NOV16FTPZVO-ZVO](https://kalshi.com/markets/kxsvk2lgame-26nov16ftpzvo) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 85c | **86c** | **11** (`$9.46`) | 3c | 26910 | +16.28% | 36.66h |
| 21 | [KXCONCACAFNLTOTAL-26NOV16GLPBMU-6](https://kalshi.com/markets/kxconcacafnltotal-26nov16glpbmu) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **11** (`$9.46`) | 2c | 43313 | +16.28% | 40.66h |
| 22 | [KXINTLFRIENDLYGAME-26NOV16ANDAZE-AND](https://kalshi.com/markets/kxintlfriendlygame-26nov16andaze) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 84c | **85c** | **11** (`$9.35`) | 3c | 66392 | +17.65% | 38.66h |
| 23 | [KXUEFANLSPREAD-26NOV17ISRAUT-AUT3](https://kalshi.com/markets/kxuefanlspread-26nov17israut) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **12** (`$9.84`) | 3c | 73107 | +21.95% | 65.41h |
| 24 | [KXUEFANL1HSPREAD-26NOV16GIBMLT-MLT2](https://kalshi.com/markets/kxuefanl1hspread-26nov16gibmlt) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 84c | **85c** | **11** (`$9.35`) | 3c | 2012 | +17.65% | 41.41h |
| 25 | [KXUEFANLSCORE-26NOV16GIBMLT-GIB0MLT2](https://kalshi.com/markets/kxuefanlscore-26nov16gibmlt) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 84c | **85c** | **11** (`$9.35`) | 3c | 8629 | +17.65% | 40.41h |
