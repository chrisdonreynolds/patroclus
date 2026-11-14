# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.1)
**Timestamp:** `2026-11-14T12:35:59.295116+00:00`  
**Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)  

## 1. Liquid Bankroll & Kelly Sizing Guardrails
* **Balance Source:** `LIVE_KALSHI_PORTFOLIO_API (Live=$1075.59; SizingFloor=$200.00)`
* **Effective Sizing Bankroll:** `$1075.59`
* **Max Dollar Risk Per Pick (5% Cap):** `$53.78` (auto-capped at `<=35%` of visible book depth on thin markets)
* **Max Daily Deployed Capital (15% Max):** `$161.34`
* **Dry Powder Reserve (85% Min):** `$914.25`

## 2. Scanner Diagnostics Funnel (v3.1 Per-Bucket Telemetry)
* **Open Non-Parlay Markets Scanned:** `11577`
* **In Expiration Window (8h - 168h):** `4433` (Bucket A: `55`, Bucket B: `127`, Bucket C: `4251`)
* **Passed Preliminary Two-Sided Quote Gate:** `616` (A: `10`, B: `28`, C: `578`)
* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `616`
* **Passed Bucket Spread & Depth Gate:** `142` (A: `4`, B: `0`, C: `138`)
* **Passed Strike-vs-Oracle Tail Gate:** `139` (A: `1`, B: `0`, C: `138`)

## 3. Top 3 Orthogonal Picks (1 Per Bucket)
* **BUCKET_A_WEATHER_ATMOSPHERIC:** [`KXHIGHLAX-26NOV14-B73.5`](https://kalshi.com/markets/kxhighlax-26nov14) — Will the maximum temperature be 73-74° on Nov 14, 2026? (73° to 74°)  
  * **Action:** Buy No (Limit) @ **87c** x **61 contracts** (Risk `$53.07` to win `$7.93` / `+14.94%`)  
  * **Book:** Yes Bid `12c` / No Bid `86c` | Spread `2c` | Book Depth `11529` | Expires `31.4h`  
  * **Oracle Proof:** NWS KLAX forecast high (2026-11-14) is 70.0F; bracket 73.0F-74.0F sits +3.0F above forecast.
* **BUCKET_B_MACRO_ENERGY_COMMODITY:** `SKIP BUCKET` — No contract currently meets bucket spread, book depth, and oracle tail distance gates.
* **BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE:** [`KXRT-HOWT-35`](https://kalshi.com/markets/kxrt-howt) — How to Rob a Bank Rotten Tomatoes score? (Above 35)  
  * **Action:** Buy No (Limit) @ **82c** x **65 contracts** (Risk `$53.30` to win `$11.70` / `+21.95%`)  
  * **Book:** Yes Bid `17c` / No Bid `81c` | Spread `2c` | Book Depth `124463` | Expires `50.4h`  
  * **Oracle Proof:** Independent longshot bid at 17c Yes (81c No bid, 2c two-sided spread across 16 event market(s)).

## 4. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | [KXHIGHLAX-26NOV14-B73.5](https://kalshi.com/markets/kxhighlax-26nov14) | BUCKET_A_WEATHER_ATMOSPHERIC | 12c | 86c | **87c** | **61** (`$53.07`) | 2c | 11529 | +14.94% | 31.4h |
| 2 | [KXRT-HOWT-35](https://kalshi.com/markets/kxrt-howt) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 81c | **82c** | **65** (`$53.30`) | 2c | 124463 | +21.95% | 50.4h |
| 3 | [KXGOLDEVENT-18NOV261330-T395000](https://kalshi.com/markets/kxgoldevent-18nov261330) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 17c | 80c | **82c** | **65** (`$53.30`) | 3c | 23138 | +21.95% | 101.9h |
| 4 | [KXEUROLEAGUEGAME-26NOV171300BAYZAL-BAY](https://kalshi.com/markets/kxeuroleaguegame-26nov171300bayzal) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **65** (`$53.30`) | 4c | 26348 | +21.95% | 80.4h |
| 5 | [KXCONCACAFNLGAME-26NOV15PANCUW-CUW](https://kalshi.com/markets/kxconcacafnlgame-26nov15pancuw) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 83c | **84c** | **64** (`$53.76`) | 3c | 60738 | +19.05% | 37.4h |
| 6 | [KXINTLFRIENDLYGAME-26NOV17JPNPAR-PAR](https://kalshi.com/markets/kxintlfriendlygame-26nov17jpnpar) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **65** (`$53.30`) | 4c | 70058 | +21.95% | 75.57h |
| 7 | [KXUEFANLSPREAD-26NOV17DENNOR-NOR2](https://kalshi.com/markets/kxuefanlspread-26nov17dennor) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 82c | **83c** | **64** (`$53.12`) | 2c | 48852 | +20.48% | 83.15h |
| 8 | [KXUEFANLTEAMTOTAL-26NOV15BLRALB-ALB3](https://kalshi.com/markets/kxuefanlteamtotal-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 80c | **82c** | **65** (`$53.30`) | 6c | 32098 | +21.95% | 31.4h |
| 9 | [KXUEFANLTOTAL-26NOV16GRESRB-5](https://kalshi.com/markets/kxuefanltotal-26nov16gresrb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 83c | **84c** | **64** (`$53.76`) | 2c | 154070 | +19.05% | 59.15h |
| 10 | [KXCOPPEREVENT-19NOV261330-T630000](https://kalshi.com/markets/kxcopperevent-19nov261330) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **65** (`$53.30`) | 4c | 17387 | +21.95% | 125.9h |
| 11 | [KXUEFANLGAME-26NOV17ISRAUT-ISR](https://kalshi.com/markets/kxuefanlgame-26nov17israut) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 80c | **82c** | **65** (`$53.30`) | 5c | 119773 | +21.95% | 82.15h |
| 12 | [KXUEFANLSPREAD-26NOV16ESTBUL-EST2](https://kalshi.com/markets/kxuefanlspread-26nov16estbul) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 82c | **83c** | **64** (`$53.12`) | 3c | 42743 | +20.48% | 56.4h |
| 13 | [KXUEFANLTOTAL-26NOV16ESTBUL-4](https://kalshi.com/markets/kxuefanltotal-26nov16estbul) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 84c | **85c** | **63** (`$53.55`) | 3c | 67726 | +17.65% | 56.4h |
| 14 | [KXUEFANLSCORE-26NOV15BLRALB-BLR0ALB1](https://kalshi.com/markets/kxuefanlscore-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **62** (`$53.32`) | 2c | 12037 | +16.28% | 31.4h |
| 15 | [KXAPRPOTUS-26NOV20-37.8](https://kalshi.com/markets/kxaprpotus-26nov20) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 81c | **82c** | **65** (`$53.30`) | 3c | 29868 | +21.95% | 147.4h |
| 16 | [KXPERLIGA1GAME-26NOV16MOQCAG-CAG](https://kalshi.com/markets/kxperliga1game-26nov16moqcag) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **62** (`$53.32`) | 2c | 28163 | +16.28% | 58.65h |
| 17 | [KXUEFANLSPREAD-26NOV16GERNED-GER3](https://kalshi.com/markets/kxuefanlspread-26nov16gerned) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 85c | **86c** | **62** (`$53.32`) | 2c | 73471 | +16.28% | 59.15h |
| 18 | [KXCOPPEREVENT-18NOV261330-T630000](https://kalshi.com/markets/kxcopperevent-18nov261330) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 83c | **84c** | **64** (`$53.76`) | 4c | 20778 | +19.05% | 101.9h |
| 19 | [KXUEFANLSPREAD-26NOV16GIBMLT-MLT3](https://kalshi.com/markets/kxuefanlspread-26nov16gibmlt) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 82c | **83c** | **64** (`$53.12`) | 4c | 18184 | +20.48% | 59.15h |
| 20 | [KXCOPPEREVENT-18NOV261430-T630000](https://kalshi.com/markets/kxcopperevent-18nov261430) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 13c | 83c | **84c** | **64** (`$53.76`) | 4c | 20387 | +19.05% | 102.9h |
| 21 | [KXUEFANLTOTAL-26NOV16ISLLUX-5](https://kalshi.com/markets/kxuefanltotal-26nov16isllux) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 83c | **84c** | **64** (`$53.76`) | 5c | 37595 | +19.05% | 56.4h |
| 22 | [KXCOLLECTIONSALE-KOCH-20NOV26-60000000](https://kalshi.com/markets/kxcollectionsale-koch-20nov26) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 16c | 80c | **82c** | **65** (`$53.30`) | 4c | 13634 | +21.95% | 160.4h |
| 23 | [KXUEFANLSCORE-26NOV15BLRALB-BLR1ALB1](https://kalshi.com/markets/kxuefanlscore-26nov15blralb) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 12c | 86c | **87c** | **61** (`$53.07`) | 2c | 10781 | +14.94% | 31.4h |
| 24 | [KXCOLLECTIONSALE-KOONS-17NOV26-150000000](https://kalshi.com/markets/kxcollectionsale-koons-17nov26) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 14c | 81c | **82c** | **65** (`$53.30`) | 5c | 13865 | +21.95% | 88.4h |
| 25 | [KXLALIGA2GAME-26NOV16ALBRCC-RCC](https://kalshi.com/markets/kxlaliga2game-26nov16albrcc) | BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE | 15c | 81c | **82c** | **65** (`$53.30`) | 4c | 29173 | +21.95% | 57.9h |
