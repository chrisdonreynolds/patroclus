# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-17T07:49:25.900775+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `DEFAULT_SIZING_FLOOR ($200.00)`
* **Effective Sizing Bankroll:** `$200.00`
* **Max Dollar Risk Per Pick (5% Cap):** `$10.00` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$30.00`
* **Dry Powder Reserve (85% Min):** `$170.00`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `9910`
* **In Expiration Window (8h - 168h):** `2529` (Bucket A: `103`, Bucket B: `102`, Bucket C: `2324`)
* **Passed Preliminary Two-Sided Quote Gate:** `301` (A: `20`, B: `18`, C: `263`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `301`
* **Passed Bucket Spread & Depth Gate:** `116` (A: `7`, B: `5`, C: `104`)
* **Passed Strike-vs-Oracle Tail Gate:** `112` (A: `3`, B: `5`, C: `104`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXRAINWKND-26NOV21-DEN`](https://kalshi.com/markets/kxrainwknd-26nov21) — Will it rain in Denver between Nov 21 and Nov 22, 2026? (Denver)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `13c` / No Bid `80c` | Spread `7c` | Book Depth `1874` | Expires `165.18h`  
  * **Oracle Proof:** Independent longshot bid at 13c Yes (80c No bid, 7c two-sided spread across 36 event market(s)).
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXWTI-26NOV1814-T86.49`](https://kalshi.com/markets/kxwti-26nov1814) — Will the WTI crude oil settlement price be above 86.49 USD/Bbl on Nov 18, 2026? (Above $86.49)  
  * **Action:** Buy No (Limit) @ **83c** x **12 contracts** (Risk `$9.96` to win `$2.04` / `+20.48%`)  
  * **Book:** Yes Bid `14c` / No Bid `82c` | Spread `4c` | Book Depth `25180` | Expires `35.68h`  
  * **Oracle Proof:** Independent longshot bid at 14c Yes (82c No bid, 4c two-sided spread across 30 event market(s)).
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXSRBSLGAME-26NOV21RDNZEM-ZEM`](https://kalshi.com/markets/kxsrbslgame-26nov21rdnzem) — Zemun wins (Zemun)  
  * **Action:** Buy No (Limit) @ **83c** x **12 contracts** (Risk `$9.96` to win `$2.04` / `+20.48%`)  
  * **Book:** Yes Bid `16c` / No Bid `82c` | Spread `2c` | Book Depth `12203` | Expires `103.18h`  
  * **Oracle Proof:** Independent longshot bid at 16c Yes (82c No bid, 2c two-sided spread across 3 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXRAINWKND-26NOV21-DEN](https://kalshi.com/markets/kxrainwknd-26nov21) | BUCKET_A_WEATHER_ATMOSPHERIC | 13c | 80c | **82c** | **12** (`$9.84`) | 7c | 1874 | +21.95% | 165.18h |
| 2 | [KXLOWTCHI-26NOV17-B32.5](https://kalshi.com/markets/kxlowtchi-26nov17) | BUCKET_A_WEATHER_ATMOSPHERIC | 2c | 95c | **96c** | **10** (`$9.60`) | 3c | 2869 | +4.17% | 36.18h |
| 3 | [KXRAINWKND-26NOV21-LV](https://kalshi.com/markets/kxrainwknd-26nov21) | BUCKET_A_WEATHER_ATMOSPHERIC | 3c | 95c | **96c** | **10** (`$9.60`) | 2c | 915 | +4.17% | 165.18h |
| 4 | [KXWTI-26NOV1814-T86.49](https://kalshi.com/markets/kxwti-26nov1814) | BUCKET_B_MACRO_ENERGY_COMMODITY | 14c | 82c | **83c** | **12** (`$9.96`) | 4c | 25180 | +20.48% | 35.68h |
| 5 | [KXWTI-26NOV1714-T85.99](https://kalshi.com/markets/kxwti-26nov1714) | BUCKET_B_MACRO_ENERGY_COMMODITY | 9c | 89c | **90c** | **11** (`$9.90`) | 2c | 47873 | +11.11% | 11.68h |
| 6 | [KXWTI-26NOV1814-T86.99](https://kalshi.com/markets/kxwti-26nov1814) | BUCKET_B_MACRO_ENERGY_COMMODITY | 9c | 87c | **88c** | **11** (`$9.68`) | 4c | 14717 | +13.64% | 35.68h |
| 7 | [KXSRBSLGAME-26NOV21RDNZEM-ZEM](https://kalshi.com/markets/kxsrbslgame-26nov21rdnzem) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 82c | **83c** | **12** (`$9.96`) | 2c | 12203 | +20.48% | 103.18h |
| 8 | [KXLIGAMXTOTAL-26NOV20TIJALA-5](https://kalshi.com/markets/kxligamxtotal-26nov20tijala) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 82c | **83c** | **12** (`$9.96`) | 2c | 64992 | +20.48% | 95.18h |
| 9 | [KXEFLL1GAME-26NOV21BURALUT-BURA](https://kalshi.com/markets/kxefll1game-26nov21buralut) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 9859 | +21.95% | 106.18h |
| 10 | [KXLIGAMXTOTAL-26NOV20JUAATL-5](https://kalshi.com/markets/kxligamxtotal-26nov20juaatl) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 31019 | +20.48% | 95.18h |
| 11 | [KXLIGAMXTOTAL-26NOV21TIGAME-5](https://kalshi.com/markets/kxligamxtotal-26nov21tigame) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 61583 | +21.95% | 119.18h |
| 12 | [KXBELGIANPLGAME-26NOV21YRMBRU-TIE](https://kalshi.com/markets/kxbelgianplgame-26nov21yrmbru) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 83c | **84c** | **11** (`$9.24`) | 2c | 33464 | +19.05% | 110.93h |
| 13 | [KXEFLL1GAME-26NOV21REABRO-TIE](https://kalshi.com/markets/kxefll1game-26nov21reabro) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **12** (`$9.96`) | 4c | 9961 | +20.48% | 103.68h |
| 14 | [KXCZEFLGAME-26NOV21MLAFCZ-FCZ](https://kalshi.com/markets/kxczeflgame-26nov21mlafcz) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 84c | **85c** | **11** (`$9.35`) | 2c | 30513 | +17.65% | 105.18h |
| 15 | [KXSWISSLEAGUEGAME-26NOV21LUGGCZ-TIE](https://kalshi.com/markets/kxswissleaguegame-26nov21luggcz) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 81c | **82c** | **12** (`$9.84`) | 5c | 23752 | +21.95% | 108.18h |
| 16 | [KXLIGUE1TOTAL-26NOV22PARANG-5](https://kalshi.com/markets/kxligue1total-26nov22parang) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **12** (`$9.84`) | 3c | 13849 | +21.95% | 130.18h |
| 17 | [KXSLGREECEGAME-26NOV21KALAEK-TIE](https://kalshi.com/markets/kxslgreecegame-26nov21kalaek) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 80c | **82c** | **12** (`$9.84`) | 6c | 17103 | +21.95% | 108.68h |
| 18 | [KXTESTMATCH-26NOV162330SRIPAK-SRI](https://kalshi.com/markets/kxtestmatch-26nov162330sripak) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 86c | **87c** | **11** (`$9.57`) | 2c | 517417 | +14.94% | 116.68h |
| 19 | [KXBUNDESLIGASPREAD-26NOV21BMGBVB-BVB3](https://kalshi.com/markets/kxbundesligaspread-26nov21bmgbvb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 38081 | +21.95% | 106.68h |
| 20 | [KXSWISSLEAGUEGAME-26NOV21YBTHU-TIE](https://kalshi.com/markets/kxswissleaguegame-26nov21ybthu) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 82c | **83c** | **12** (`$9.96`) | 5c | 23695 | +20.48% | 108.18h |
| 21 | [KXLIGUE1TOTAL-26NOV21RCLTFC-5](https://kalshi.com/markets/kxligue1total-26nov21rcltfc) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 16009 | +21.95% | 111.93h |
| 22 | [KXBUNDESLIGASPREAD-26NOV21SGETSG-TSG2](https://kalshi.com/markets/kxbundesligaspread-26nov21sgetsg) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 17257 | +20.48% | 106.68h |
| 23 | [KXLIGUE1SPREAD-26NOV21LILOL-LIL2](https://kalshi.com/markets/kxligue1spread-26nov21lilol) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 15260 | +20.48% | 111.93h |
| 24 | [KXEFLL2GAME-26NOV21GRIROT-ROT](https://kalshi.com/markets/kxefll2game-26nov21grirot) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 80c | **82c** | **12** (`$9.84`) | 6c | 9067 | +21.95% | 106.18h |
| 25 | [KXBUNDESLIGATOTAL-26NOV21SGETSG-6](https://kalshi.com/markets/kxbundesligatotal-26nov21sgetsg) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 12683 | +20.48% | 106.68h |
