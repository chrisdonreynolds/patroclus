# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-21T06:58:23.226328+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `DEFAULT_SIZING_FLOOR ($200.00)`
* **Effective Sizing Bankroll:** `$200.00`
* **Max Dollar Risk Per Pick (5% Cap):** `$10.00` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$30.00`
* **Dry Powder Reserve (85% Min):** `$170.00`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `13013`
* **In Expiration Window (8h - 168h):** `5909` (Bucket A: `156`, Bucket B: `382`, Bucket C: `5371`)
* **Passed Preliminary Two-Sided Quote Gate:** `749` (A: `59`, B: `43`, C: `647`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `749`
* **Passed Bucket Spread & Depth Gate:** `296` (A: `15`, B: `13`, C: `268`)
* **Passed Strike-vs-Oracle Tail Gate:** `293` (A: `12`, B: `13`, C: `268`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXRAINTHANKSGIVING-26NOV26-SPG`](https://kalshi.com/markets/kxrainthanksgiving-26nov26) — Will it rain in St. Petersburg on Thanksgiving? (St. Petersburg)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `16c` / No Bid `80c` | Spread `4c` | Book Depth `5516` | Expires `152.03h`  
  * **Oracle Proof:** Independent longshot bid at 16c Yes (80c No bid, 4c two-sided spread across 48 event market(s)).
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXWTI-26NOV2414-T86.49`](https://kalshi.com/markets/kxwti-26nov2414) — Will the WTI crude oil settlement price be above 86.49 USD/Bbl on Nov 24, 2026? (Above $86.49)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `15c` / No Bid `81c` | Spread `4c` | Book Depth `13281` | Expires `84.53h`  
  * **Oracle Proof:** Independent longshot bid at 15c Yes (81c No bid, 4c two-sided spread across 30 event market(s)).
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXLALIGATEAMTOTAL-26NOV22GETATM-GET2`](https://kalshi.com/markets/kxlaligateamtotal-26nov22getatm) — Will Getafe score over 1.5 goals? (Getafe over 1.5 goals)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `15c` / No Bid `81c` | Spread `4c` | Book Depth `4002` | Expires `40.03h`  
  * **Oracle Proof:** Independent longshot bid at 15c Yes (81c No bid, 4c two-sided spread across 6 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXRAINTHANKSGIVING-26NOV26-SPG](https://kalshi.com/markets/kxrainthanksgiving-26nov26) | BUCKET_A_WEATHER_ATMOSPHERIC | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 5516 | +21.95% | 152.03h |
| 2 | [KXSNOWTHANKSGIVING-26NOV26-DTW](https://kalshi.com/markets/kxsnowthanksgiving-26nov26) | BUCKET_A_WEATHER_ATMOSPHERIC | 13c | 80c | **82c** | **12** (`$9.84`) | 7c | 5180 | +21.95% | 152.03h |
| 3 | [KXSNOWTHANKSGIVING-26NOV26-CMH](https://kalshi.com/markets/kxsnowthanksgiving-26nov26) | BUCKET_A_WEATHER_ATMOSPHERIC | 9c | 87c | **88c** | **11** (`$9.68`) | 4c | 7434 | +13.64% | 152.03h |
| 4 | [KXLOWTCHI-26NOV21-B46.5](https://kalshi.com/markets/kxlowtchi-26nov21) | BUCKET_A_WEATHER_ATMOSPHERIC | 2c | 95c | **96c** | **10** (`$9.60`) | 3c | 4019 | +4.17% | 37.03h |
| 5 | [KXRAINTHANKSGIVING-26NOV26-CLL](https://kalshi.com/markets/kxrainthanksgiving-26nov26) | BUCKET_A_WEATHER_ATMOSPHERIC | 7c | 91c | **92c** | **10** (`$9.20`) | 2c | 6283 | +8.7% | 152.03h |
| 6 | [KXWTI-26NOV2414-T86.49](https://kalshi.com/markets/kxwti-26nov2414) | BUCKET_B_MACRO_ENERGY_COMMODITY | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 13281 | +21.95% | 84.53h |
| 7 | [KXAAAGASCDHI-26NOV21-SD](https://kalshi.com/markets/kxaaagascdhi-26nov21) | BUCKET_B_MACRO_ENERGY_COMMODITY | 9c | 89c | **90c** | **11** (`$9.90`) | 2c | 2892 | +11.11% | 8.03h |
| 8 | [KXAAAGASCDAK-26NOV21-SD](https://kalshi.com/markets/kxaaagascdak-26nov21) | BUCKET_B_MACRO_ENERGY_COMMODITY | 10c | 88c | **89c** | **11** (`$9.79`) | 2c | 6610 | +12.36% | 8.03h |
| 9 | [KXWTI-26NOV2414-T87.49](https://kalshi.com/markets/kxwti-26nov2414) | BUCKET_B_MACRO_ENERGY_COMMODITY | 10c | 86c | **87c** | **11** (`$9.57`) | 4c | 12770 | +14.94% | 84.53h |
| 10 | [KXJOBLESSCLAIMS-26NOV25-210000](https://kalshi.com/markets/kxjoblessclaims-26nov25) | BUCKET_B_MACRO_ENERGY_COMMODITY | 7c | 88c | **89c** | **11** (`$9.79`) | 5c | 2768 | +12.36% | 104.01h |
| 11 | [KXWTIW-26NOV2714-B82.50](https://kalshi.com/markets/kxwtiw-26nov2714) | BUCKET_B_MACRO_ENERGY_COMMODITY | 8c | 89c | **90c** | **11** (`$9.90`) | 3c | 14731 | +11.11% | 156.53h |
| 12 | [KXPCECORE-26OCT-T0.3](https://kalshi.com/markets/kxpcecore-26oct) | BUCKET_B_MACRO_ENERGY_COMMODITY | 5c | 91c | **92c** | **10** (`$9.20`) | 4c | 54712 | +8.7% | 104.03h |
| 13 | [KXWTIW-26NOV2714-B80.50](https://kalshi.com/markets/kxwtiw-26nov2714) | BUCKET_B_MACRO_ENERGY_COMMODITY | 6c | 91c | **92c** | **10** (`$9.20`) | 3c | 13036 | +8.7% | 156.53h |
| 14 | [KXLALIGATEAMTOTAL-26NOV22GETATM-GET2](https://kalshi.com/markets/kxlaligateamtotal-26nov22getatm) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 4002 | +21.95% | 40.03h |
| 15 | [KXBULLETBRAWLTOP-26NOV21T5-RMAH](https://kalshi.com/markets/kxbulletbrawltop-26nov21t5) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 83c | **84c** | **11** (`$9.24`) | 4c | 1359 | +19.05% | 18.03h |
| 16 | [KXAPRPOTUS-26NOV27-38.7](https://kalshi.com/markets/kxaprpotus-26nov27) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **12** (`$9.84`) | 3c | 37421 | +21.95% | 153.03h |
| 17 | [KXLIGAMX1HTOTAL-26NOV22CDGCRA-3](https://kalshi.com/markets/kxligamx1htotal-26nov22cdgcra) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **12** (`$9.96`) | 4c | 1750 | +20.48% | 44.14h |
| 18 | [KXBOLPDIVGAME-26NOV22SANARE-TIE](https://kalshi.com/markets/kxbolpdivgame-26nov22sanare) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 80c | **82c** | **12** (`$9.84`) | 6c | 14506 | +21.95% | 43.53h |
| 19 | [KXBULLETBRAWLTOP-26NOV21T5-HXUE](https://kalshi.com/markets/kxbulletbrawltop-26nov21t5) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 86c | **87c** | **11** (`$9.57`) | 3c | 1633 | +14.94% | 18.03h |
| 20 | [KXLIGAMX1HTOTAL-26NOV22QUENCX-3](https://kalshi.com/markets/kxligamx1htotal-26nov22quencx) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 83c | **84c** | **11** (`$9.24`) | 4c | 2269 | +19.05% | 46.19h |
| 21 | [KXBRENTW-26NOV2717-T93.99](https://kalshi.com/markets/kxbrentw-26nov2717) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **12** (`$9.84`) | 3c | 33060 | +21.95% | 159.03h |
| 22 | [KXLIGAMXSPREAD-26NOV22CDGCRA-CRA2](https://kalshi.com/markets/kxligamxspread-26nov22cdgcra) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 54447 | +20.48% | 44.14h |
| 23 | [KXSERIEATEAMTOTAL-26NOV22ACMFRO-FRO3](https://kalshi.com/markets/kxserieateamtotal-26nov22acmfro) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 87c | **88c** | **11** (`$9.68`) | 2c | 2318 | +13.64% | 37.03h |
| 24 | [KXBULLETBRAWLTOP-26NOV21T3-JXIO](https://kalshi.com/markets/kxbulletbrawltop-26nov21t3) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 84c | **85c** | **11** (`$9.35`) | 5c | 1630 | +17.65% | 18.03h |
| 25 | [KXCOPPERW-26NOV2714-T5.75](https://kalshi.com/markets/kxcopperw-26nov2714) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 17920 | +21.95% | 156.78h |
