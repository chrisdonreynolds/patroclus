# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-13T20:38:12.991517+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `LIVE_KALSHI_PORTFOLIO_API (Live=$1059.98; SizingFloor=$200.00)`
* **Effective Sizing Bankroll:** `$1059.98`
* **Max Dollar Risk Per Pick (5% Cap):** `$53.00` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$159.00`
* **Dry Powder Reserve (85% Min):** `$900.98`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `10144`
* **In Expiration Window (8h - 168h):** `3457` (Bucket A: `109`, Bucket B: `196`, Bucket C: `3152`)
* **Passed Preliminary Two-Sided Quote Gate:** `340` (A: `22`, B: `31`, C: `287`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `340`
* **Passed Bucket Spread & Depth Gate:** `140` (A: `10`, B: `14`, C: `116`)
* **Passed Strike-vs-Oracle Tail Gate:** `132` (A: `2`, B: `14`, C: `116`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXHIGHLAX-26NOV14-B73.5`](https://kalshi.com/markets/kxhighlax-26nov14) — Will the maximum temperature be 73-74° on Nov 14, 2026? (73° to 74°)  
  * **Action:** Buy No (Limit) @ **83c** x **63 contracts** (Risk `$52.29` to win `$10.71` / `+20.48%`)  
  * **Book:** Yes Bid `16c` / No Bid `82c` | Spread `2c` | Book Depth `12146` | Expires `47.36h`  
  * **Oracle Proof:** NWS KLAX forecast high (2026-11-14) is 70.0F; bracket 73.0F-74.0F sits +3.0F above forecast.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXAAAGASCDDE-26NOV14-LD`](https://kalshi.com/markets/kxaaagascdde-26nov14) — Will gas prices show a large decrease? (Large decrease)  
  * **Action:** Buy No (Limit) @ **85c** x **62 contracts** (Risk `$52.70` to win `$9.30` / `+17.65%`)  
  * **Book:** Yes Bid `12c` / No Bid `84c` | Spread `4c` | Book Depth `1084` | Expires `18.36h`  
  * **Oracle Proof:** Tail longshot bid at 12c Yes (mutually exclusive event modal peak 67c Yes across 5 slices); 4c spread.
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXUEFANLGAME-26NOV17WALPOR-TIE`](https://kalshi.com/markets/kxuefanlgame-26nov17walpor) — Tie is the result (Tie)  
  * **Action:** Buy No (Limit) @ **82c** x **64 contracts** (Risk `$52.48` to win `$11.52` / `+21.95%`)  
  * **Book:** Yes Bid `16c` / No Bid `81c` | Spread `3c` | Book Depth `55040` | Expires `98.11h`  
  * **Oracle Proof:** Independent longshot bid at 16c Yes (81c No bid, 3c two-sided spread across 3 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXHIGHLAX-26NOV14-B73.5](https://kalshi.com/markets/kxhighlax-26nov14) | BUCKET_A_WEATHER_ATMOSPHERIC | 16c | 82c | **83c** | **63** (`$52.29`) | 2c | 12146 | +20.48% | 47.36h |
| 2 | [KXLOWTNYC-26NOV14-B34.5](https://kalshi.com/markets/kxlowtnyc-26nov14) | BUCKET_A_WEATHER_ATMOSPHERIC | 3c | 94c | **95c** | **55** (`$52.25`) | 3c | 3152 | +5.26% | 47.36h |
| 3 | [KXAAAGASCDDE-26NOV14-LD](https://kalshi.com/markets/kxaaagascdde-26nov14) | BUCKET_B_MACRO_ENERGY_COMMODITY | 12c | 84c | **85c** | **62** (`$52.70`) | 4c | 1084 | +17.65% | 18.36h |
| 4 | [KXAAAGASCDHI-26NOV14-LD](https://kalshi.com/markets/kxaaagascdhi-26nov14) | BUCKET_B_MACRO_ENERGY_COMMODITY | 8c | 90c | **91c** | **58** (`$52.78`) | 2c | 1187 | +9.89% | 18.36h |
| 5 | [KXWTI-26NOV1614-T91.49](https://kalshi.com/markets/kxwti-26nov1614) | BUCKET_B_MACRO_ENERGY_COMMODITY | 11c | 87c | **88c** | **60** (`$52.80`) | 2c | 29740 | +13.64% | 70.86h |
| 6 | [KXAAAGASCDCT-26NOV14-SD](https://kalshi.com/markets/kxaaagascdct-26nov14) | BUCKET_B_MACRO_ENERGY_COMMODITY | 4c | 94c | **95c** | **55** (`$52.25`) | 2c | 4863 | +5.26% | 18.36h |
| 7 | [KXWTI-26NOV1614-T91.99](https://kalshi.com/markets/kxwti-26nov1614) | BUCKET_B_MACRO_ENERGY_COMMODITY | 7c | 90c | **91c** | **58** (`$52.78`) | 3c | 27069 | +9.89% | 70.86h |
| 8 | [KXGBPUSDEVENT-20NOV260300-T13300](https://kalshi.com/markets/kxgbpusdevent-20nov260300) | BUCKET_B_MACRO_ENERGY_COMMODITY | 13c | 81c | **82c** | **64** (`$52.48`) | 6c | 10754 | +21.95% | 155.36h |
| 9 | [KXUSDCADEVENT-20NOV260930-T14350](https://kalshi.com/markets/kxusdcadevent-20nov260930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 11c | 82c | **83c** | **63** (`$52.29`) | 7c | 12752 | +20.48% | 161.86h |
| 10 | [KXGBPUSDEVENT-20NOV260300-T13325](https://kalshi.com/markets/kxgbpusdevent-20nov260300) | BUCKET_B_MACRO_ENERGY_COMMODITY | 8c | 86c | **87c** | **60** (`$52.20`) | 6c | 14329 | +14.94% | 155.36h |
| 11 | [KXUEFANLGAME-26NOV17WALPOR-TIE](https://kalshi.com/markets/kxuefanlgame-26nov17walpor) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **64** (`$52.48`) | 3c | 55040 | +21.95% | 98.11h |
| 12 | [KXCOLLECTIONSALE-KOONS-17NOV26-150000000](https://kalshi.com/markets/kxcollectionsale-koons-17nov26) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 82c | **83c** | **63** (`$52.29`) | 2c | 14315 | +20.48% | 104.36h |
| 13 | [KXCOPPEREVENT-18NOV261330-T630000](https://kalshi.com/markets/kxcopperevent-18nov261330) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **64** (`$52.48`) | 4c | 7551 | +21.95% | 117.86h |
| 14 | [KXCOPPEREVENT-18NOV261430-T630000](https://kalshi.com/markets/kxcopperevent-18nov261430) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **64** (`$52.48`) | 4c | 8533 | +21.95% | 118.86h |
| 15 | [KXUEFANLSPREAD-26NOV16SUISCO-SUI3](https://kalshi.com/markets/kxuefanlspread-26nov16suisco) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 84c | **85c** | **62** (`$52.70`) | 2c | 65650 | +17.65% | 75.11h |
| 16 | [KXPERLIGA1GAME-26NOV16MOQCAG-CAG](https://kalshi.com/markets/kxperliga1game-26nov16moqcag) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **61** (`$52.46`) | 2c | 25869 | +16.28% | 74.61h |
| 17 | [KXUEFANLGAME-26NOV17ISRAUT-ISR](https://kalshi.com/markets/kxuefanlgame-26nov17israut) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 80c | **82c** | **64** (`$52.48`) | 6c | 71770 | +21.95% | 98.11h |
| 18 | [KXAPRPOTUS-26NOV20-37.8](https://kalshi.com/markets/kxaprpotus-26nov20) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 80c | **82c** | **64** (`$52.48`) | 5c | 23699 | +21.95% | 163.36h |
| 19 | [KXUEFANLTEAMTOTAL-26NOV15BLRALB-ALB3](https://kalshi.com/markets/kxuefanlteamtotal-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 81c | **82c** | **64** (`$52.48`) | 7c | 25183 | +21.95% | 47.36h |
| 20 | [KXGOLDEVENT-17NOV261830-T395000](https://kalshi.com/markets/kxgoldevent-17nov261830) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 82c | **83c** | **63** (`$52.29`) | 5c | 8846 | +20.48% | 98.86h |
| 21 | [KXURYPDGAME-26NOV15DEFPEN-DEF](https://kalshi.com/markets/kxurypdgame-26nov15defpen) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **63** (`$52.29`) | 4c | 38949 | +20.48% | 53.36h |
| 22 | [KXUSLTOTAL-26NOV15NEWSRP-5](https://kalshi.com/markets/kxusltotal-26nov15newsrp) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 10c | 87c | **88c** | **60** (`$52.80`) | 3c | 4145 | +13.64% | 55.36h |
| 23 | [KXUEFANLSCORE-26NOV15BLRALB-BLR0ALB1](https://kalshi.com/markets/kxuefanlscore-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 86c | **87c** | **60** (`$52.20`) | 2c | 9843 | +14.94% | 47.36h |
| 24 | [KXCOPPEREVENT-17NOV261830-T630000](https://kalshi.com/markets/kxcopperevent-17nov261830) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 83c | **84c** | **63** (`$52.92`) | 5c | 12124 | +19.05% | 98.86h |
| 25 | [KXAPRPOTUS-26NOV20-38.0](https://kalshi.com/markets/kxaprpotus-26nov20) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 83c | **84c** | **63** (`$52.92`) | 4c | 26433 | +19.05% | 163.36h |
