# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-13T18:46:37.742721+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `LIVE_KALSHI_PORTFOLIO_API (Live=$1016.18; SizingFloor=$200.00)`
* **Effective Sizing Bankroll:** `$1016.18`
* **Max Dollar Risk Per Pick (5% Cap):** `$50.81` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$152.43`
* **Dry Powder Reserve (85% Min):** `$863.75`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `9476`
* **In Expiration Window (8h - 168h):** `2759` (Bucket A: `109`, Bucket B: `195`, Bucket C: `2455`)
* **Passed Preliminary Two-Sided Quote Gate:** `246` (A: `29`, B: `36`, C: `181`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `246`
* **Passed Bucket Spread & Depth Gate:** `106` (A: `11`, B: `14`, C: `81`)
* **Passed Strike-vs-Oracle Tail Gate:** `97` (A: `2`, B: `14`, C: `81`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXHIGHDEN-26NOV13-B60.5`](https://kalshi.com/markets/kxhighden-26nov13) — Will the maximum temperature be 60-61° on Nov 13, 2026? (60° to 61°)  
  * **Action:** Buy No (Limit) @ **96c** x **52 contracts** (Risk `$49.92` to win `$2.08` / `+4.17%`)  
  * **Book:** Yes Bid `3c` / No Bid `95c` | Spread `2c` | Book Depth `4861` | Expires `25.22h`  
  * **Oracle Proof:** NWS KDEN forecast high (2026-11-13) is 64.0F; bracket 60.0F-61.0F sits -3.0F below forecast.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** [`KXAAAGASCDHI-26NOV14-SD`](https://kalshi.com/markets/kxaaagascdhi-26nov14) — Will gas prices show a small decrease? (Small decrease)  
  * **Action:** Buy No (Limit) @ **82c** x **61 contracts** (Risk `$50.02` to win `$10.98` / `+21.95%`)  
  * **Book:** Yes Bid `17c` / No Bid `80c` | Spread `3c` | Book Depth `2420` | Expires `20.22h`  
  * **Oracle Proof:** Tail longshot bid at 17c Yes (mutually exclusive event modal peak 33c Yes across 5 slices); 3c spread.
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXUEFANLTOTAL-26NOV16MKDSLO-4`](https://kalshi.com/markets/kxuefanltotal-26nov16mkdslo) — Will over 3.5 goals be scored? (Over 3.5 goals scored)  
  * **Action:** Buy No (Limit) @ **82c** x **61 contracts** (Risk `$50.02` to win `$10.98` / `+21.95%`)  
  * **Book:** Yes Bid `17c` / No Bid `81c` | Spread `2c` | Book Depth `58511` | Expires `76.97h`  
  * **Oracle Proof:** Independent longshot bid at 17c Yes (81c No bid, 2c two-sided spread across 6 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXHIGHDEN-26NOV13-B60.5](https://kalshi.com/markets/kxhighden-26nov13) | BUCKET_A_WEATHER_ATMOSPHERIC | 3c | 95c | **96c** | **52** (`$49.92`) | 2c | 4861 | +4.17% | 25.22h |
| 2 | [KXLOWTCHI-26NOV14-B29.5](https://kalshi.com/markets/kxlowtchi-26nov14) | BUCKET_A_WEATHER_ATMOSPHERIC | 7c | 80c | **82c** | **61** (`$50.02`) | 13c | 2854 | +21.95% | 49.22h |
| 3 | [KXAAAGASCDHI-26NOV14-SD](https://kalshi.com/markets/kxaaagascdhi-26nov14) | BUCKET_B_MACRO_ENERGY_COMMODITY | 17c | 80c | **82c** | **61** (`$50.02`) | 3c | 2420 | +21.95% | 20.22h |
| 4 | [KXAAAGASCDDE-26NOV14-MC](https://kalshi.com/markets/kxaaagascdde-26nov14) | BUCKET_B_MACRO_ENERGY_COMMODITY | 14c | 83c | **84c** | **60** (`$50.40`) | 3c | 4452 | +19.05% | 20.22h |
| 5 | [KXWTI-26NOV1614-T91.49](https://kalshi.com/markets/kxwti-26nov1614) | BUCKET_B_MACRO_ENERGY_COMMODITY | 12c | 84c | **85c** | **59** (`$50.15`) | 4c | 24870 | +17.65% | 72.72h |
| 6 | [KXGBPUSDEVENT-20NOV260300-T13300](https://kalshi.com/markets/kxgbpusdevent-20nov260300) | BUCKET_B_MACRO_ENERGY_COMMODITY | 13c | 80c | **82c** | **61** (`$50.02`) | 7c | 6327 | +21.95% | 157.22h |
| 7 | [KXAAAGASCDCT-26NOV14-SD](https://kalshi.com/markets/kxaaagascdct-26nov14) | BUCKET_B_MACRO_ENERGY_COMMODITY | 3c | 95c | **96c** | **52** (`$49.92`) | 2c | 2381 | +4.17% | 20.22h |
| 8 | [KXUSDJPYEVENT-19NOV261930-T16100](https://kalshi.com/markets/kxusdjpyevent-19nov261930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 12c | 80c | **82c** | **61** (`$50.02`) | 8c | 5939 | +21.95% | 149.72h |
| 9 | [KXWTI-26NOV1614-T91.99](https://kalshi.com/markets/kxwti-26nov1614) | BUCKET_B_MACRO_ENERGY_COMMODITY | 8c | 88c | **89c** | **57** (`$50.73`) | 4c | 25042 | +12.36% | 72.72h |
| 10 | [KXUSDCADEVENT-20NOV260930-T14350](https://kalshi.com/markets/kxusdcadevent-20nov260930) | BUCKET_B_MACRO_ENERGY_COMMODITY | 10c | 82c | **83c** | **61** (`$50.63`) | 8c | 3796 | +20.48% | 163.72h |
| 11 | [KXUEFANLTOTAL-26NOV16MKDSLO-4](https://kalshi.com/markets/kxuefanltotal-26nov16mkdslo) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 81c | **82c** | **61** (`$50.02`) | 2c | 58511 | +21.95% | 76.97h |
| 12 | [KXSERIECGAME-26NOV16PCSTOR-TOR](https://kalshi.com/markets/kxseriecgame-26nov16pcstor) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **61** (`$50.02`) | 4c | 10729 | +21.95% | 75.97h |
| 13 | [KXUEFANLGAME-26NOV17WALPOR-TIE](https://kalshi.com/markets/kxuefanlgame-26nov17walpor) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **61** (`$50.02`) | 4c | 54709 | +21.95% | 99.97h |
| 14 | [KXGOLDEVENT-17NOV261830-T395000](https://kalshi.com/markets/kxgoldevent-17nov261830) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **61** (`$50.02`) | 4c | 3576 | +21.95% | 100.72h |
| 15 | [KXPERLIGA1GAME-26NOV16MOQCAG-CAG](https://kalshi.com/markets/kxperliga1game-26nov16moqcag) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **59** (`$50.74`) | 2c | 23248 | +16.28% | 76.47h |
| 16 | [KXUEFANLSPREAD-26NOV16SUISCO-SUI3](https://kalshi.com/markets/kxuefanlspread-26nov16suisco) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **61** (`$50.63`) | 3c | 73864 | +20.48% | 76.97h |
| 17 | [KXCOPPEREVENT-17NOV261830-T630000](https://kalshi.com/markets/kxcopperevent-17nov261830) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **61** (`$50.63`) | 4c | 4284 | +20.48% | 100.72h |
| 18 | [KXAPRPOTUS-26NOV20-37.8](https://kalshi.com/markets/kxaprpotus-26nov20) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 80c | **82c** | **61** (`$50.02`) | 5c | 23832 | +21.95% | 165.22h |
| 19 | [KXUEFANLSCORE-26NOV15BLRALB-BLR0ALB1](https://kalshi.com/markets/kxuefanlscore-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 85c | **86c** | **59** (`$50.74`) | 3c | 7988 | +16.28% | 49.22h |
| 20 | [KXUEFANLGAME-26NOV16MKDSLO-MKD](https://kalshi.com/markets/kxuefanlgame-26nov16mkdslo) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 84c | **85c** | **59** (`$50.15`) | 2c | 93275 | +17.65% | 75.97h |
| 21 | [KXUEFANLSCORE-26NOV15BLRALB-BLR1ALB1](https://kalshi.com/markets/kxuefanlscore-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 84c | **85c** | **59** (`$50.15`) | 4c | 8066 | +17.65% | 49.22h |
| 22 | [KXURYPDGAME-26NOV15DEFPEN-DEF](https://kalshi.com/markets/kxurypdgame-26nov15defpen) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **61** (`$50.63`) | 4c | 38519 | +20.48% | 55.22h |
| 23 | [KXUSLTOTAL-26NOV15NEWSRP-5](https://kalshi.com/markets/kxusltotal-26nov15newsrp) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 10c | 87c | **88c** | **57** (`$50.16`) | 3c | 4725 | +13.64% | 57.22h |
| 24 | [KXUEFANLGAME-26NOV17ISRAUT-ISR](https://kalshi.com/markets/kxuefanlgame-26nov17israut) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 80c | **82c** | **61** (`$50.02`) | 7c | 71514 | +21.95% | 99.97h |
| 25 | [KXAPRPOTUS-26NOV20-38.0](https://kalshi.com/markets/kxaprpotus-26nov20) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 83c | **84c** | **60** (`$50.40`) | 5c | 26421 | +19.05% | 165.22h |
