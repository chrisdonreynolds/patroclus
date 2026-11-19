# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-19T07:16:28.856952+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `DEFAULT_SIZING_FLOOR ($200.00)`
* **Effective Sizing Bankroll:** `$200.00`
* **Max Dollar Risk Per Pick (5% Cap):** `$10.00` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$30.00`
* **Dry Powder Reserve (85% Min):** `$170.00`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `10187`
* **In Expiration Window (8h - 168h):** `3089` (Bucket A: `66`, Bucket B: `89`, Bucket C: `2934`)
* **Passed Preliminary Two-Sided Quote Gate:** `206` (A: `16`, B: `19`, C: `171`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `206`
* **Passed Bucket Spread & Depth Gate:** `87` (A: `4`, B: `9`, C: `74`)
* **Passed Strike-vs-Oracle Tail Gate:** `85` (A: `2`, B: `9`, C: `74`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXHIGHDEN-26NOV19-B50.5`](https://kalshi.com/markets/kxhighden-26nov19) — Will the maximum temperature be 50-51° on Nov 19, 2026? (50° to 51°)  
  * **Action:** Buy No (Limit) @ **91c** x **10 contracts** (Risk `$9.10` to win `$0.90` / `+9.89%`)  
  * **Book:** Yes Bid `8c` / No Bid `90c` | Spread `2c` | Book Depth `5298` | Expires `36.73h`  
  * **Oracle Proof:** NWS KDEN forecast high (2026-11-19) is 55.0F; bracket 50.0F-51.0F sits -4.0F below forecast.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXWTI-26NOV2014-T84.49`](https://kalshi.com/markets/kxwti-26nov2014) — Will the WTI crude oil settlement price be above 84.49 USD/Bbl on Nov 20, 2026? (Above $84.49)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `16c` / No Bid `80c` | Spread `4c` | Book Depth `15007` | Expires `36.23h`  
  * **Oracle Proof:** Independent longshot bid at 16c Yes (80c No bid, 4c two-sided spread across 30 event market(s)).
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXSUPERLIGGAME-26NOV22KONBES-KON`](https://kalshi.com/markets/kxsuperliggame-26nov22konbes) — Konyaspor wins (Konyaspor)  
  * **Action:** Buy No (Limit) @ **82c** x **12 contracts** (Risk `$9.84` to win `$2.16` / `+21.95%`)  
  * **Book:** Yes Bid `15c` / No Bid `81c` | Spread `4c` | Book Depth `60733` | Expires `80.73h`  
  * **Oracle Proof:** Independent longshot bid at 15c Yes (81c No bid, 4c two-sided spread across 3 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXHIGHDEN-26NOV19-B50.5](https://kalshi.com/markets/kxhighden-26nov19) | BUCKET_A_WEATHER_ATMOSPHERIC | 8c | 90c | **91c** | **10** (`$9.10`) | 2c | 5298 | +9.89% | 36.73h |
| 2 | [KXLOWTCHI-26NOV19-B45.5](https://kalshi.com/markets/kxlowtchi-26nov19) | BUCKET_A_WEATHER_ATMOSPHERIC | 6c | 92c | **93c** | **10** (`$9.30`) | 2c | 2992 | +7.53% | 36.73h |
| 3 | [KXWTI-26NOV2014-T84.49](https://kalshi.com/markets/kxwti-26nov2014) | BUCKET_B_MACRO_ENERGY_COMMODITY | 16c | 80c | **82c** | **12** (`$9.84`) | 4c | 15007 | +21.95% | 36.23h |
| 4 | [KXWTI-26NOV2014-T84.99](https://kalshi.com/markets/kxwti-26nov2014) | BUCKET_B_MACRO_ENERGY_COMMODITY | 11c | 85c | **86c** | **11** (`$9.46`) | 4c | 30543 | +16.28% | 36.23h |
| 5 | [KXUSDJPYEVENT-25NOV260930-T16075](https://kalshi.com/markets/kxusdjpyevent-25nov260930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 13c | 80c | **82c** | **12** (`$9.84`) | 7c | 1496 | +21.95% | 151.23h |
| 6 | [KXUSDJPYEVENT-25NOV260930-T16100](https://kalshi.com/markets/kxusdjpyevent-25nov260930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 9c | 84c | **85c** | **11** (`$9.35`) | 7c | 1006 | +17.65% | 151.23h |
| 7 | [KXUSDMXNEVENT-25NOV260930-T191500](https://kalshi.com/markets/kxusdmxnevent-25nov260930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 7c | 86c | **87c** | **11** (`$9.57`) | 7c | 255 | +14.94% | 151.23h |
| 8 | [KXUSDMXNEVENT-25NOV260930-T192500](https://kalshi.com/markets/kxusdmxnevent-25nov260930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 2c | 91c | **92c** | **10** (`$9.20`) | 7c | 254 | +8.7% | 151.23h |
| 9 | [KXSUPERLIGGAME-26NOV22KONBES-KON](https://kalshi.com/markets/kxsuperliggame-26nov22konbes) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **12** (`$9.84`) | 4c | 60733 | +21.95% | 80.73h |
| 10 | [KXSLGREECEGAME-26NOV22PAOKKIF-TIE](https://kalshi.com/markets/kxslgreecegame-26nov22paokkif) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 31812 | +21.95% | 85.23h |
| 11 | [KXBRASILEIROTOTAL-26NOV22CAPCR-5](https://kalshi.com/markets/kxbrasileirototal-26nov22capcr) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **12** (`$9.84`) | 3c | 59910 | +21.95% | 87.73h |
| 12 | [KXLIGUE1TOTAL-26NOV22PARANG-5](https://kalshi.com/markets/kxligue1total-26nov22parang) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **12** (`$9.84`) | 3c | 24166 | +21.95% | 82.73h |
| 13 | [KXLIGUE1SPREAD-26NOV22FCLREN-REN2](https://kalshi.com/markets/kxligue1spread-26nov22fclren) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 82c | **83c** | **12** (`$9.96`) | 2c | 38356 | +20.48% | 84.98h |
| 14 | [KXBUNDESLIGASPREAD-26NOV22FCAM05-FCA2](https://kalshi.com/markets/kxbundesligaspread-26nov22fcam05) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 83c | **84c** | **11** (`$9.24`) | 2c | 69181 | +19.05% | 83.23h |
| 15 | [KXBUNDESLIGASPREAD-26NOV22SVWHSV-SVW3](https://kalshi.com/markets/kxbundesligaspread-26nov22svwhsv) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **12** (`$9.96`) | 3c | 39265 | +20.48% | 85.23h |
| 16 | [KXBOLPDIVGAME-26NOV22POTBOL-TIE](https://kalshi.com/markets/kxbolpdivgame-26nov22potbol) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 83c | **84c** | **11** (`$9.24`) | 5c | 17006 | +19.05% | 86.73h |
| 17 | [KXBOLPDIVGAME-26NOV22SANARE-TIE](https://kalshi.com/markets/kxbolpdivgame-26nov22sanare) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 80c | **82c** | **12** (`$9.84`) | 7c | 14732 | +21.95% | 91.23h |
| 18 | [KXBELGIANPLGAME-26NOV22RSCOHL-OHL](https://kalshi.com/markets/kxbelgianplgame-26nov22rscohl) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **11** (`$9.46`) | 2c | 38225 | +16.28% | 85.23h |
| 19 | [KXSLGREECEGAME-26NOV22PANOFI-TIE](https://kalshi.com/markets/kxslgreecegame-26nov22panofi) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 87c | **88c** | **11** (`$9.68`) | 2c | 15055 | +13.64% | 83.23h |
| 20 | [KXLIGAMXSPREAD-26NOV22CDGCRA-CRA2](https://kalshi.com/markets/kxligamxspread-26nov22cdgcra) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 83c | **84c** | **11** (`$9.24`) | 3c | 25527 | +19.05% | 91.84h |
| 21 | [KXBOLPDIVGAME-26NOV22POTBOL-POT](https://kalshi.com/markets/kxbolpdivgame-26nov22potbol) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 9c | 88c | **89c** | **11** (`$9.79`) | 3c | 62969 | +12.36% | 86.73h |
| 22 | [KXLIGUE1SPREAD-26NOV22FCLREN-FCL2](https://kalshi.com/markets/kxligue1spread-26nov22fclren) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 85c | **86c** | **11** (`$9.46`) | 3c | 10657 | +16.28% | 84.98h |
| 23 | [KXBULFLGAME-26NOV22LEVLSO-TIE](https://kalshi.com/markets/kxbulflgame-26nov22levlso) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 82c | **83c** | **12** (`$9.96`) | 7c | 9869 | +20.48% | 81.23h |
| 24 | [KXBUNDESLIGATOTAL-26NOV22FCAM05-6](https://kalshi.com/markets/kxbundesligatotal-26nov22fcam05) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 86c | **87c** | **11** (`$9.57`) | 2c | 25297 | +14.94% | 83.23h |
| 25 | [KXPERLIGA1GAME-26NOV22CRICIE-CIE](https://kalshi.com/markets/kxperliga1game-26nov22cricie) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 11c | 85c | **86c** | **11** (`$9.46`) | 4c | 67762 | +16.28% | 87.73h |
