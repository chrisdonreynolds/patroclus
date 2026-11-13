# Patroclus Kalshi Longshot-Bias Underwriting Snapshot

- **Generated Timestamp (UTC):** `2026-11-13T06:19:46.978220+00:00`
- **Repository:** [https://github.com/chrisdonreynolds/patroclus](https://github.com/chrisdonreynolds/patroclus)
- **Live Raw JSON Feed:** [https://raw.githubusercontent.com/chrisdonreynolds/patroclus/main/kalshi_snapshot.json](https://raw.githubusercontent.com/chrisdonreynolds/patroclus/main/kalshi_snapshot.json)
- **Outbound User-Agent:** `PatroclusKalshiScanner/1.0 (christopherdonreynolds@gmail.com)`
- **Execution Mode:** Manual Kalshi Mobile App Execution Only (`READ-ONLY API`)

## 1. Live Kalshi Portfolio Bankroll & Fractional Kelly Cap

- **Balance Data Source:** `LIVE_KALSHI_PORTFOLIO_API (Live=$0.02; SizingFloor=$200.00)` (Queried [https://external-api.kalshi.com/trade-api/v2/portfolio/balance](https://external-api.kalshi.com/trade-api/v2/portfolio/balance))
- **Available Cash Reported:** `$0.02` (`2` cents)
- **Portfolio Value Reported:** `$0.00` (`0` cents)
- **Effective Sizing Bankroll:** **`$200.00`** (`used_minimum_sizing_floor=True`)
- **5% Single-Pick Allocation Cap (`max_dollar_risk_5pct`):** **`$10.00`**
- **Max Daily Deployment (3 Uncorrelated Picks = 15%):** **`$30.00`**
- **Mandatory Dry Powder Reserve (85%):** **`$170.00`**

> **Kelly Asymmetry Warning:** Because an 86¢ `No` contract carries a **6.14-to-1 payoff asymmetry** (where 1 loss wipes out 6.14 wins, and every 1% drop in true win rate slashes optimal Kelly allocation by 7.14%), total daily exposure must be strictly capped at **3 uncorrelated picks (15% total bankroll deployed)** while keeping **85% in dry powder**.

## 2. Broad Market Harvesting Summary

- **Open Markets Scanned:** `2400` across `12` paginated API batches
- **Markets in Target Expiration Window:** `1803`
- **Uncrowded Longshot Candidates Exported:** `25`

## 3. Top Uncrowded Maker 'No' Underwriting Candidates

| Rank | Ticker | Bucket | Rec. Maker No Bid | Contracts (5% Cap) | Spread (¢) | Top No Queue | OBI | Event Overround | Net Return % | Hours Left |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `KXMVECROSSCATEGORY-S20266DXGRR3OB5XCY4TS-3Q45ZC2CC` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **83¢** | **12** (`$9.96`) | 18¢ | 0 | +0.00 | 1.00 | +20.48% | 19.42h |
| 2 | `KXMVECROSSCATEGORY-S202634KGJATYRRN4LKOW-4MBZK4EHW` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **84¢** | **11** (`$9.24`) | 17¢ | 0 | +0.00 | 1.00 | +19.05% | 19.42h |
| 3 | `KXMVECROSSCATEGORY-S2026HGVY75APCCII5F6V-YFPOUHV6Y` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **84¢** | **11** (`$9.24`) | 17¢ | 0 | +0.00 | 1.00 | +19.05% | 44.17h |
| 4 | `KXMVECROSSCATEGORY-S2026MA35YGUTBOJ464YS-BYG5IMEDA` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **84¢** | **11** (`$9.24`) | 17¢ | 0 | +0.00 | 1.00 | +19.05% | 26.67h |
| 5 | `KXMVECROSSCATEGORY-S2026XE6XD274UUISHA4Q-DMXXPAN6F` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **85¢** | **11** (`$9.35`) | 16¢ | 0 | +0.00 | 1.00 | +17.65% | 26.17h |
| 6 | `KXMVECROSSCATEGORY-S2026INTJREGC6YPAIPBD-WT4NMY4QZ` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **85¢** | **11** (`$9.35`) | 16¢ | 0 | +0.00 | 1.00 | +17.65% | 27.17h |
| 7 | `KXMVECROSSCATEGORY-S2026JMFLYAP6YPRKUGZJ-5KQWDKFQS` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **85¢** | **11** (`$9.35`) | 16¢ | 0 | +0.00 | 1.00 | +17.65% | 50.17h |
| 8 | `KXMVECROSSCATEGORY-S2026FS7BVDKTY72WWAP6-4QJEZ6KEL` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **85¢** | **11** (`$9.35`) | 16¢ | 0 | +0.00 | 1.00 | +17.65% | 29.17h |
| 9 | `KXMVECROSSCATEGORY-S2026BKXTWBIZBXAH3XNH-KCT56ONUU` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **86¢** | **11** (`$9.46`) | 15¢ | 0 | +0.00 | 1.00 | +16.28% | 27.17h |
| 10 | `KXMVECROSSCATEGORY-S2026GRK2ZC4LEIGV3IXW-5WWTKLB7R` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **86¢** | **11** (`$9.46`) | 15¢ | 0 | +0.00 | 1.00 | +16.28% | 38.67h |
| 11 | `KXMVECROSSCATEGORY-S2026AJ2IPPQV7AGYGIBI-EGBYYWCCP` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **86¢** | **11** (`$9.46`) | 15¢ | 0 | +0.00 | 1.00 | +16.28% | 20.84h |
| 12 | `KXMVECROSSCATEGORY-S2026U6GEU6RSYE4T6CJX-SSTYKI7JX` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **86¢** | **11** (`$9.46`) | 15¢ | 0 | +0.00 | 1.00 | +16.28% | 27.17h |
| 13 | `KXMVECROSSCATEGORY-S2026GGBWZHXB42RUV5R3-K6WDIL45G` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **87¢** | **11** (`$9.57`) | 14¢ | 0 | +0.00 | 1.00 | +14.94% | 49.67h |
| 14 | `KXMVECROSSCATEGORY-S2026BEI26RCYSZP4ECK4-BCH7SIBKR` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **87¢** | **11** (`$9.57`) | 14¢ | 0 | +0.00 | 1.00 | +14.94% | 23.67h |
| 15 | `KXMVECROSSCATEGORY-S2026BT5JVL5Z6VZBEH34-6GI4C6JXF` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **89¢** | **11** (`$9.79`) | 12¢ | 0 | +0.00 | 1.00 | +12.36% | 43.67h |
| 16 | `KXMVECROSSCATEGORY-S2026H5ERW5R7O7443J7G-QH2SV2HYZ` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **89¢** | **11** (`$9.79`) | 12¢ | 0 | +0.00 | 1.00 | +12.36% | 27.17h |
| 17 | `KXMVECROSSCATEGORY-S2026QW4WYL4HFAP7FJ6P-C3JGTGY7R` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **89¢** | **11** (`$9.79`) | 12¢ | 0 | +0.00 | 1.00 | +12.36% | 23.67h |
| 18 | `KXMVECROSSCATEGORY-S2026SZOS4IUNLLOMYNK3-RGOMHVYHD` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **90¢** | **11** (`$9.90`) | 11¢ | 0 | +0.00 | 1.00 | +11.11% | 23.67h |
| 19 | `KXMVECROSSCATEGORY-S2026LILNKIJNAPKSL7B5-VEW4THMDE` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **90¢** | **11** (`$9.90`) | 11¢ | 0 | +0.00 | 1.00 | +11.11% | 27.17h |
| 20 | `KXMVECROSSCATEGORY-S2026FWQUIXUFJDDQPYXK-WJJWCWWTR` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **90¢** | **11** (`$9.90`) | 11¢ | 0 | +0.00 | 1.00 | +11.11% | 19.42h |
| 21 | `KXMVECROSSCATEGORY-S2026WBBTPQIS6BWU3EUT-3NQKP6GBU` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **91¢** | **10** (`$9.10`) | 10¢ | 0 | +0.00 | 1.00 | +9.89% | 26.17h |
| 22 | `KXMVECROSSCATEGORY-S2026KVM7PADKAQ56KS24-Z22TERTIQ` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **91¢** | **10** (`$9.10`) | 10¢ | 0 | +0.00 | 1.00 | +9.89% | 27.17h |
| 23 | `KXMVECROSSCATEGORY-S2026MWPTFGOUG7NINPRD-FT7OTSFFR` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **91¢** | **10** (`$9.10`) | 10¢ | 0 | +0.00 | 1.00 | +9.89% | 19.42h |
| 24 | `KXMVECROSSCATEGORY-S2026QL4VJTAJ3Y4VMVS3-G2IZP37IH` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **92¢** | **10** (`$9.20`) | 9¢ | 0 | +0.00 | 1.00 | +8.70% | 19.42h |
| 25 | `KXMVECROSSCATEGORY-S2026ENKK3QTKC5L7I252-YQ2ULCJXT` | `BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE` | **92¢** | **10** (`$9.20`) | 9¢ | 0 | +0.00 | 1.00 | +8.70% | 49.17h |

## 4. Primary Truth Feed Summary

- **Vertical 1 (SEC EDGAR 8-K/10-Q & Fed Speeches):** `{"artificial intelligence": 2504, "tariff": 1694, "recession": 1094, "disinflation": 2}`
- **Vertical 2 (Federal Register & Congressional Clocks):** Weekend/Recess Brake = `True`
- **Vertical 3 (Launch Library 2 & TSA Throughput):** 7-Day Avg TSA Passengers = `None`
- **Vertical 6 (NWS Weather Grids & METAR Trap):** Tracked `8` Kalshi settlement airport stations
- **Vertical 7 (AAA National Gas & EIA):** `{"current_regular_avg": 3.9081, "yesterday_regular_avg": 3.9081, "week_ago_regular_avg": 4.1999, "month_ago_regular_avg": 3.9954, "daily_cent_velocity_1d": 0.0, "rolling_3d_estimated_cent_velocity_per_day": -1.668}`
