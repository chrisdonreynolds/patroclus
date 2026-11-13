#!/usr/bin/env python3
"""
Patroclus Kalshi Longshot-Bias Underwriting Scanner (v3.0)
Repository: https://github.com/chrisdonreynolds/patroclus

All 5 Production Fixes in v3.0:
1. Kalshi API v2 Wire-Format & Fixed-Point Schema Compatibility:
   - Passes repeated `?tickers=A&tickers=B` list params (`params={"tickers": chunk}`)
     instead of comma-joined strings on `GET /markets/orderbooks`.
   - Unwraps `orderbook_fp` (`yes_dollars` / `no_dollars` fixed-point strings) as well
     as legacy `orderbook` arrays, and prioritizes `*_dollars` / `*_fp` fields when
     legacy integer fields return `0` or `None`.
2. Event-First Non-Parlay Discovery (`GET /events?status=open&with_nested_markets=true`):
   - Automatically excludes `KXMVE*` multivariate combo parlays on Kalshi's server,
     captures event-level `category` and `mutually_exclusive` flags, and excludes Sports.
3. Explicit Strike-vs-Oracle Tail Enforcement:
   - Compares `strike_type` (`greater`, `less`, `between`), `floor_strike`, and `cap_strike`
     directly against date-matched NWS hourly forecast highs/lows (`>= 3.5F` buffer +
     Midnight Clocks Trap check on same-day markets) and AAA national regular gas averages,
     plus a Distribution Tail Gate rejecting modal center brackets on multi-slice ladders.
4. Horizon & Schedule Alignment (`8h` to `168h` Expiration Window):
   - Captures next-day weather (`~38h`) alongside weekly Macro/Gas/TSA/Entertainment
     contracts (`96h-168h`) with a capital-velocity score bonus for faster settlement.
5. Bankroll Book-Depth Participation Cap (for $1,000+ Live Balances):
   - Requires minimum market activity (`volume_24h`, `open_interest`, and resting book depth)
     and caps any single Maker order at `<= 35%` of visible orderbook depth (up to the 5%
     bankroll cap) so $50+ orders never become the entire resting market.
"""

import base64
import datetime as dt
import json
import math
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

import requests

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    CRYPTO_AVAILABLE = True
except Exception:
    CRYPTO_AVAILABLE = False

USER_AGENT = "PatroclusKalshiScanner/3.0 (christopherdonreynolds@gmail.com)"
KALSHI_BASE_URL = "https://external-api.kalshi.com/trade-api/v2"
KALSHI_EVENTS_URL = f"{KALSHI_BASE_URL}/events"
KALSHI_MARKETS_URL = f"{KALSHI_BASE_URL}/markets"
KALSHI_ORDERBOOKS_BATCH_URL = f"{KALSHI_BASE_URL}/markets/orderbooks"
KALSHI_BALANCE_URL = f"{KALSHI_BASE_URL}/portfolio/balance"

MINIMUM_SIZING_FLOOR_DOLLARS = 200.0
SINGLE_PICK_RISK_CAP_PCT = 0.05
DAILY_TOTAL_RISK_CAP_PCT = 0.15

# Expiration Window (8h to 168h = 7 days)
MIN_HOURS_TO_EXPIRATION = 8.0
MAX_HOURS_TO_EXPIRATION = 168.0

# Two-Sided Longshot Microstructure Gates (Zero 99c/1c or 0-bid ghost books)
MIN_YES_BID_CENTS = 2          # Real resting Yes buyers >= 2c
MAX_YES_BID_CENTS = 17         # Longshot ceiling on Yes bid
MIN_NO_BID_CENTS = 81          # Ensures recommended_maker_no_bid_cents >= 82c
MAX_NO_BID_CENTS = 95          # Ensures recommended_maker_no_bid_cents <= 96c (never 99c/1c)
MIN_SPREAD_CENTS = 2           # Minimum 2c spread so +1c Maker improvement never crosses book
MAX_SPREAD_CENTS = 15          # Reject hollow/abandoned books wider than 15c
MAX_TOP_NO_QUEUE_DEPTH = 2000  # Avoid congested institutional walls
MAX_OBI_THRESHOLD = 0.85       # Order Book Imbalance safety cap

# Liquidity & Book-Share Protection for $1,000+ Bankrolls
MIN_TOTAL_BOOK_CONTRACTS = 15
MIN_ACTIVITY_CONTRACTS = 20    # Minimum open_interest or volume_24h
MAX_BOOK_DEPTH_SHARE = 0.35    # Never bid more than 35% of visible resting book depth

# Weather & AAA Gas Oracle Buffers
WEATHER_SAFE_BUFFER_F = 3.5    # Clears +-1.8F METAR whole-degree Celsius rounding trap

TARGET_SERIES_BY_BUCKET: Dict[str, List[str]] = {
    "BUCKET_A_WEATHER_ATMOSPHERIC": [
        "KXHIGHNY",
        "KXHIGHCHI",
        "KXHIGHHOU",
        "KXHIGHDEN",
        "KXHIGHLAX",
        "KXHIGHMIA",
        "KXHIGHAUS",
        "KXHIGHPHIL",
        "KXLOWTNYC",
        "KXLOWTCHI",
    ],
    "BUCKET_B_MACRO_ENERGY_COMMODITY": [
        "KXAAAGAS",
        "KXAAAGASW",
        "KXGAS",
        "KXWTI",
        "KXCPI",
        "KXCPIYOY",
        "KXPCE",
        "KXFED",
        "KXFEDDECISION",
        "KXGDP",
        "KXJOBLESS",
    ],
    "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE": [
        "KXRTMOVIE",
        "KXRT",
        "KXSPACE",
        "KXSTARSHIP",
        "KXTSA",
        "KXSEC",
        "KXEO",
        "KXBILL",
    ],
}

EXCLUDED_TICKER_PREFIXES = (
    "KXMVE",
    "KXMVECROSSCATEGORY",
    "KXPARLAY",
    "KXCOMBO",
    "KXNBA",
    "KXNFL",
    "KXMLB",
    "KXNHL",
    "KXNCAA",
    "KXSOCCER",
    "KXUFC",
    "KXTENNIS",
    "KXPGA",
    "KXEPL",
    "KXUCL",
    "KXBTC15M",
    "KXETH15M",
    "KXDOGE",
)

EXCLUDED_CATEGORIES = {
    "sports",
}

NWS_STATIONS: Dict[str, Dict[str, Any]] = {
    "KNYC": {
        "station_id": "KNYC",
        "city": "New York Central Park",
        "lat": 40.7829,
        "lon": -73.9654,
        "tz": "America/New_York",
        "high_prefixes": ["KXHIGHNY"],
        "low_prefixes": ["KXLOWTNYC"],
    },
    "KMDW": {
        "station_id": "KMDW",
        "city": "Chicago Midway",
        "lat": 41.7868,
        "lon": -87.7522,
        "tz": "America/Chicago",
        "high_prefixes": ["KXHIGHCHI"],
        "low_prefixes": ["KXLOWTCHI"],
    },
    "KHOU": {
        "station_id": "KHOU",
        "city": "Houston Hobby",
        "lat": 29.6454,
        "lon": -95.2789,
        "tz": "America/Chicago",
        "high_prefixes": ["KXHIGHHOU"],
        "low_prefixes": ["KXLOWTHOU"],
    },
    "KDEN": {
        "station_id": "KDEN",
        "city": "Denver International",
        "lat": 39.8561,
        "lon": -104.6737,
        "tz": "America/Denver",
        "high_prefixes": ["KXHIGHDEN"],
        "low_prefixes": ["KXLOWTDEN"],
    },
    "KLAX": {
        "station_id": "KLAX",
        "city": "Los Angeles International",
        "lat": 33.9425,
        "lon": -118.4081,
        "tz": "America/Los_Angeles",
        "high_prefixes": ["KXHIGHLAX"],
        "low_prefixes": ["KXLOWTLAX"],
    },
    "KMIA": {
        "station_id": "KMIA",
        "city": "Miami International",
        "lat": 25.7959,
        "lon": -80.2870,
        "tz": "America/New_York",
        "high_prefixes": ["KXHIGHMIA"],
        "low_prefixes": ["KXLOWTMIA"],
    },
    "KAUS": {
        "station_id": "KAUS",
        "city": "Austin Bergstrom",
        "lat": 30.1975,
        "lon": -97.6664,
        "tz": "America/Chicago",
        "high_prefixes": ["KXHIGHAUS"],
        "low_prefixes": ["KXLOWTAUS"],
    },
    "KPHL": {
        "station_id": "KPHL",
        "city": "Philadelphia International",
        "lat": 39.8744,
        "lon": -75.2424,
        "tz": "America/New_York",
        "high_prefixes": ["KXHIGHPHIL"],
        "low_prefixes": ["KXLOWTPHIL"],
    },
}

MONTH_MAP = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}


def safe_get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 15,
) -> Optional[requests.Response]:
    merged_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        merged_headers.update(headers)
    for attempt in range(2):
        try:
            resp = requests.get(
                url, params=params, headers=merged_headers, timeout=timeout
            )
            if resp.status_code == 429 and attempt == 0:
                time.sleep(0.6)
                continue
            return resp
        except Exception:
            if attempt == 0:
                time.sleep(0.3)
    return None


def build_kalshi_auth_headers(method: str, path: str) -> Optional[Dict[str, str]]:
    access_key = os.environ.get("KALSHI_ACCESS_KEY", "").strip()
    private_key_pem = os.environ.get("KALSHI_PRIVATE_KEY", "").strip()
    if not access_key or not private_key_pem or not CRYPTO_AVAILABLE:
        return None
    try:
        if "\\n" in private_key_pem:
            private_key_pem = private_key_pem.replace("\\n", "\n")
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode("utf-8"), password=None
        )
        timestamp_ms = str(int(time.time() * 1000))
        msg_string = f"{timestamp_ms}{method.upper()}{path}"
        signature = private_key.sign(
            msg_string.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_LENGTH,
            ),
            hashes.SHA256(),
        )
        sig_b64 = base64.b64encode(signature).decode("utf-8")
        return {
            "KALSHI-ACCESS-KEY": access_key,
            "KALSHI-ACCESS-SIGNATURE": sig_b64,
            "KALSHI-ACCESS-TIMESTAMP": timestamp_ms,
        }
    except Exception:
        return None


def fetch_bankroll_and_sizing() -> Dict[str, Any]:
    path = "/trade-api/v2/portfolio/balance"
    auth_headers = build_kalshi_auth_headers("GET", path)
    available_cash_cents = 0
    portfolio_value_cents = 0
    authenticated = False

    if auth_headers:
        resp = safe_get(KALSHI_BALANCE_URL, headers=auth_headers, timeout=12)
        if resp is not None and resp.status_code == 200:
            data = resp.json()
            if data.get("balance_dollars") is not None:
                available_cash_cents = int(
                    round(float(data["balance_dollars"]) * 100.0)
                )
            else:
                available_cash_cents = int(round(float(data.get("balance", 0) or 0)))

            if data.get("portfolio_value_dollars") is not None:
                portfolio_value_cents = int(
                    round(float(data["portfolio_value_dollars"]) * 100.0)
                )
            else:
                portfolio_value_cents = int(
                    round(float(data.get("portfolio_value", 0) or 0))
                )
            authenticated = True

    avail_dollars = round(available_cash_cents / 100.0, 2)
    port_dollars = round(portfolio_value_cents / 100.0, 2)
    live_total = round(avail_dollars + port_dollars, 2)

    used_floor = live_total < MINIMUM_SIZING_FLOOR_DOLLARS
    effective_bankroll = max(live_total, MINIMUM_SIZING_FLOOR_DOLLARS)
    max_risk_5pct = round(effective_bankroll * SINGLE_PICK_RISK_CAP_PCT, 2)
    max_daily_15pct = round(effective_bankroll * DAILY_TOTAL_RISK_CAP_PCT, 2)
    dry_powder_85pct = round(effective_bankroll - max_daily_15pct, 2)

    return {
        "source": (
            f"LIVE_KALSHI_PORTFOLIO_API (Live=${live_total:.2f}; SizingFloor=${MINIMUM_SIZING_FLOOR_DOLLARS:.2f})"
            if authenticated
            else f"DEFAULT_SIZING_FLOOR (${MINIMUM_SIZING_FLOOR_DOLLARS:.2f})"
        ),
        "authenticated": authenticated,
        "available_cash_cents": available_cash_cents,
        "portfolio_value_cents": portfolio_value_cents,
        "available_cash_dollars": avail_dollars,
        "portfolio_value_dollars": port_dollars,
        "live_reported_bankroll_dollars": live_total,
        "used_minimum_sizing_floor": used_floor,
        "total_liquid_bankroll_dollars": effective_bankroll,
        "max_dollar_risk_5pct": max_risk_5pct,
        "max_daily_deployed_15pct": max_daily_15pct,
        "dry_powder_reserve_85pct": dry_powder_85pct,
        "endpoint_queried": KALSHI_BALANCE_URL,
    }


def fetch_weather_oracles(now_utc: dt.datetime) -> Dict[str, Any]:
    stations_out: Dict[str, Any] = {}
    for code, meta in NWS_STATIONS.items():
        tz = ZoneInfo(meta["tz"])
        today_local_str = now_utc.astimezone(tz).strftime("%Y-%m-%d")
        points_url = f"https://api.weather.gov/points/{meta['lat']},{meta['lon']}"
        obs_url = f"https://api.weather.gov/stations/{code}/observations?limit=30"
        hourly_url = None
        daily_highs_f: Dict[str, float] = {}
        daily_lows_f: Dict[str, float] = {}

        p_resp = safe_get(points_url, timeout=10)
        if p_resp is not None and p_resp.status_code == 200:
            hourly_url = p_resp.json().get("properties", {}).get("forecastHourly")
            if hourly_url:
                h_resp = safe_get(hourly_url, timeout=10)
                if h_resp is not None and h_resp.status_code == 200:
                    periods = h_resp.json().get("properties", {}).get("periods", [])
                    for p in periods[:96]:
                        st_raw = p.get("startTime")
                        t_val = p.get("temperature")
                        if not st_raw or t_val is None:
                            continue
                        try:
                            p_dt = dt.datetime.fromisoformat(
                                st_raw.replace("Z", "+00:00")
                            ).astimezone(tz)
                            d_key = p_dt.strftime("%Y-%m-%d")
                            t_f = float(t_val)
                            if d_key not in daily_highs_f or t_f > daily_highs_f[d_key]:
                                daily_highs_f[d_key] = round(t_f, 1)
                            if d_key not in daily_lows_f or t_f < daily_lows_f[d_key]:
                                daily_lows_f[d_key] = round(t_f, 1)
                        except Exception:
                            continue

        midnight_temp_f: Optional[float] = None
        observed_today_max_f: Optional[float] = None
        latest_c: Optional[float] = None
        latest_f: Optional[float] = None

        o_resp = safe_get(obs_url, timeout=10)
        if o_resp is not None and o_resp.status_code == 200:
            features = o_resp.json().get("features", [])
            for idx, feat in enumerate(features):
                props = feat.get("properties", {})
                temp_c_val = (props.get("temperature") or {}).get("value")
                ts_str = props.get("timestamp")
                if temp_c_val is None or not ts_str:
                    continue
                try:
                    temp_c_num = float(temp_c_val)
                    temp_f_num = round((temp_c_num * 9.0 / 5.0) + 32.0, 1)
                    if idx == 0:
                        latest_c = round(temp_c_num, 1)
                        latest_f = temp_f_num
                    obs_local = dt.datetime.fromisoformat(
                        ts_str.replace("Z", "+00:00")
                    ).astimezone(tz)
                    if obs_local.strftime("%Y-%m-%d") == today_local_str:
                        if (
                            observed_today_max_f is None
                            or temp_f_num > observed_today_max_f
                        ):
                            observed_today_max_f = temp_f_num
                        if 0 <= obs_local.hour <= 2:
                            if midnight_temp_f is None or temp_f_num > midnight_temp_f:
                                midnight_temp_f = temp_f_num
                except Exception:
                    continue

        today_fcst_high = daily_highs_f.get(today_local_str)
        trap_triggered = bool(
            today_fcst_high is not None
            and midnight_temp_f is not None
            and midnight_temp_f >= (today_fcst_high - 0.5)
        )

        stations_out[code] = {
            "station_id": code,
            "city": meta["city"],
            "timezone": meta["tz"],
            "today_local_date": today_local_str,
            "points_url": points_url,
            "observations_url": obs_url,
            "forecast_hourly_url": hourly_url,
            "daily_forecast_highs_f": daily_highs_f,
            "daily_forecast_lows_f": daily_lows_f,
            "hourly_forecast_peak_f": today_fcst_high,
            "observed_today_max_f": observed_today_max_f,
            "midnight_00_02_temp_f": midnight_temp_f,
            "midnight_clocks_trap_triggered": trap_triggered,
            "latest_observed_temp_c": latest_c,
            "latest_observed_temp_f": latest_f,
            "metar_celsius_rounding_warning": True,
        }

    return {
        "vertical": "Daily High/Low Weather Station Grids (NWS + METAR)",
        "source_urls": ["https://api.weather.gov"],
        "stations": stations_out,
    }


def fetch_energy_oracles() -> Dict[str, Any]:
    aaa_url = "https://gasprices.aaa.com/"
    current_avg = None
    resp = safe_get(
        aaa_url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; PatroclusScanner/3.0)"},
        timeout=12,
    )
    if resp is not None and resp.status_code == 200:
        m = re.search(r"\$([2345]\.\d{3,4})", resp.text)
        if m:
            current_avg = float(m.group(1))

    return {
        "vertical": "AAA Daily National Gas & EIA Energy Trends",
        "source_urls": [
            "https://gasprices.aaa.com/",
            "https://ir.eia.gov/wpsr/psw01.csv",
        ],
        "aaa_national_regular_gas": {
            "current_regular_avg": current_avg,
        },
    }


def fetch_space_and_procedural_oracles() -> Dict[str, Any]:
    launches: List[Dict[str, Any]] = []
    ll_resp = safe_get(
        "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=6", timeout=10
    )
    if ll_resp is not None and ll_resp.status_code == 200:
        for item in ll_resp.json().get("results", [])[:6]:
            launches.append(
                {
                    "name": item.get("name"),
                    "net_utc": item.get("net"),
                    "status_abbrev": (item.get("status") or {}).get("abbrev"),
                }
            )

    fed_reg_count = 0
    fr_resp = safe_get(
        "https://www.federalregister.gov/api/v1/documents.json?per_page=5", timeout=10
    )
    if fr_resp is not None and fr_resp.status_code == 200:
        fed_reg_count = len(fr_resp.json().get("results", []))

    return {
        "upcoming_launches": launches,
        "federal_register_recent_docs": fed_reg_count,
    }


def is_excluded_market(market: Dict[str, Any], event_category: str = "") -> bool:
    ticker = (market.get("ticker") or "").upper()
    event_ticker = (market.get("event_ticker") or "").upper()
    series_ticker = (market.get("series_ticker") or market.get("_series_ticker") or "").upper()
    title = (market.get("title") or "").lower()
    cat = (event_category or market.get("_event_category") or market.get("category") or "").strip().lower()

    if cat in EXCLUDED_CATEGORIES:
        return True
    if market.get("mve_collection_ticker"):
        return True
    for pref in EXCLUDED_TICKER_PREFIXES:
        if (
            ticker.startswith(pref)
            or event_ticker.startswith(pref)
            or series_ticker.startswith(pref)
        ):
            return True
    if "crosscategory" in ticker.lower() or "crosscategory" in event_ticker.lower():
        return True
    if (
        title.count(",yes ")
        + title.count(",no ")
        + title.count(", yes ")
        + title.count(", no ")
        >= 2
    ):
        return True
    return False


def classify_orthogonality_bucket(market: Dict[str, Any]) -> str:
    ticker = (market.get("ticker") or "").upper()
    event_ticker = (market.get("event_ticker") or "").upper()
    series_ticker = (market.get("_series_ticker") or market.get("series_ticker") or "").upper()
    title = (market.get("title") or "").lower()
    cat = (market.get("_event_category") or market.get("category") or "").lower()

    for bucket, prefixes in TARGET_SERIES_BY_BUCKET.items():
        if any(
            ticker.startswith(p)
            or event_ticker.startswith(p)
            or series_ticker.startswith(p)
            for p in prefixes
        ):
            return bucket

    if "weather" in cat or "climate" in cat or any(
        k in ticker or k in event_ticker or k in title
        for k in ("KXHIGH", "KXLOWT", "KXRAIN", "KXSNOW", "KXHURR", "TEMPERATURE")
    ):
        return "BUCKET_A_WEATHER_ATMOSPHERIC"

    if cat in ("economics", "financials") or any(
        k in ticker or k in event_ticker or k in title
        for k in (
            "AAAGAS",
            "GAS PRICE",
            "WTI",
            "CRUDE",
            "CPI",
            "PCE",
            "INFLATION",
            "FOMC",
            "FED RATE",
            "PAYROLL",
            "JOBLESS",
            "GDP",
            "TREASURY",
        )
    ):
        return "BUCKET_B_MACRO_ENERGY_COMMODITY"

    return "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE"


def extract_cents(market: Dict[str, Any], cents_key: str, dollars_key: str) -> int:
    """
    Reads Kalshi v2 fixed-point dollar strings (`*_dollars`, e.g. `"0.0800"`) FIRST
    so a legacy `0` on `yes_bid` never masks a live v2 dollar quote.
    """
    d_val = market.get(dollars_key)
    if d_val is not None and str(d_val).strip() != "":
        try:
            c = int(round(float(d_val) * 100.0))
            if c > 0:
                return c
        except Exception:
            pass

    val = market.get(cents_key)
    if val is not None and str(val).strip() != "":
        try:
            f_val = float(val)
            if 0.0 < f_val < 1.0 and "." in str(val):
                return int(round(f_val * 100.0))
            c = int(round(f_val))
            if c > 0:
                return c
        except Exception:
            pass
    return 0


def extract_count(market: Dict[str, Any], int_key: str, fp_key: str) -> float:
    for k in (fp_key, int_key):
        v = market.get(k)
        if v is not None and str(v).strip() != "":
            try:
                num = float(v)
                if num > 0:
                    return num
            except Exception:
                pass
    return 0.0


def parse_expiration_hours(
    market: Dict[str, Any], now_utc: dt.datetime
) -> Optional[float]:
    exp_str = (
        market.get("expected_expiration_time")
        or market.get("close_time")
        or market.get("expiration_time")
    )
    if not exp_str:
        return None
    try:
        exp_dt = dt.datetime.fromisoformat(exp_str.replace("Z", "+00:00"))
        return round((exp_dt - now_utc).total_seconds() / 3600.0, 2)
    except Exception:
        return None


def harvest_kalshi_markets(
    now_utc: dt.datetime, max_event_pages: int = 20
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Primary discovery via `GET /events?status=open&with_nested_markets=true`
    (which natively excludes KXMVE multivariate parlays on Kalshi's backend),
    supplemented by direct series queries across Buckets A, B, and C.
    """
    seen_tickers = set()
    harvested: List[Dict[str, Any]] = []
    events_scanned = 0
    pages_fetched = 0
    min_close_ts = int(
        (now_utc + dt.timedelta(hours=MIN_HOURS_TO_EXPIRATION)).timestamp()
    )

    # Pass 1: Event-level discovery with nested markets (zero KXMVE parlay noise)
    cursor = None
    for _ in range(max_event_pages):
        params: Dict[str, Any] = {
            "status": "open",
            "with_nested_markets": "true",
            "min_close_ts": min_close_ts,
            "limit": 200,
        }
        if cursor:
            params["cursor"] = cursor
        resp = safe_get(KALSHI_EVENTS_URL, params=params, timeout=18)
        if resp is None or resp.status_code != 200:
            break
        pages_fetched += 1
        data = resp.json()
        events = data.get("events", [])
        if not events:
            break

        for ev in events:
            events_scanned += 1
            ev_cat = ev.get("category") or ""
            ev_title = ev.get("title") or ""
            ev_series = ev.get("series_ticker") or ""
            mut_excl = bool(ev.get("mutually_exclusive", False))
            nested = ev.get("markets") or []

            for m in nested:
                tkr = m.get("ticker")
                if not tkr or tkr in seen_tickers:
                    continue
                m["_event_category"] = ev_cat
                m["_event_title"] = ev_title
                m["_series_ticker"] = ev_series
                m["_mutually_exclusive"] = mut_excl
                if not is_excluded_market(m, ev_cat):
                    seen_tickers.add(tkr)
                    harvested.append(m)

        cursor = data.get("cursor")
        if not cursor:
            break

    # Pass 2: Explicit series sweep so core Weather/Gas/Entertainment series are never missed
    for bucket, series_list in TARGET_SERIES_BY_BUCKET.items():
        for s_tkr in series_list:
            resp = safe_get(
                KALSHI_MARKETS_URL,
                params={"status": "open", "series_ticker": s_tkr, "limit": 200},
                timeout=12,
            )
            if resp is not None and resp.status_code == 200:
                pages_fetched += 1
                for m in resp.json().get("markets", []):
                    tkr = m.get("ticker")
                    if tkr and tkr not in seen_tickers:
                        m.setdefault("_series_ticker", s_tkr)
                        if not is_excluded_market(m):
                            seen_tickers.add(tkr)
                            harvested.append(m)

    stats = {
        "pages_fetched": pages_fetched,
        "events_scanned": events_scanned,
        "total_open_markets_scanned": len(harvested),
    }
    return harvested, stats


def parse_orderbook_levels(
    raw_levels: Any, is_dollars: bool = False
) -> List[Tuple[int, float]]:
    """
    Parses Kalshi orderbook bid ladders (`yes_dollars`/`no_dollars` or legacy `yes`/`no`)
    and sorts descending so `levels[0]` is guaranteed to be the highest (best) bid.
    """
    parsed: List[Tuple[int, float]] = []
    if not isinstance(raw_levels, list):
        return parsed
    for item in raw_levels:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            try:
                p_raw, q_raw = item[0], item[1]
                p_float = float(p_raw)
                if is_dollars or (
                    (isinstance(p_raw, str) and "." in p_raw)
                    or (isinstance(p_raw, float) and 0.0 < p_float < 1.0)
                ):
                    price_cents = int(round(p_float * 100.0))
                else:
                    price_cents = int(round(p_float))
                qty = float(q_raw)
                if 1 <= price_cents <= 99 and qty > 0:
                    parsed.append((price_cents, qty))
            except Exception:
                continue
    parsed.sort(key=lambda x: x[0], reverse=True)
    return parsed


def extract_orderbook_from_body(ob_wrapper: Dict[str, Any]) -> Dict[str, List[Tuple[int, float]]]:
    ob_body = (
        ob_wrapper.get("orderbook_fp")
        or ob_wrapper.get("orderbook")
        or ob_wrapper
    )
    if not isinstance(ob_body, dict):
        return {"yes": [], "no": []}

    if ob_body.get("yes_dollars") is not None:
        yes_lvls = parse_orderbook_levels(ob_body.get("yes_dollars"), is_dollars=True)
    else:
        yes_lvls = parse_orderbook_levels(ob_body.get("yes"), is_dollars=False)

    if ob_body.get("no_dollars") is not None:
        no_lvls = parse_orderbook_levels(ob_body.get("no_dollars"), is_dollars=True)
    else:
        no_lvls = parse_orderbook_levels(ob_body.get("no"), is_dollars=False)

    return {"yes": yes_lvls, "no": no_lvls}


def batch_fetch_orderbooks(
    tickers: List[str],
) -> Dict[str, Dict[str, List[Tuple[int, float]]]]:
    """
    Uses repeated query parameters (`params={"tickers": chunk}`) as required by
    Kalshi's v2 `GET /markets/orderbooks` specification, with single-market fallback.
    """
    orderbooks: Dict[str, Dict[str, List[Tuple[int, float]]]] = {}
    unique_tickers = list(dict.fromkeys([t for t in tickers if t]))

    for i in range(0, len(unique_tickers), 50):
        chunk = unique_tickers[i : i + 50]
        resp = safe_get(
            KALSHI_ORDERBOOKS_BATCH_URL,
            params={"tickers": chunk},
            timeout=20,
        )
        if resp is not None and resp.status_code == 200:
            data = resp.json()
            raw_obs = data.get("orderbooks") or data.get("orderbooks_fp") or []
            if isinstance(raw_obs, list):
                for entry in raw_obs:
                    if not isinstance(entry, dict):
                        continue
                    tkr = entry.get("market_ticker") or entry.get("ticker")
                    if tkr:
                        parsed_ob = extract_orderbook_from_body(entry)
                        if parsed_ob["yes"] or parsed_ob["no"]:
                            orderbooks[tkr] = parsed_ob

        missing = [t for t in chunk if t not in orderbooks]
        for tkr in missing[:25]:
            s_resp = safe_get(f"{KALSHI_MARKETS_URL}/{tkr}/orderbook", timeout=10)
            if s_resp is not None and s_resp.status_code == 200:
                orderbooks[tkr] = extract_orderbook_from_body(s_resp.json())
            time.sleep(0.03)

    return orderbooks


def parse_target_date_from_ticker(ticker: str) -> Optional[str]:
    """
    Extracts `YYYY-MM-DD` from Kalshi date tokens like `-26NOV14` or `-2026NOV14`.
    """
    m = re.search(
        r"-(\d{2,4})(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(\d{2})\b",
        ticker.upper(),
    )
    if not m:
        return None
    yr_raw, mon_str, day_raw = m.group(1), m.group(2), m.group(3)
    year = int(yr_raw) + (2000 if len(yr_raw) == 2 else 0)
    month = MONTH_MAP[mon_str]
    day = int(day_raw)
    try:
        return dt.date(year, month, day).isoformat()
    except Exception:
        return None


def parse_float_or_none(val: Any) -> Optional[float]:
    if val is None or str(val).strip() == "":
        return None
    try:
        return float(val)
    except Exception:
        return None


def verify_oracle_tail_edge(
    market: Dict[str, Any],
    bucket: str,
    best_yes_bid: int,
    event_max_yes_bid: int,
    event_market_count: int,
    weather_oracles: Dict[str, Any],
    energy_oracles: Dict[str, Any],
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Ensures we NEVER bet 'No' on a center/consensus slice and enforces explicit
    NWS temperature and AAA gas strike distance buffers when numeric strikes exist.
    """
    tkr = (market.get("ticker") or "").upper()
    evt = (market.get("event_ticker") or "").upper()
    strike_type = (market.get("strike_type") or "").lower()
    floor_strike = parse_float_or_none(market.get("floor_strike"))
    cap_strike = parse_float_or_none(market.get("cap_strike"))
    hrs = float(market.get("_hours_to_expiration") or 24.0)

    # 1. Weather Station Strike-vs-Forecast Check
    if bucket == "BUCKET_A_WEATHER_ATMOSPHERIC":
        matched_station = None
        is_low_market = False
        for st_code, st_meta in NWS_STATIONS.items():
            if any(
                tkr.startswith(p) or evt.startswith(p)
                for p in st_meta["high_prefixes"]
            ):
                matched_station = weather_oracles.get("stations", {}).get(st_code)
                is_low_market = False
                break
            if any(
                tkr.startswith(p) or evt.startswith(p)
                for p in st_meta["low_prefixes"]
            ):
                matched_station = weather_oracles.get("stations", {}).get(st_code)
                is_low_market = True
                break

        if matched_station:
            target_date = parse_target_date_from_ticker(evt) or parse_target_date_from_ticker(tkr)
            today_local = matched_station.get("today_local_date")

            if (
                not is_low_market
                and target_date == today_local
                and matched_station.get("midnight_clocks_trap_triggered")
            ):
                return (
                    False,
                    "Disqualified: Midnight Clocks Trap active on same-day station high",
                    matched_station,
                )

            fcst_map = (
                matched_station.get("daily_forecast_lows_f", {})
                if is_low_market
                else matched_station.get("daily_forecast_highs_f", {})
            )
            ref_temp = fcst_map.get(target_date) if target_date else None
            if ref_temp is None and not is_low_market:
                ref_temp = matched_station.get("hourly_forecast_peak_f")
            if (
                not is_low_market
                and target_date == today_local
                and matched_station.get("observed_today_max_f") is not None
                and ref_temp is not None
            ):
                ref_temp = max(ref_temp, float(matched_station["observed_today_max_f"]))

            if ref_temp is not None and (floor_strike is not None or cap_strike is not None):
                st_id = matched_station["station_id"]
                lbl = "low" if is_low_market else "high"
                if strike_type == "greater" and floor_strike is not None:
                    diff = round(floor_strike - ref_temp, 1)
                    if diff < WEATHER_SAFE_BUFFER_F:
                        return False, "Strike too close to NWS forecast", matched_station
                    return (
                        True,
                        f"NWS {st_id} forecast {lbl} ({target_date or 'upcoming'}) is {ref_temp}F; strike above {floor_strike}F sits +{diff}F into the upper tail (clears METAR C-to-F rounding).",
                        matched_station,
                    )
                if strike_type == "less" and cap_strike is not None:
                    diff = round(ref_temp - cap_strike, 1)
                    if diff < WEATHER_SAFE_BUFFER_F:
                        return False, "Strike too close to NWS forecast", matched_station
                    return (
                        True,
                        f"NWS {st_id} forecast {lbl} ({target_date or 'upcoming'}) is {ref_temp}F; strike below {cap_strike}F sits -{diff}F into the lower tail.",
                        matched_station,
                    )
                if (
                    strike_type == "between"
                    and floor_strike is not None
                    and cap_strike is not None
                ):
                    if floor_strike >= ref_temp + WEATHER_SAFE_BUFFER_F:
                        diff = round(floor_strike - ref_temp, 1)
                        return (
                            True,
                            f"NWS {st_id} forecast {lbl} ({target_date or 'upcoming'}) is {ref_temp}F; bracket {floor_strike}F-{cap_strike}F sits +{diff}F above forecast.",
                            matched_station,
                        )
                    if cap_strike <= ref_temp - WEATHER_SAFE_BUFFER_F:
                        diff = round(ref_temp - cap_strike, 1)
                        return (
                            True,
                            f"NWS {st_id} forecast {lbl} ({target_date or 'upcoming'}) is {ref_temp}F; bracket {floor_strike}F-{cap_strike}F sits -{diff}F below forecast.",
                            matched_station,
                        )
                    return (
                        False,
                        "Disqualified: 2F weather bracket overlaps NWS forecast center",
                        matched_station,
                    )

    # 2. AAA National Regular Gas Strike-vs-Oracle Check
    if bucket == "BUCKET_B_MACRO_ENERGY_COMMODITY" and (
        "AAAGAS" in tkr or "AAAGAS" in evt or "GAS" in tkr
    ):
        aaa_avg = (
            energy_oracles.get("aaa_national_regular_gas", {}).get("current_regular_avg")
        )
        if aaa_avg is not None and (floor_strike is not None or cap_strike is not None):
            days_left = max(1.0, hrs / 24.0)
            req_buffer = round(max(0.02, 0.012 * days_left), 3)
            if strike_type == "greater" and floor_strike is not None:
                diff = round(floor_strike - aaa_avg, 4)
                if diff < req_buffer:
                    return False, "Gas strike within normal daily drift", None
                return (
                    True,
                    f"Live AAA national gas average is ${aaa_avg:.4f}/gal; strike above ${floor_strike:.3f} requires a +${diff:.3f}/gal jump inside {round(days_left, 1)}d.",
                    None,
                )
            if strike_type == "less" and cap_strike is not None:
                diff = round(aaa_avg - cap_strike, 4)
                if diff < req_buffer:
                    return False, "Gas strike within normal daily drift", None
                return (
                    True,
                    f"Live AAA national gas average is ${aaa_avg:.4f}/gal; strike below ${cap_strike:.3f} requires a -${diff:.3f}/gal drop inside {round(days_left, 1)}d.",
                    None,
                )
            if (
                strike_type == "between"
                and floor_strike is not None
                and cap_strike is not None
            ):
                if floor_strike >= aaa_avg + req_buffer or cap_strike <= aaa_avg - req_buffer:
                    return (
                        True,
                        f"Live AAA national gas average is ${aaa_avg:.4f}/gal; bracket ${floor_strike:.3f}-${cap_strike:.3f} sits outside the +- ${req_buffer:.3f} drift band.",
                        None,
                    )
                return False, "Gas bracket overlaps current AAA average", None

    # 3. Universal Distribution Tail Gate for Multi-Slice Ladders
    # Prevents betting 'No' on the consensus/modal slice when every slice in a 10-slice event is <=17c
    if event_market_count >= 4 and event_max_yes_bid > 0:
        if best_yes_bid >= max(event_max_yes_bid - 2, int(event_max_yes_bid * 0.75)):
            return (
                False,
                "Disqualified: Bracket is near the event's modal consensus center",
                None,
            )

    return (
        True,
        f"Tail longshot bid at {best_yes_bid}c Yes (event consensus peak {event_max_yes_bid}c Yes across {event_market_count} market(s)); verified two-sided book.",
        None,
    )


def evaluate_candidates(
    markets: List[Dict[str, Any]],
    bankroll_info: Dict[str, Any],
    weather_oracles: Dict[str, Any],
    energy_oracles: Dict[str, Any],
    now_utc: dt.datetime,
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    funnel = {
        "markets_scanned": len(markets),
        "in_8h_168h_window": 0,
        "passed_prelim_quote_gate": 0,
        "orderbooks_non_empty": 0,
        "passed_spread_and_depth_gate": 0,
        "passed_oracle_tail_gate": 0,
    }

    in_window: List[Dict[str, Any]] = []
    event_yes_ask_sum: Dict[str, int] = {}
    event_counts: Dict[str, int] = {}
    event_max_yes_bid: Dict[str, int] = {}

    for m in markets:
        hrs = parse_expiration_hours(m, now_utc)
        if hrs is None or not (MIN_HOURS_TO_EXPIRATION <= hrs <= MAX_HOURS_TO_EXPIRATION):
            continue
        funnel["in_8h_168h_window"] += 1
        m["_hours_to_expiration"] = hrs

        evt = m.get("event_ticker") or m.get("ticker") or ""
        yes_bid = extract_cents(m, "yes_bid", "yes_bid_dollars")
        no_bid = extract_cents(m, "no_bid", "no_bid_dollars")
        yes_ask = extract_cents(m, "yes_ask", "yes_ask_dollars") or (
            (100 - no_bid) if 1 <= no_bid <= 99 else 0
        )

        event_counts[evt] = event_counts.get(evt, 0) + 1
        if yes_ask > 0:
            event_yes_ask_sum[evt] = event_yes_ask_sum.get(evt, 0) + yes_ask
        if yes_bid > event_max_yes_bid.get(evt, 0):
            event_max_yes_bid[evt] = yes_bid

        in_window.append(m)

    # Pre-filter candidates near the target longshot window before fetching full depth
    preliminary: List[Dict[str, Any]] = []
    for m in in_window:
        yes_bid = extract_cents(m, "yes_bid", "yes_bid_dollars")
        no_bid = extract_cents(m, "no_bid", "no_bid_dollars")
        # Allow a 1c buffer on pre-filter in case top-of-book moved slightly
        if (MIN_YES_BID_CENTS - 1) <= yes_bid <= (MAX_YES_BID_CENTS + 1) and (
            MIN_NO_BID_CENTS - 1
        ) <= no_bid <= (MAX_NO_BID_CENTS + 1):
            preliminary.append(m)

    funnel["passed_prelim_quote_gate"] = len(preliminary)
    orderbooks = batch_fetch_orderbooks([m["ticker"] for m in preliminary])

    candidates: List[Dict[str, Any]] = []
    max_risk = bankroll_info["max_dollar_risk_5pct"]
    total_bankroll = bankroll_info["total_liquid_bankroll_dollars"]

    for m in preliminary:
        tkr = m["ticker"]
        evt = m.get("event_ticker") or tkr
        ob = orderbooks.get(tkr, {"yes": [], "no": []})
        yes_levels = ob.get("yes", [])
        no_levels = ob.get("no", [])

        if yes_levels or no_levels:
            funnel["orderbooks_non_empty"] += 1

        best_yes_bid = (
            yes_levels[0][0]
            if yes_levels
            else extract_cents(m, "yes_bid", "yes_bid_dollars")
        )
        best_no_bid = (
            no_levels[0][0]
            if no_levels
            else extract_cents(m, "no_bid", "no_bid_dollars")
        )
        last_price_yes = extract_cents(m, "last_price", "last_price_dollars")

        # HARD GATE 1: Strict two-sided quote bounds (zero 99c/1c or 0-bid books)
        if not (MIN_YES_BID_CENTS <= best_yes_bid <= MAX_YES_BID_CENTS):
            continue
        if not (MIN_NO_BID_CENTS <= best_no_bid <= MAX_NO_BID_CENTS):
            continue

        spread_cents = 100 - best_yes_bid - best_no_bid
        if not (MIN_SPREAD_CENTS <= spread_cents <= MAX_SPREAD_CENTS):
            continue

        top_no_queue = int(round(sum(q for _, q in no_levels[:2])))
        total_no_qty = int(round(sum(q for _, q in no_levels)))
        total_yes_qty = int(round(sum(q for _, q in yes_levels)))
        total_book_qty = total_no_qty + total_yes_qty

        vol_24h = extract_count(m, "volume_24h", "volume_24h_fp")
        open_int = extract_count(m, "open_interest", "open_interest_fp")

        # HARD GATE 2: Minimum real resting depth & market participation
        if total_yes_qty <= 0 or total_book_qty < MIN_TOTAL_BOOK_CONTRACTS:
            continue
        if max(vol_24h, open_int, float(total_book_qty)) < MIN_ACTIVITY_CONTRACTS:
            continue
        if top_no_queue > MAX_TOP_NO_QUEUE_DEPTH:
            continue

        obi = (
            round((total_no_qty - total_yes_qty) / total_book_qty, 4)
            if total_book_qty > 0
            else 0.0
        )
        high_adverse = abs(obi) > MAX_OBI_THRESHOLD
        if high_adverse:
            continue

        funnel["passed_spread_and_depth_gate"] += 1

        bucket = classify_orthogonality_bucket(m)
        edge_ok, edge_proof, matched_station = verify_oracle_tail_edge(
            market=m,
            bucket=bucket,
            best_yes_bid=best_yes_bid,
            event_max_yes_bid=event_max_yes_bid.get(evt, best_yes_bid),
            event_market_count=event_counts.get(evt, 1),
            weather_oracles=weather_oracles,
            energy_oracles=energy_oracles,
        )
        if not edge_ok:
            continue

        funnel["passed_oracle_tail_gate"] += 1

        rec_maker_no_bid = min(best_no_bid + 1, 96)
        implied_yes_ask = 100 - best_no_bid
        price_per_contract = rec_maker_no_bid / 100.0

        uncapped_contracts = int(math.floor(max_risk / price_per_contract))
        depth_cap_contracts = max(
            1, int(math.floor(total_book_qty * MAX_BOOK_DEPTH_SHARE))
        )
        contracts_to_bid = min(uncapped_contracts, depth_cap_contracts)
        if contracts_to_bid < 1:
            continue

        liquidity_cap_applied = contracts_to_bid < uncapped_contracts
        total_exposure = round(contracts_to_bid * price_per_contract, 2)
        max_profit = round(contracts_to_bid * (1.0 - price_per_contract), 2)
        net_return_pct = round(
            ((1.0 - price_per_contract) / price_per_contract) * 100.0, 2
        )

        taker_fee_per_contract = round(
            0.07 * price_per_contract * (1.0 - price_per_contract), 4
        )

        # Only report multi-candidate overround when outcomes are mutually exclusive
        mut_excl = bool(m.get("_mutually_exclusive", False))
        raw_overround = round(event_yes_ask_sum.get(evt, 100) / 100.0, 2)
        effective_overround = raw_overround if (mut_excl and event_counts.get(evt, 1) >= 2) else 1.0

        hrs = m["_hours_to_expiration"]
        velocity_bonus = max(0.0, (MAX_HOURS_TO_EXPIRATION - hrs) / 24.0) * 1.5
        depth_bonus = min(8.0, math.log1p(total_book_qty) * 1.5)
        overround_bonus = max(0.0, (effective_overround - 1.0) * 25.0)

        quality_score = (
            (best_yes_bid * 1.6)
            + velocity_bonus
            + depth_bonus
            + overround_bonus
            - (spread_cents * 1.1)
            - (top_no_queue * 0.004)
        )

        candidates.append(
            {
                "ticker": tkr,
                "event_ticker": evt,
                "series_ticker": m.get("_series_ticker") or m.get("series_ticker") or "",
                "title": m.get("title") or m.get("_event_title") or "",
                "subtitle": m.get("yes_sub_title") or m.get("subtitle") or "",
                "category": m.get("_event_category") or m.get("category") or "",
                "kalshi_market_url": f"https://kalshi.com/markets/{evt.lower()}",
                "orthogonality_bucket": bucket,
                "hours_to_expiration": hrs,
                "expiration_iso": m.get("expected_expiration_time")
                or m.get("close_time")
                or m.get("expiration_time"),
                "quality_score": round(quality_score, 3),
                "oracle_edge_proof": edge_proof,
                "orderbook_pricing": {
                    "best_yes_bid_cents": best_yes_bid,
                    "best_no_bid_cents": best_no_bid,
                    "implied_yes_ask_cents": implied_yes_ask,
                    "last_price_yes_cents": last_price_yes,
                    "recommended_maker_no_bid_cents": rec_maker_no_bid,
                    "price_improvement_cents": 1,
                },
                "microstructure_metrics": {
                    "spread_cents": spread_cents,
                    "top_no_queue_depth": top_no_queue,
                    "total_no_bid_qty": total_no_qty,
                    "total_yes_bid_qty": total_yes_qty,
                    "total_book_depth_contracts": total_book_qty,
                    "volume_24h_contracts": round(vol_24h, 1),
                    "open_interest_contracts": round(open_int, 1),
                    "obi": obi,
                    "mutually_exclusive_event": mut_excl,
                    "event_overround": effective_overround,
                    "taker_fee_saved_dollars_per_contract": taker_fee_per_contract,
                    "taker_fee_saved_cents_per_contract": round(
                        taker_fee_per_contract * 100.0, 2
                    ),
                    "total_taker_fee_saved_on_position_dollars": round(
                        taker_fee_per_contract * contracts_to_bid, 2
                    ),
                    "high_adverse_selection_risk": high_adverse,
                },
                "position_sizing_5pct_cap": {
                    "total_bankroll_dollars": total_bankroll,
                    "max_dollar_risk_5pct": max_risk,
                    "uncapped_5pct_contracts": uncapped_contracts,
                    "liquidity_cap_35pct_book_contracts": depth_cap_contracts,
                    "liquidity_cap_applied": liquidity_cap_applied,
                    "contracts_to_bid": contracts_to_bid,
                    "total_order_exposure_dollars": total_exposure,
                    "max_profit_if_no_wins_dollars": max_profit,
                    "net_win_return_pct": net_return_pct,
                    "payoff_asymmetry_losses_to_wipe_wins": f"{round(price_per_contract / (1.0 - price_per_contract), 2)}-to-1",
                },
                "primary_truth_oracle": {
                    "oracle_edge_proof": edge_proof,
                    "weather_station": matched_station,
                    "event_field_inflation": {
                        "event_ticker": evt,
                        "candidate_count": event_counts.get(evt, 1),
                        "mutually_exclusive": mut_excl,
                        "event_overround": effective_overround,
                        "field_inflation_flagged": effective_overround > 1.05,
                    },
                },
            }
        )

    candidates.sort(key=lambda x: x["quality_score"], reverse=True)
    return candidates, funnel


def select_orthogonal_top_candidates(
    all_candidates: List[Dict[str, Any]],
) -> Tuple[Dict[str, Optional[Dict[str, Any]]], List[Dict[str, Any]]]:
    buckets = [
        "BUCKET_A_WEATHER_ATMOSPHERIC",
        "BUCKET_B_MACRO_ENERGY_COMMODITY",
        "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE",
    ]
    by_bucket: Dict[str, List[Dict[str, Any]]] = {
        b: [c for c in all_candidates if c["orthogonality_bucket"] == b]
        for b in buckets
    }

    selected_3: Dict[str, Optional[Dict[str, Any]]] = {
        b: (by_bucket[b][0] if by_bucket[b] else None) for b in buckets
    }

    # Deduplicate to max 2 brackets per event in the Top 25 table so one event never hogs all rows
    balanced: List[Dict[str, Any]] = []
    seen_tickers = set()
    event_row_counts: Dict[str, int] = {}

    for b in buckets:
        added_in_bucket = 0
        for c in by_bucket[b]:
            evt = c["event_ticker"]
            if event_row_counts.get(evt, 0) >= 2:
                continue
            balanced.append(c)
            seen_tickers.add(c["ticker"])
            event_row_counts[evt] = event_row_counts.get(evt, 0) + 1
            added_in_bucket += 1
            if added_in_bucket >= 8:
                break

    for c in all_candidates:
        if len(balanced) >= 25:
            break
        evt = c["event_ticker"]
        if c["ticker"] not in seen_tickers and event_row_counts.get(evt, 0) < 2:
            balanced.append(c)
            seen_tickers.add(c["ticker"])
            event_row_counts[evt] = event_row_counts.get(evt, 0) + 1

    return selected_3, balanced[:25]


def write_outputs(snapshot: Dict[str, Any]) -> None:
    with open("kalshi_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    b_info = snapshot["bankroll_and_kelly_sizing"]
    funnel = snapshot["diagnostics_funnel"]
    sel_3 = snapshot["selected_3_orthogonal_picks"]
    top_25 = snapshot["top_25_uncrowded_candidates"]

    lines = [
        "# Patroclus Kalshi Longshot-Bias Underwriting Snapshot (v3.0)",
        f"**Timestamp:** `{snapshot['generated_at_utc']}`  ",
        f"**Repository:** [{snapshot['repository_url']}]({snapshot['repository_url']})  ",
        "",
        "## 1. Liquid Bankroll & Kelly Sizing Guardrails",
        f"* **Balance Source:** `{b_info['source']}`",
        f"* **Effective Sizing Bankroll:** `${b_info['total_liquid_bankroll_dollars']:.2f}`",
        f"* **Max Dollar Risk Per Pick (5% Cap):** `${b_info['max_dollar_risk_5pct']:.2f}` (auto-capped at `<=35%` of visible book depth on thin markets)",
        f"* **Max Daily Deployed Capital (15% Max):** `${b_info['max_daily_deployed_15pct']:.2f}`",
        f"* **Dry Powder Reserve (85% Min):** `${b_info['dry_powder_reserve_85pct']:.2f}`",
        "",
        "## 2. Scanner Diagnostics Funnel",
        f"* **Open Non-Parlay Markets Scanned:** `{funnel['markets_scanned']}`",
        f"* **In Expiration Window (8h - 168h):** `{funnel['in_8h_168h_window']}`",
        f"* **Passed Preliminary Two-Sided Quote Gate:** `{funnel['passed_prelim_quote_gate']}`",
        f"* **Non-Empty Orderbooks Retrieved (`orderbook_fp`):** `{funnel['orderbooks_non_empty']}`",
        f"* **Passed Spread (2c-15c) & Book Depth Gate:** `{funnel['passed_spread_and_depth_gate']}`",
        f"* **Passed Strike-vs-Oracle Tail Gate:** `{funnel['passed_oracle_tail_gate']}`",
        "",
        "## 3. Top 3 Orthogonal Picks (1 Per Bucket)",
    ]

    for bucket_name, cand in sel_3.items():
        if cand is None:
            lines.append(
                f"* **{bucket_name}:** `SKIP BUCKET` — No contract currently meets two-sided spread (2c-15c), book depth, and oracle tail distance gates."
            )
        else:
            ob = cand["orderbook_pricing"]
            mm = cand["microstructure_metrics"]
            sz = cand["position_sizing_5pct_cap"]
            cap_note = (
                f" *(depth-capped from {sz['uncapped_5pct_contracts']} to 35% of {mm['total_book_depth_contracts']}-contract book)*"
                if sz["liquidity_cap_applied"]
                else ""
            )
            sub_str = f" ({cand['subtitle']})" if cand.get("subtitle") else ""
            lines.append(
                f"* **{bucket_name}:** [`{cand['ticker']}`]({cand['kalshi_market_url']}) — {cand['title']}{sub_str}  \n"
                f"  * **Action:** Buy No (Limit) @ **{ob['recommended_maker_no_bid_cents']}c** x **{sz['contracts_to_bid']} contracts**{cap_note} "
                f"(Risk `${sz['total_order_exposure_dollars']:.2f}` to win `${sz['max_profit_if_no_wins_dollars']:.2f}` / `+{sz['net_win_return_pct']}%`)  \n"
                f"  * **Book:** Yes Bid `{ob['best_yes_bid_cents']}c` / No Bid `{ob['best_no_bid_cents']}c` | Spread `{mm['spread_cents']}c` | Book Depth `{mm['total_book_depth_contracts']}` | Expires `{cand['hours_to_expiration']}h`  \n"
                f"  * **Oracle Proof:** {cand['oracle_edge_proof']}"
            )

    lines.extend(
        [
            "",
            "## 4. Top Uncrowded Maker 'No' Underwriting Candidates",
            "",
            "| Rank | Ticker | Bucket | Yes Bid | No Bid | Maker No Bid | Contracts | Spread | Book Depth | Net Return % | Hours Left |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
    )

    for idx, c in enumerate(top_25, 1):
        ob = c["orderbook_pricing"]
        mm = c["microstructure_metrics"]
        sz = c["position_sizing_5pct_cap"]
        lines.append(
            f"| {idx} | [{c['ticker']}]({c['kalshi_market_url']}) | {c['orthogonality_bucket']} | "
            f"{ob['best_yes_bid_cents']}c | {ob['best_no_bid_cents']}c | "
            f"**{ob['recommended_maker_no_bid_cents']}c** | "
            f"**{sz['contracts_to_bid']}** (`${sz['total_order_exposure_dollars']:.2f}`) | "
            f"{mm['spread_cents']}c | {mm['total_book_depth_contracts']} | "
            f"+{sz['net_win_return_pct']}% | {c['hours_to_expiration']}h |"
        )

    with open("kalshi_snapshot.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    now_utc = dt.datetime.now(dt.timezone.utc)
    bankroll_info = fetch_bankroll_and_sizing()
    weather_oracles = fetch_weather_oracles(now_utc)
    energy_oracles = fetch_energy_oracles()
    space_proc_oracles = fetch_space_and_procedural_oracles()

    markets, harvest_stats = harvest_kalshi_markets(now_utc)
    all_candidates, funnel = evaluate_candidates(
        markets, bankroll_info, weather_oracles, energy_oracles, now_utc
    )
    selected_3, top_25 = select_orthogonal_top_candidates(all_candidates)

    bucket_counts = {
        b: sum(1 for c in all_candidates if c["orthogonality_bucket"] == b)
        for b in (
            "BUCKET_A_WEATHER_ATMOSPHERIC",
            "BUCKET_B_MACRO_ENERGY_COMMODITY",
            "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE",
        )
    }
    funnel["candidates_by_bucket"] = bucket_counts

    snapshot = {
        "scanner_name": "Patroclus Kalshi Longshot-Bias Underwriting Scanner v3.0",
        "generated_at_utc": now_utc.isoformat(),
        "repository_url": "https://github.com/chrisdonreynolds/patroclus",
        "raw_json_url": "https://raw.githubusercontent.com/chrisdonreynolds/patroclus/main/kalshi_snapshot.json",
        "raw_md_url": "https://raw.githubusercontent.com/chrisdonreynolds/patroclus/main/kalshi_snapshot.md",
        "user_agent": USER_AGENT,
        "execution_mode": "CHOICE_1_MANUAL_APP_EXECUTION_ONLY",
        "bankroll_and_kelly_sizing": bankroll_info,
        "harvest_statistics": harvest_stats,
        "diagnostics_funnel": funnel,
        "primary_truth_feeds": {
            "vertical_2_3_space_procedural": space_proc_oracles,
            "vertical_6_weather": weather_oracles,
            "vertical_7_energy": energy_oracles,
        },
        "selected_3_orthogonal_picks": selected_3,
        "top_25_uncrowded_candidates": top_25,
    }
    write_outputs(snapshot)


if __name__ == "__main__":
    main()
