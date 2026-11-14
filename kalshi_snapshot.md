# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-14T06:12:18.177298+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `LIVE_KALSHI_PORTFOLIO_API (Live=$1071.99; SizingFloor=$200.00)`
* **Effective Sizing Bankroll:** `$1071.99`
* **Max Dollar Risk Per Pick (5% Cap):** `$53.60` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$160.80`
* **Dry Powder Reserve (85% Min):** `$911.19`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `11663`
* **In Expiration Window (8h - 168h):** `5011` (Bucket A: `85`, Bucket B: `253`, Bucket C: `4673`)
* **Passed Preliminary Two-Sided Quote Gate:** `589` (A: `11`, B: `44`, C: `534`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `589`
* **Passed Bucket Spread & Depth Gate:** `142` (A: `4`, B: `3`, C: `135`)
* **Passed Strike-vs-Oracle Tail Gate:** `138` (A: `1`, B: `2`, C: `135`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXHIGHNY-26NOV14-B48.5`](https://kalshi.com/markets/kxhighny-26nov14) — Will the maximum temperature be 48-49° on Nov 14, 2026? (48° to 49°)  
  * **Action:** Buy No (Limit) @ **85c** x **63 contracts** (Risk `$53.55` to win `$9.45` / `+17.65%`)  
  * **Book:** Yes Bid `13c` / No Bid `84c` | Spread `3c` | Book Depth `11443` | Expires `37.79h`  
  * **Oracle Proof:** NWS KNYC forecast high (2026-11-14) is 45.0F; bracket 48.0F-49.0F sits +3.0F above forecast.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXAAAGASCDDE-26NOV14-MC`](https://kalshi.com/markets/kxaaagascdde-26nov14) — Will gas prices show a minimal change? (Minimal change)  
  * **Action:** Buy No (Limit) @ **89c** x **60 contracts** (Risk `$53.40` to win `$6.60` / `+12.36%`)  
  * **Book:** Yes Bid `5c` / No Bid `88c` | Spread `7c` | Book Depth `941` | Expires `8.79h`  
  * **Oracle Proof:** Tail longshot bid at 5c Yes (mutually exclusive event modal peak 75c Yes across 5 slices); 7c spread.
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXUEFANLTOTAL-26NOV16GRESRB-5`](https://kalshi.com/markets/kxuefanltotal-26nov16gresrb) — Will over 4.5 goals be scored? (Over 4.5 goals scored)  
  * **Action:** Buy No (Limit) @ **84c** x **63 contracts** (Risk `$52.92` to win `$10.08` / `+19.05%`)  
  * **Book:** Yes Bid `15c` / No Bid `83c` | Spread `2c` | Book Depth `110539` | Expires `65.54h`  
  * **Oracle Proof:** Independent longshot bid at 15c Yes (83c No bid, 2c two-sided spread across 6 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXHIGHNY-26NOV14-B48.5](https://kalshi.com/markets/kxhighny-26nov14) | BUCKET_A_WEATHER_ATMOSPHERIC | 13c | 84c | **85c** | **63** (`$53.55`) | 3c | 11443 | +17.65% | 37.79h |
| 2 | [KXAAAGASCDDE-26NOV14-MC](https://kalshi.com/markets/kxaaagascdde-26nov14) | BUCKET_B_MACRO_ENERGY_COMMODITY | 5c | 88c | **89c** | **60** (`$53.40`) | 7c | 941 | +12.36% | 8.79h |
| 3 | [KXJOBLESSCLAIMS-26NOV19-210000](https://kalshi.com/markets/kxjoblessclaims-26nov19) | BUCKET_B_MACRO_ENERGY_COMMODITY | 2c | 94c | **95c** | **56** (`$53.20`) | 4c | 2894 | +5.26% | 128.78h |
| 4 | [KXUEFANLTOTAL-26NOV16GRESRB-5](https://kalshi.com/markets/kxuefanltotal-26nov16gresrb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 83c | **84c** | **63** (`$52.92`) | 2c | 110539 | +19.05% | 65.54h |
| 5 | [KXGOLDEVENT-18NOV261330-T395000](https://kalshi.com/markets/kxgoldevent-18nov261330) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **65** (`$53.30`) | 4c | 21031 | +21.95% | 108.29h |
| 6 | [KXCOLLECTIONSALE-KOONS-17NOV26-150000000](https://kalshi.com/markets/kxcollectionsale-koons-17nov26) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **65** (`$53.30`) | 3c | 14175 | +21.95% | 94.79h |
| 7 | [KXUEFANLTEAMTOTAL-26NOV15BLRALB-ALB3](https://kalshi.com/markets/kxuefanlteamtotal-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 80c | **82c** | **65** (`$53.30`) | 6c | 35354 | +21.95% | 37.79h |
| 8 | [KXCOPPEREVENT-19NOV261330-T630000](https://kalshi.com/markets/kxcopperevent-19nov261330) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **65** (`$53.30`) | 4c | 21988 | +21.95% | 132.29h |
| 9 | [KXEUROLEAGUEGAME-26NOV171300ASVFEN-ASV](https://kalshi.com/markets/kxeuroleaguegame-26nov171300asvfen) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 80c | **82c** | **65** (`$53.30`) | 6c | 20054 | +21.95% | 86.79h |
| 10 | [KXUEFANLSPREAD-26NOV16GERNED-GER3](https://kalshi.com/markets/kxuefanlspread-26nov16gerned) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **62** (`$53.32`) | 2c | 80438 | +16.28% | 65.54h |
| 11 | [KXCOLLECTIONSALE-KOCH-20NOV26-60000000](https://kalshi.com/markets/kxcollectionsale-koch-20nov26) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 82c | **83c** | **64** (`$53.12`) | 2c | 14150 | +20.48% | 166.79h |
| 12 | [KXUEFANLSCORE-26NOV15BLRALB-BLR1ALB1](https://kalshi.com/markets/kxuefanlscore-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 86c | **87c** | **61** (`$53.07`) | 2c | 9090 | +14.94% | 37.79h |
| 13 | [KXBRASILEIROTOTAL-26NOV18CFCSAN-5](https://kalshi.com/markets/kxbrasileirototal-26nov18cfcsan) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **64** (`$53.12`) | 4c | 19114 | +20.48% | 116.29h |
| 14 | [KXRT-HOWT-35](https://kalshi.com/markets/kxrt-howt) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 86c | **87c** | **61** (`$53.07`) | 2c | 68711 | +14.94% | 56.79h |
| 15 | [KXLALIGA2GAME-26NOV16ALBRCC-RCC](https://kalshi.com/markets/kxlaliga2game-26nov16albrcc) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **65** (`$53.30`) | 4c | 30363 | +21.95% | 64.29h |
| 16 | [KXUSLTOTAL-26NOV15NEWSRP-5](https://kalshi.com/markets/kxusltotal-26nov15newsrp) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 10c | 87c | **88c** | **60** (`$52.80`) | 3c | 6827 | +13.64% | 45.79h |
| 17 | [KXRT-EBE-55](https://kalshi.com/markets/kxrt-ebe) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 9c | 89c | **90c** | **59** (`$53.10`) | 2c | 97564 | +11.11% | 56.79h |
| 18 | [KXUEFANLSCORE-26NOV15BLRALB-BLR0ALB1](https://kalshi.com/markets/kxuefanlscore-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 85c | **86c** | **62** (`$53.32`) | 3c | 9810 | +16.28% | 37.79h |
| 19 | [KXBRASILEIROGAME-26NOV18CRCHA-CHA](https://kalshi.com/markets/kxbrasileirogame-26nov18crcha) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **65** (`$53.30`) | 4c | 47696 | +21.95% | 115.79h |
| 20 | [KXCOPPEREVENT-18NOV261330-T630000](https://kalshi.com/markets/kxcopperevent-18nov261330) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 83c | **84c** | **63** (`$52.92`) | 5c | 24511 | +19.05% | 108.29h |
| 21 | [KXCOPPEREVENT-18NOV261430-T630000](https://kalshi.com/markets/kxcopperevent-18nov261430) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 83c | **84c** | **63** (`$52.92`) | 5c | 22286 | +19.05% | 109.29h |
| 22 | [KXBRASILEIROSPREAD-26NOV18CRCHA-CR3](https://kalshi.com/markets/kxbrasileirospread-26nov18crcha) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 84c | **85c** | **63** (`$53.55`) | 2c | 20460 | +17.65% | 116.79h |
| 23 | [KXPERLIGA1GAME-26NOV16CUSASO-ASO](https://kalshi.com/markets/kxperliga1game-26nov16cusaso) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 83c | **84c** | **63** (`$52.92`) | 6c | 24804 | +19.05% | 65.04h |
| 24 | [KXAPRPOTUS-26NOV20-37.8](https://kalshi.com/markets/kxaprpotus-26nov20) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 80c | **82c** | **65** (`$53.30`) | 5c | 30191 | +21.95% | 153.79h |
| 25 | [KXGOLDEVENT-20NOV261100-T400000](https://kalshi.com/markets/kxgoldevent-20nov261100) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 85c | **86c** | **62** (`$53.32`) | 3c | 24217 | +16.28% | 153.79h |
