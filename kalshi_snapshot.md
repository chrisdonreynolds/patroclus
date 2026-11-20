# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-20T07:05:35.764939+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `DEFAULT_SIZING_FLOOR ($200.00)`
* **Effective Sizing Bankroll:** `$200.00`
* **Max Dollar Risk Per Pick (5% Cap):** `$10.00` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$30.00`
* **Dry Powder Reserve (85% Min):** `$170.00`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `9858`
* **In Expiration Window (8h - 168h):** `2895` (Bucket A: `66`, Bucket B: `100`, Bucket C: `2729`)
* **Passed Preliminary Two-Sided Quote Gate:** `135` (A: `14`, B: `28`, C: `93`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `135`
* **Passed Bucket Spread & Depth Gate:** `62` (A: `7`, B: `12`, C: `43`)
* **Passed Strike-vs-Oracle Tail Gate:** `57` (A: `2`, B: `12`, C: `43`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXLOWTNYC-26NOV20-B47.5`](https://kalshi.com/markets/kxlowtnyc-26nov20) — Will the minimum temperature be 47-48° on Nov 20, 2026? (47° to 48°)  
  * **Action:** Buy No (Limit) @ **91c** x **10 contracts** (Risk `$9.10` to win `$0.90` / `+9.89%`)  
  * **Book:** Yes Bid `7c` / No Bid `90c` | Spread `3c` | Book Depth `2844` | Expires `36.91h`  
  * **Oracle Proof:** NWS KNYC forecast low (2026-11-20) is 44.0F; bracket 47.0F-48.0F sits +3.0F above forecast.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXWTI-26NOV2314-T85.99`](https://kalshi.com/markets/kxwti-26nov2314) — Will the WTI crude oil settlement price be above 85.99 USD/Bbl on Nov 23, 2026? (Above $85.99)  
  * **Action:** Buy No (Limit) @ **84c** x **11 contracts** (Risk `$9.24` to win `$1.76` / `+19.05%`)  
  * **Book:** Yes Bid `13c` / No Bid `83c` | Spread `4c` | Book Depth `15839` | Expires `84.41h`  
  * **Oracle Proof:** Independent longshot bid at 13c Yes (83c No bid, 4c two-sided spread across 30 event market(s)).
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXBRASILEIROBTOTAL-26NOV22CRIFOR-4`](https://kalshi.com/markets/kxbrasileirobtotal-26nov22crifor) — Will over 3.5 goals be scored? (Over 3.5 goals scored)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `16c` / No Bid `81c` | Spread `3c` | Book Depth `13163` | Expires `63.91h`  
  * **Oracle Proof:** Independent longshot bid at 16c Yes (81c No bid, 3c two-sided spread across 6 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXLOWTNYC-26NOV20-B47.5](https://kalshi.com/markets/kxlowtnyc-26nov20) | BUCKET_A_WEATHER_ATMOSPHERIC | 7c | 90c | **91c** | **10** (`$9.10`) | 3c | 2844 | +9.89% | 36.91h |
| 2 | [KXLOWTCHI-26NOV20-B42.5](https://kalshi.com/markets/kxlowtchi-26nov20) | BUCKET_A_WEATHER_ATMOSPHERIC | 6c | 85c | **86c** | **11** (`$9.46`) | 9c | 3435 | +16.28% | 36.91h |
| 3 | [KXWTI-26NOV2314-T85.99](https://kalshi.com/markets/kxwti-26nov2314) | BUCKET_B_MACRO_ENERGY_COMMODITY | 13c | 83c | **84c** | **11** (`$9.24`) | 4c | 15839 | +19.05% | 84.41h |
| 4 | [KXWTI-26NOV2314-T86.49](https://kalshi.com/markets/kxwti-26nov2314) | BUCKET_B_MACRO_ENERGY_COMMODITY | 11c | 85c | **86c** | **11** (`$9.46`) | 4c | 15148 | +16.28% | 84.41h |
| 5 | [KXUSDJPYEVENT-26NOV261930-T16050](https://kalshi.com/markets/kxusdjpyevent-26nov261930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 12c | 81c | **82c** | **12** (`$9.84`) | 7c | 996 | +21.95% | 161.41h |
| 6 | [KXUSDJPYEVENT-26NOV261930-T16075](https://kalshi.com/markets/kxusdjpyevent-26nov261930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 8c | 85c | **86c** | **11** (`$9.46`) | 7c | 996 | +16.28% | 161.41h |
| 7 | [KXUSDMXNEVENT-26NOV261600-T194500](https://kalshi.com/markets/kxusdmxnevent-26nov261600) | BUCKET_B_MACRO_ENERGY_COMMODITY | 7c | 86c | **87c** | **11** (`$9.57`) | 7c | 1002 | +14.94% | 157.91h |
| 8 | [KXUSDMXNEVENT-26NOV261600-T195500](https://kalshi.com/markets/kxusdmxnevent-26nov261600) | BUCKET_B_MACRO_ENERGY_COMMODITY | 3c | 91c | **92c** | **10** (`$9.20`) | 6c | 997 | +8.7% | 157.91h |
| 9 | [KXBRASILEIROBTOTAL-26NOV22CRIFOR-4](https://kalshi.com/markets/kxbrasileirobtotal-26nov22crifor) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 13163 | +21.95% | 63.91h |
| 10 | [KXPERLIGA1GAME-26NOV22CRICIE-TIE](https://kalshi.com/markets/kxperliga1game-26nov22cricie) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 16337 | +21.95% | 63.91h |
| 11 | [KXBRASILEIROSPREAD-26NOV22RBBVDG-RBB2](https://kalshi.com/markets/kxbrasileirospread-26nov22rbbvdg) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 21259 | +21.95% | 67.41h |
| 12 | [KXBRASILEIROTOTAL-26NOV22RBBVDG-5](https://kalshi.com/markets/kxbrasileirototal-26nov22rbbvdg) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 22461 | +21.95% | 67.41h |
| 13 | [KXBRASILEIROTOTAL-26NOV22CAPCR-5](https://kalshi.com/markets/kxbrasileirototal-26nov22capcr) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 38726 | +21.95% | 63.91h |
| 14 | [KXBOLPDIVGAME-26NOV22POTBOL-TIE](https://kalshi.com/markets/kxbolpdivgame-26nov22potbol) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 82c | **83c** | **12** (`$9.96`) | 5c | 13979 | +20.48% | 62.91h |
| 15 | [KXLIGAMXSPREAD-26NOV22CDGCRA-CRA2](https://kalshi.com/markets/kxligamxspread-26nov22cdgcra) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 24327 | +21.95% | 68.02h |
| 16 | [KXBOLPDIVGAME-26NOV22SANARE-TIE](https://kalshi.com/markets/kxbolpdivgame-26nov22sanare) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 80c | **82c** | **12** (`$9.84`) | 7c | 11505 | +21.95% | 67.41h |
| 17 | [KXSVNPLGAME-26NOV23KOPALU-ALU](https://kalshi.com/markets/kxsvnplgame-26nov23kopalu) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 82c | **83c** | **12** (`$9.96`) | 5c | 13829 | +20.48% | 84.41h |
| 18 | [KXVENFUTVEGAME-26NOV22CFCPOR-POR](https://kalshi.com/markets/kxvenfutvegame-26nov22cfcpor) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 83c | **84c** | **11** (`$9.24`) | 6c | 8618 | +19.05% | 65.41h |
| 19 | [KXPERLIGA1GAME-26NOV22CRICIE-CIE](https://kalshi.com/markets/kxperliga1game-26nov22cricie) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 87c | **88c** | **11** (`$9.68`) | 2c | 65322 | +13.64% | 63.91h |
| 20 | [KXGOLDEVENT-25NOV261430-T365000](https://kalshi.com/markets/kxgoldevent-25nov261430) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 80c | **82c** | **12** (`$9.84`) | 7c | 149 | +21.95% | 132.41h |
| 21 | [KXBRASILEIROSPREAD-26NOV22FLUMIR-FLU3](https://kalshi.com/markets/kxbrasileirospread-26nov22flumir) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 81c | **82c** | **12** (`$9.84`) | 8c | 19705 | +21.95% | 66.41h |
| 22 | [KXBOLPDIVGAME-26NOV22STRBLO-TIE](https://kalshi.com/markets/kxbolpdivgame-26nov22strblo) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 10c | 83c | **84c** | **11** (`$9.24`) | 7c | 11662 | +19.05% | 65.16h |
| 23 | [KXUSDJPYEVENT-25NOV260930-T16025](https://kalshi.com/markets/kxusdjpyevent-25nov260930) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 81c | **82c** | **12** (`$9.84`) | 7c | 994 | +21.95% | 127.41h |
| 24 | [KXBRASILEIROSPREAD-26NOV22RBBVDG-VDG2](https://kalshi.com/markets/kxbrasileirospread-26nov22rbbvdg) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 84c | **85c** | **11** (`$9.35`) | 5c | 6566 | +17.65% | 67.41h |
| 25 | [KXBRASILEIROBSPREAD-26NOV22GOIVIN-GOI3](https://kalshi.com/markets/kxbrasileirobspread-26nov22goivin) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 7c | 91c | **92c** | **10** (`$9.20`) | 2c | 14283 | +8.7% | 66.41h |
