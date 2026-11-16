# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-16T06:18:52.010831+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `DEFAULT_SIZING_FLOOR ($200.00)`
* **Effective Sizing Bankroll:** `$200.00`
* **Max Dollar Risk Per Pick (5% Cap):** `$10.00` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$30.00`
* **Dry Powder Reserve (85% Min):** `$170.00`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `10513`
* **In Expiration Window (8h - 168h):** `3687` (Bucket A: `88`, Bucket B: `337`, Bucket C: `3262`)
* **Passed Preliminary Two-Sided Quote Gate:** `598` (A: `17`, B: `47`, C: `534`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `598`
* **Passed Bucket Spread & Depth Gate:** `215` (A: `3`, B: `9`, C: `203`)
* **Passed Strike-vs-Oracle Tail Gate:** `214` (A: `2`, B: `9`, C: `203`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXRAINDMKE-19NOV26-0`](https://kalshi.com/markets/kxraindmke-19nov26) — Rain in Milwaukee on Nov 19, 2026? (Above 0 inches)  
  * **Action:** Buy No (Limit) @ **89c** x **11 contracts** (Risk `$9.79` to win `$1.21` / `+12.36%`)  
  * **Book:** Yes Bid `5c` / No Bid `88c` | Spread `7c` | Book Depth `642` | Expires `104.69h`  
  * **Oracle Proof:** Independent longshot bid at 5c Yes (88c No bid, 7c two-sided spread across 1 event market(s)).
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXAAAGASCDGA-26NOV16-SD`](https://kalshi.com/markets/kxaaagascdga-26nov16) — Will gas prices show a small decrease? (Small decrease)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `16c` / No Bid `80c` | Spread `4c` | Book Depth `1979` | Expires `8.69h`  
  * **Oracle Proof:** Independent longshot bid at 16c Yes (80c No bid, 4c two-sided spread across 5 event market(s)).
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXUEFANLTEAMTOTAL-26NOV17POLSWE-SWE3`](https://kalshi.com/markets/kxuefanlteamtotal-26nov17polswe) — Will Sweden score over 2.5 goals? (Sweden over 2.5 goals)  
  * **Action:** Buy No (Limit) @ **84c** x **11 contracts** (Risk `$9.24` to win `$1.76` / `+19.05%`)  
  * **Book:** Yes Bid `14c` / No Bid `83c` | Spread `3c` | Book Depth `17527` | Expires `40.44h`  
  * **Oracle Proof:** Independent longshot bid at 14c Yes (83c No bid, 3c two-sided spread across 6 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXRAINDMKE-19NOV26-0](https://kalshi.com/markets/kxraindmke-19nov26) | BUCKET_A_WEATHER_ATMOSPHERIC | 5c | 88c | **89c** | **11** (`$9.79`) | 7c | 642 | +12.36% | 104.69h |
| 2 | [KXRAINDPIT-21NOV26-0](https://kalshi.com/markets/kxraindpit-21nov26) | BUCKET_A_WEATHER_ATMOSPHERIC | 2c | 86c | **87c** | **11** (`$9.57`) | 12c | 694 | +14.94% | 152.69h |
| 3 | [KXAAAGASCDGA-26NOV16-SD](https://kalshi.com/markets/kxaaagascdga-26nov16) | BUCKET_B_MACRO_ENERGY_COMMODITY | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 1979 | +21.95% | 8.69h |
| 4 | [KXAAAGASCDNC-26NOV16-LD](https://kalshi.com/markets/kxaaagascdnc-26nov16) | BUCKET_B_MACRO_ENERGY_COMMODITY | 9c | 89c | **90c** | **11** (`$9.90`) | 2c | 1774 | +11.11% | 8.69h |
| 5 | [KXAAAGASCDNV-26NOV16-SD](https://kalshi.com/markets/kxaaagascdnv-26nov16) | BUCKET_B_MACRO_ENERGY_COMMODITY | 10c | 86c | **87c** | **11** (`$9.57`) | 4c | 1538 | +14.94% | 8.69h |
| 6 | [KXWTI-26NOV1714-T90.49](https://kalshi.com/markets/kxwti-26nov1714) | BUCKET_B_MACRO_ENERGY_COMMODITY | 10c | 86c | **87c** | **11** (`$9.57`) | 4c | 14861 | +14.94% | 37.19h |
| 7 | [KXWTI-26NOV1714-T90.99](https://kalshi.com/markets/kxwti-26nov1714) | BUCKET_B_MACRO_ENERGY_COMMODITY | 7c | 89c | **90c** | **11** (`$9.90`) | 4c | 15120 | +11.11% | 37.19h |
| 8 | [KXWTIW-26NOV2014-B85.50](https://kalshi.com/markets/kxwtiw-26nov2014) | BUCKET_B_MACRO_ENERGY_COMMODITY | 7c | 90c | **91c** | **10** (`$9.10`) | 3c | 48017 | +9.89% | 109.19h |
| 9 | [KXWTIW-26NOV2014-B86.50](https://kalshi.com/markets/kxwtiw-26nov2014) | BUCKET_B_MACRO_ENERGY_COMMODITY | 8c | 89c | **90c** | **11** (`$9.90`) | 3c | 43409 | +11.11% | 109.19h |
| 10 | [KXUEFANLTEAMTOTAL-26NOV17POLSWE-SWE3](https://kalshi.com/markets/kxuefanlteamtotal-26nov17polswe) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 83c | **84c** | **11** (`$9.24`) | 3c | 17527 | +19.05% | 40.44h |
| 11 | [KXCONCACAFNLGAME-26NOV17NICMSR-MSR](https://kalshi.com/markets/kxconcacafnlgame-26nov17nicmsr) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 84c | **85c** | **11** (`$9.35`) | 3c | 41087 | +17.65% | 47.69h |
| 12 | [KXBRASILEIROTOTAL-26NOV18GPABAH-5](https://kalshi.com/markets/kxbrasileirototal-26nov18gpabah) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 31770 | +20.48% | 70.19h |
| 13 | [KXBRASILEIROSPREAD-26NOV18CRUPAL-PAL2](https://kalshi.com/markets/kxbrasileirospread-26nov18crupal) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 53346 | +21.95% | 69.19h |
| 14 | [KXCOLLECTIONSALE-KOCH-20NOV26-60000000](https://kalshi.com/markets/kxcollectionsale-koch-20nov26) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 2547 | +21.95% | 118.69h |
| 15 | [KXBRASILEIROSPREAD-26NOV18CRCHA-CR3](https://kalshi.com/markets/kxbrasileirospread-26nov18crcha) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 29858 | +20.48% | 68.69h |
| 16 | [KXBRASILEIROTOTAL-26NOV18CFCSAN-5](https://kalshi.com/markets/kxbrasileirototal-26nov18cfcsan) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 30279 | +21.95% | 68.19h |
| 17 | [KXSILVERW-26NOV2017-T49.99](https://kalshi.com/markets/kxsilverw-26nov2017) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 46111 | +21.95% | 111.69h |
| 18 | [KXEUROCUPGAME-26NOV181300WROBUD-WRO](https://kalshi.com/markets/kxeurocupgame-26nov181300wrobud) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 83c | **84c** | **11** (`$9.24`) | 4c | 8706 | +19.05% | 62.69h |
| 19 | [KXBRASILEIROTOTAL-26NOV18CRUPAL-5](https://kalshi.com/markets/kxbrasileirototal-26nov18crupal) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 83c | **84c** | **11** (`$9.24`) | 3c | 22559 | +19.05% | 69.19h |
| 20 | [KXLIGAMXTOTAL-26NOV20PUEASL-5](https://kalshi.com/markets/kxligamxtotal-26nov20pueasl) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 63727 | +21.95% | 118.69h |
| 21 | [KXUEFANLSCORE-26NOV17HUNNIR-HUN1NIR0](https://kalshi.com/markets/kxuefanlscore-26nov17hunnir) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 11134 | +20.48% | 40.44h |
| 22 | [KXEFLL1GAME-26NOV21BRADR-DR](https://kalshi.com/markets/kxefll1game-26nov21bradr) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 5801 | +21.95% | 131.69h |
| 23 | [KXCOPPEREVENT-20NOV261100-T630000](https://kalshi.com/markets/kxcopperevent-20nov261100) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 83c | **84c** | **11** (`$9.24`) | 4c | 745 | +19.05% | 105.69h |
| 24 | [KXLIGAMXSPREAD-26NOV20PUEASL-ASL2](https://kalshi.com/markets/kxligamxspread-26nov20pueasl) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 83c | **84c** | **11** (`$9.24`) | 3c | 20639 | +19.05% | 118.69h |
| 25 | [KXBRASILEIROTOTAL-26NOV19VITRBB-5](https://kalshi.com/markets/kxbrasileirototal-26nov19vitrbb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 83c | **84c** | **11** (`$9.24`) | 4c | 50564 | +19.05% | 92.19h |
