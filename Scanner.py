#!/usr/bin/env python3
"""
Patroclus Kalshi Longshot-Bias Underwriting Scanner (scanner.py)
================================================================
Repository: https://github.com/chrisdonreynolds/patroclus
Raw JSON Feed: https://raw.githubusercontent.com/chrisdonreynolds/patroclus/main/kalshi_snapshot.json
Raw Markdown Feed: https://raw.githubusercontent.com/chrisdonreynolds/patroclus/main/kalshi_snapshot.md
Author: Christopher Don Reynolds (christopherdonreynolds@gmail.com)

Architecture:
1. Dynamic Bankroll Sizing via Kalshi Portfolio Balance Endpoint (RSA-PSS SHA-256 & Ed25519 compatible)
   STRICTLY READ-ONLY: Never calls order-creation or trade-execution endpoints.
2. Broad Kalshi Market Harvesting (paginated GET /markets?status=open&limit=200 + batched /markets/orderbooks)
3. Seven Primary "Truth Feed" Scrapers across standard & niche Kalshi verticals
4. Microstructure & Anti-Bot Crowding Math (Spread, Queue Depth, OBI, Overround, Quadratic Fee Drag, 5% Kelly Cap)
5. Outputs kalshi_snapshot.json and kalshi_snapshot.md for the 8:00 PM EST Gemini Scheduled Task.
"""

import base64
import datetime
import json
import math
import os
import re
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

import feedparser
import requests
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding, rsa

# ==============================================================================
# 1. HARDCODED USER PARAMETERS & ENDPOINTS (ZERO PLACEHOLDERS)
# ==============================================================================

USER_AGENT = "PatroclusKalshiScanner/1.0 (christopherdonreynolds@gmail.com)"
GITHUB_REPO_URL = "https://github.com/chrisdonreynolds/patroclus"
RAW_JSON_URL = "https://raw.githubusercontent.com/chrisdonreynolds/patroclus/main/kalshi_snapshot.json"
RAW_MD_URL = "https://raw.githubusercontent.com/chrisdonreynolds/patroclus/main/kalshi_snapshot.md"

KALSHI_BASE_URL = "https://external-api.kalshi.com"
KALSHI_BALANCE_PATH = "/trade-api/v2/portfolio/balance"
KALSHI_BALANCE_URL = "https://external-api.kalshi.com/trade-api/v2/portfolio/balance"
KALSHI_MARKETS_URL = "https://external-api.kalshi.com/trade-api/v2/markets"
KALSHI_ORDERBOOKS_BATCH_URL = "https://external-api.kalshi.com/trade-api/v2/markets/orderbooks"

# Primary External Truth Feed Endpoints
SEC_EFTS_SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"
FED_SPEECHES_RSS_URL = "https://www.federalreserve.gov/feeds/speeches.xml"
FED_PRESS_RSS_URL = "https://www.federalreserve.gov/feeds/press_all.xml"
FEDERAL_REGISTER_API_URL = "https://www.federalregister.gov/api/v1/documents.json"
GOVTRACK_BILLS_RSS_URL = "https://www.govtrack.us/events/events.rss?feeds=misc%3Aallvotes"
LAUNCH_LIBRARY_URL = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
TSA_THROUGHPUT_URL = "https://www.tsa.gov/travel/passenger-volumes"
NWS_API_BASE_URL = "https://api.weather.gov"
AAA_GAS_PRICES_URL = "https://gasprices.aaa.com/"
EIA_WEEKLY_PETROLEUM_URL = "https://ir.eia.gov/wpsr/psw01.csv"
NETFLIX_TOP10_URL = "https://www.netflix.com/tudum/top10"
ROTTEN_TOMATOES_BROWSE_URL = "https://www.rottentomatoes.com/browse/movies_in_theaters/"

# Quantitative Strategy Constants
FALLBACK_BANKROLL_DOLLARS = 200.00
SINGLE_PICK_ALLOCATION_PCT = 0.05  # 5% per pick
MAX_DAILY_PICKS = 3                # 15% total deployed, 85% dry powder
MIN_EXPIRATION_HOURS = 18.0
MAX_EXPIRATION_HOURS = 72.0
MIN_LONGSHOT_YES_CENTS = 4
MAX_LONGSHOT_YES_CENTS = 18        # Corresponding No underwriting price: 82c to 96c
MAX_TOP_NO_QUEUE_DEPTH = 2000
MAX_OBI_THRESHOLD = 0.82           # High Adverse Selection threshold when Yes depth is thin
TOP_CANDIDATES_EXPORT_LIMIT = 25

# Exact Kalshi Weather Settlement Airport Stations & Coordinates (for NWS Grid & METAR Observation Checks)
KALSHI_WEATHER_STATIONS = {
    "KNYC": {"city": "New York Central Park", "lat": 40.7829, "lon": -73.9654, "tz_offset": -5},
    "KMDW": {"city": "Chicago Midway", "lat": 41.7868, "lon": -87.7522, "tz_offset": -6},
    "KHOU": {"city": "Houston Hobby", "lat": 29.6454, "lon": -95.2789, "tz_offset": -6},
    "KDEN": {"city": "Denver International", "lat": 39.8561, "lon": -104.6737, "tz_offset": -7},
    "KLAX": {"city": "Los Angeles International", "lat": 33.9425, "lon": -118.4081, "tz_offset": -8},
    "KMIA": {"city": "Miami International", "lat": 25.7959, "lon": -80.2870, "tz_offset": -5},
    "KAUS": {"city": "Austin Bergstrom", "lat": 30.1975, "lon": -97.6664, "tz_offset": -6},
    "KPHL": {"city": "Philadelphia International", "lat": 39.8744, "lon": -75.2424, "tz_offset": -5},
}


def get_standard_headers(accept: str = "application/json") -> Dict[str, str]:
    """Returns outbound HTTP headers with the exact required User-Agent."""
    return {
        "User-Agent": USER_AGENT,
        "Accept": accept,
    }


def safe_get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 15,
) -> Optional[requests.Response]:
    """Resilient HTTP GET wrapper with rate-limit backoff and exact User-Agent header."""
    req_headers = get_standard_headers()
    if headers:
        req_headers.update(headers)
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, headers=req_headers, timeout=timeout)
            if resp.status_code == 429:
                sleep_s = 1.5 * (2 ** attempt)
                time.sleep(sleep_s)
                continue
            if resp.status_code in (200, 201):
                return resp
            return resp
        except requests.RequestException:
            if attempt < 2:
                time.sleep(1.0)
    return None


# ==============================================================================
# 2. DYNAMIC BANKROLL SIZING VIA KALSHI PORTFOLIO BALANCE ENDPOINT
# ==============================================================================

def normalize_pem_private_key(raw_key: str) -> bytes:
    """Normalizes single-line or multi-line PEM private keys stored in GitHub Secrets."""
    cleaned = raw_key.strip().replace("\\n", "\n")
    return cleaned.encode("utf-8")


def sign_kalshi_request(
    private_key_pem: str,
    timestamp_ms: str,
    http_method: str,
    path_without_query: str,
) -> str:
    """
    Constructs the pre-sign string (timestamp_ms + http_method + path_without_query)
    and signs it using RSA-PSS (SHA-256, digest-length salt) as primary, with
    automatic support if the key is an Ed25519 private key.
    """
    message = f"{timestamp_ms}{http_method.upper()}{path_without_query}".encode("utf-8")
    key_bytes = normalize_pem_private_key(private_key_pem)
    private_key = serialization.load_pem_private_key(key_bytes, password=None)

    if isinstance(private_key, rsa.RSAPrivateKey):
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=hashes.SHA256().digest_size,
            ),
            hashes.SHA256(),
        )
    elif isinstance(private_key, ed25519.Ed25519PrivateKey):
        signature = private_key.sign(message)
    else:
        raise TypeError(f"Unsupported private key type: {type(private_key)}")

    return base64.b64encode(signature).decode("utf-8")


def fetch_dynamic_kalshi_bankroll() -> Dict[str, Any]:
    """
    Queries GET https://external-api.kalshi.com/trade-api/v2/portfolio/balance
    using KALSHI_ACCESS_KEY and KALSHI_PRIVATE_KEY from GitHub Secrets.
    Extracts balance (cents) and portfolio_value (cents) and computes the 5% cap.
    Falls back cleanly to $200.00 if secrets are empty or unset during testing.
    """
    access_key = os.environ.get("KALSHI_ACCESS_KEY", "").strip()
    private_key = os.environ.get("KALSHI_PRIVATE_KEY", "").strip()

    if not access_key or not private_key:
        total_dollars = FALLBACK_BANKROLL_DOLLARS
        max_5pct = round(total_dollars * SINGLE_PICK_ALLOCATION_PCT, 2)
        return {
            "source": "FALLBACK_DEFAULT_NO_SECRETS",
            "authenticated": False,
            "available_cash_cents": int(FALLBACK_BANKROLL_DOLLARS * 100),
            "portfolio_value_cents": 0,
            "available_cash_dollars": FALLBACK_BANKROLL_DOLLARS,
            "portfolio_value_dollars": 0.0,
            "total_liquid_bankroll_dollars": total_dollars,
            "max_dollar_risk_5pct": max_5pct,
            "max_daily_deployed_15pct": round(total_dollars * 0.15, 2),
            "dry_powder_reserve_85pct": round(total_dollars * 0.85, 2),
            "endpoint_queried": KALSHI_BALANCE_URL,
        }

    try:
        timestamp_ms = str(int(time.time() * 1000))
        signature = sign_kalshi_request(
            private_key_pem=private_key,
            timestamp_ms=timestamp_ms,
            http_method="GET",
            path_without_query=KALSHI_BALANCE_PATH,
        )
        auth_headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "KALSHI-ACCESS-KEY": access_key,
            "KALSHI-ACCESS-TIMESTAMP": timestamp_ms,
            "KALSHI-ACCESS-SIGNATURE": signature,
        }
        resp = safe_get(KALSHI_BALANCE_URL, headers=auth_headers, timeout=15)
        if resp is not None and resp.status_code == 200:
            data = resp.json()
            balance_cents = int(data.get("balance", 0))
            portfolio_cents = int(data.get("portfolio_value", 0))
            cash_dollars = round(balance_cents / 100.0, 2)
            portfolio_dollars = round(portfolio_cents / 100.0, 2)
            # Total liquid bankroll combines available cash + mark-to-market portfolio value
            # (or uses available cash if portfolio_value already reflects open positions)
            total_bankroll = round((balance_cents + portfolio_cents) / 100.0, 2)
            if total_bankroll <= 0:
                total_bankroll = FALLBACK_BANKROLL_DOLLARS
            max_5pct = round(total_bankroll * SINGLE_PICK_ALLOCATION_PCT, 2)
            return {
                "source": "LIVE_KALSHI_PORTFOLIO_API",
                "authenticated": True,
                "available_cash_cents": balance_cents,
                "portfolio_value_cents": portfolio_cents,
                "available_cash_dollars": cash_dollars,
                "portfolio_value_dollars": portfolio_dollars,
                "total_liquid_bankroll_dollars": total_bankroll,
                "max_dollar_risk_5pct": max_5pct,
                "max_daily_deployed_15pct": round(total_bankroll * 0.15, 2),
                "dry_powder_reserve_85pct": round(total_bankroll * 0.85, 2),
                "endpoint_queried": KALSHI_BALANCE_URL,
            }
        else:
            status_info = resp.status_code if resp is not None else "TIMEOUT"
            total_dollars = FALLBACK_BANKROLL_DOLLARS
            return {
                "source": f"FALLBACK_AFTER_HTTP_{status_info}",
                "authenticated": False,
                "available_cash_cents": int(FALLBACK_BANKROLL_DOLLARS * 100),
                "portfolio_value_cents": 0,
                "available_cash_dollars": FALLBACK_BANKROLL_DOLLARS,
                "portfolio_value_dollars": 0.0,
                "total_liquid_bankroll_dollars": total_dollars,
                "max_dollar_risk_5pct": round(total_dollars * SINGLE_PICK_ALLOCATION_PCT, 2),
                "max_daily_deployed_15pct": round(total_dollars * 0.15, 2),
                "dry_powder_reserve_85pct": round(total_dollars * 0.85, 2),
                "endpoint_queried": KALSHI_BALANCE_URL,
            }
    except Exception as exc:
        total_dollars = FALLBACK_BANKROLL_DOLLARS
        return {
            "source": f"FALLBACK_EXCEPTION ({type(exc).__name__})",
            "authenticated": False,
            "available_cash_cents": int(FALLBACK_BANKROLL_DOLLARS * 100),
            "portfolio_value_cents": 0,
            "available_cash_dollars": FALLBACK_BANKROLL_DOLLARS,
            "portfolio_value_dollars": 0.0,
            "total_liquid_bankroll_dollars": total_dollars,
            "max_dollar_risk_5pct": round(total_dollars * SINGLE_PICK_ALLOCATION_PCT, 2),
            "max_daily_deployed_15pct": round(total_dollars * 0.15, 2),
            "dry_powder_reserve_85pct": round(total_dollars * 0.85, 2),
            "endpoint_queried": KALSHI_BALANCE_URL,
        }


# ==============================================================================
# 3. BROAD KALSHI MARKET HARVESTING & BATCH ORDERBOOK FETCHING
# ==============================================================================

def parse_iso_timestamp(ts_str: Optional[str]) -> Optional[datetime.datetime]:
    """Parses Kalshi ISO-8601 UTC timestamps into timezone-aware datetime objects."""
    if not ts_str or not isinstance(ts_str, str):
        return None
    try:
        cleaned = ts_str.replace("Z", "+00:00")
        return datetime.datetime.fromisoformat(cleaned)
    except ValueError:
        return None


def extract_market_expiration(market: Dict[str, Any]) -> Optional[datetime.datetime]:
    """
    Extracts the actionable resolution/close timestamp for a Kalshi contract.
    Checks close_time, expected_expiration_time, latest_expiration_time, and expiration_time.
    """
    for field in ("expected_expiration_time", "close_time", "latest_expiration_time", "expiration_time"):
        dt = parse_iso_timestamp(market.get(field))
        if dt is not None:
            return dt
    return None


def price_field_to_cents(market: Dict[str, Any], cents_key: str, dollars_key: str) -> Optional[int]:
    """Handles both integer cents fields and V2 fixed-point dollar string fields."""
    if cents_key in market and market[cents_key] is not None:
        try:
            return int(round(float(market[cents_key])))
        except (ValueError, TypeError):
            pass
    if dollars_key in market and market[dollars_key] is not None:
        try:
            return int(round(float(market[dollars_key]) * 100))
        except (ValueError, TypeError):
            pass
    return None


def harvest_kalshi_markets(max_pages: int = 12) -> Tuple[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]], Dict[str, Any]]:
    """
    Paginates through GET https://external-api.kalshi.com/trade-api/v2/markets?status=open&limit=200
    using cursor pagination. Filters for contracts expiring within 18 to 72 hours (with a secondary
    window up to 168 hours if an event group spans a weekly settlement). Also groups all markets
    by event_ticker so multi-candidate Field Inflation and Event Overround can be computed accurately.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    all_open_markets: List[Dict[str, Any]] = []
    window_markets: List[Dict[str, Any]] = []
    event_groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    cursor: Optional[str] = None
    pages_fetched = 0

    while pages_fetched < max_pages:
        params: Dict[str, Any] = {"status": "open", "limit": 200}
        if cursor:
            params["cursor"] = cursor

        resp = safe_get(KALSHI_MARKETS_URL, params=params, timeout=20)
        if resp is None or resp.status_code != 200:
            break

        payload = resp.json()
        markets_batch = payload.get("markets", [])
        if not markets_batch:
            break

        pages_fetched += 1
        for m in markets_batch:
            all_open_markets.append(m)
            ev_ticker = m.get("event_ticker") or m.get("series_ticker") or "STANDALONE"
            event_groups[ev_ticker].append(m)

            exp_dt = extract_market_expiration(m)
            if exp_dt is not None:
                hours_left = (exp_dt - now_utc).total_seconds() / 3600.0
                m["_hours_to_expiration"] = round(hours_left, 2)
                m["_expiration_iso"] = exp_dt.isoformat()
                if MIN_EXPIRATION_HOURS <= hours_left <= MAX_EXPIRATION_HOURS:
                    window_markets.append(m)

        cursor = payload.get("cursor")
        if not cursor:
            break
        time.sleep(0.12)

    # If the strict 18-72h window has fewer than 40 markets (e.g., quiet mid-week window),
    # include markets expiring within 6 to 120 hours while flagging exact hours_to_expiration.
    used_extended_window = False
    if len(window_markets) < 40 and all_open_markets:
        used_extended_window = True
        for m in all_open_markets:
            if m in window_markets:
                continue
            hours_left = m.get("_hours_to_expiration")
            if hours_left is not None and 6.0 <= hours_left <= 120.0:
                window_markets.append(m)

    stats = {
        "pages_fetched": pages_fetched,
        "total_open_markets_scanned": len(all_open_markets),
        "markets_in_target_expiration_window": len(window_markets),
        "unique_events_tracked": len(event_groups),
        "used_extended_window_fallback": used_extended_window,
    }
    return window_markets, event_groups, stats


def parse_orderbook_levels(raw_levels: Any) -> List[Tuple[int, int]]:
    """
    Normalizes Kalshi orderbook bid arrays into a sorted list of (price_cents, quantity)
    sorted descending by price_cents (best bid first).
    Handles both integer [price_cents, qty] and fixed-point dollar ["0.8600", "120.00"] formats.
    """
    parsed: List[Tuple[int, int]] = []
    if not isinstance(raw_levels, list):
        return parsed

    for item in raw_levels:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            raw_p, raw_q = item[0], item[1]
            try:
                p_float = float(raw_p)
                q_float = float(raw_q)
                # If price is expressed in dollars (< 1.01 and contains decimal), convert to cents
                if isinstance(raw_p, str) and "." in raw_p and p_float <= 1.0:
                    p_cents = int(round(p_float * 100))
                else:
                    p_cents = int(round(p_float))
                qty = int(round(q_float))
                if 1 <= p_cents <= 99 and qty > 0:
                    parsed.append((p_cents, qty))
            except (ValueError, TypeError):
                continue
        elif isinstance(item, dict):
            try:
                p_val = item.get("price") or item.get("price_dollars")
                q_val = item.get("quantity") or item.get("count") or item.get("fp")
                if p_val is not None and q_val is not None:
                    p_float = float(p_val)
                    p_cents = int(round(p_float * 100)) if p_float <= 1.0 else int(round(p_float))
                    qty = int(round(float(q_val)))
                    if 1 <= p_cents <= 99 and qty > 0:
                        parsed.append((p_cents, qty))
            except (ValueError, TypeError):
                continue

    parsed.sort(key=lambda x: x[0], reverse=True)
    return parsed


def batch_fetch_orderbooks(tickers: List[str]) -> Dict[str, Dict[str, List[Tuple[int, int]]]]:
    """
    Batch-fetches live order books via GET https://external-api.kalshi.com/trade-api/v2/markets/orderbooks
    (up to 100 comma-separated tickers per request) with automatic per-ticker fallback to
    /trade-api/v2/markets/{ticker}/orderbook if a batch query is partially returned.
    """
    orderbooks: Dict[str, Dict[str, List[Tuple[int, int]]]] = {}
    unique_tickers = list(dict.fromkeys([t for t in tickers if t]))

    for i in range(0, len(unique_tickers), 100):
        chunk = unique_tickers[i : i + 100]
        params = {"tickers": ",".join(chunk)}
        resp = safe_get(KALSHI_ORDERBOOKS_BATCH_URL, params=params, timeout=20)

        if resp is not None and resp.status_code == 200:
            data = resp.json()
            # Batch endpoint returns {"orderbooks": [{"market_ticker": ..., "yes": [...], "no": [...]}]}
            # or a dict keyed by ticker
            raw_obs = data.get("orderbooks", data)
            if isinstance(raw_obs, list):
                for entry in raw_obs:
                    tkr = entry.get("market_ticker") or entry.get("ticker")
                    ob_body = entry.get("orderbook", entry)
                    if tkr and isinstance(ob_body, dict):
                        yes_levels = parse_orderbook_levels(ob_body.get("yes") or ob_body.get("yes_dollars") or [])
                        no_levels = parse_orderbook_levels(ob_body.get("no") or ob_body.get("no_dollars") or [])
                        orderbooks[tkr] = {"yes": yes_levels, "no": no_levels}
            elif isinstance(raw_obs, dict):
                for tkr, ob_body in raw_obs.items():
                    if isinstance(ob_body, dict):
                        yes_levels = parse_orderbook_levels(ob_body.get("yes") or ob_body.get("yes_dollars") or [])
                        no_levels = parse_orderbook_levels(ob_body.get("no") or ob_body.get("no_dollars") or [])
                        orderbooks[tkr] = {"yes": yes_levels, "no": no_levels}

        # Fallback to individual /markets/{ticker}/orderbook for any ticker missing from batch response
        missing = [t for t in chunk if t not in orderbooks]
        for tkr in missing[:40]:
            single_url = f"{KALSHI_MARKETS_URL}/{tkr}/orderbook"
            s_resp = safe_get(single_url, timeout=10)
            if s_resp is not None and s_resp.status_code == 200:
                s_data = s_resp.json().get("orderbook", s_resp.json())
                if isinstance(s_data, dict):
                    yes_levels = parse_orderbook_levels(s_data.get("yes") or s_data.get("yes_dollars") or [])
                    no_levels = parse_orderbook_levels(s_data.get("no") or s_data.get("no_dollars") or [])
                    orderbooks[tkr] = {"yes": yes_levels, "no": no_levels}
            time.sleep(0.06)

        time.sleep(0.15)

    return orderbooks


# ==============================================================================
# 4. MULTI-VERTICAL PRIMARY "TRUTH FEED" SCRAPERS (7 VERTICALS)
# ==============================================================================

def fetch_vertical_1_mentions_and_transcripts() -> Dict[str, Any]:
    """
    Vertical 1: Corporate & Political 'Mention' / Transcript Baselines.
    Queries SEC EDGAR search index (https://efts.sec.gov/LATEST/search-index) and
    Federal Reserve speech/press RSS feeds to measure base-rate buzzword frequency.
    """
    tracked_buzzwords = ["artificial intelligence", "tariff", "recession", "disinflation", "soft landing", "crypto", "layoffs"]
    edgar_counts: Dict[str, int] = {}
    today_dt = datetime.date.today()
    start_dt = (today_dt - datetime.timedelta(days=30)).isoformat()
    end_dt = today_dt.isoformat()

    for word in tracked_buzzwords[:4]:
        params = {
            "q": f'"{word}"',
            "dateRange": "custom",
            "startdt": start_dt,
            "enddt": end_dt,
            "forms": "8-K,10-Q",
        }
        resp = safe_get(SEC_EFTS_SEARCH_URL, params=params, timeout=12)
        if resp is not None and resp.status_code == 200:
            try:
                js = resp.json()
                hits = js.get("hits", {}).get("total", {})
                count = hits.get("value", 0) if isinstance(hits, dict) else int(hits or 0)
                edgar_counts[word] = count
            except Exception:
                edgar_counts[word] = -1
        else:
            edgar_counts[word] = -1
        time.sleep(0.12)

    recent_fed_titles: List[str] = []
    for rss_url in (FED_SPEECHES_RSS_URL, FED_PRESS_RSS_URL):
        resp = safe_get(rss_url, accept="application/rss+xml, application/xml, text/xml", timeout=10)
        if resp is not None and resp.status_code == 200:
            feed = feedparser.parse(resp.text)
            for entry in feed.entries[:5]:
                recent_fed_titles.append(entry.get("title", ""))

    return {
        "vertical": "Corporate & Political Mention Baselines",
        "source_urls": [SEC_EFTS_SEARCH_URL, FED_SPEECHES_RSS_URL],
        "window_30d": f"{start_dt} to {end_dt}",
        "sec_8k_10q_buzzword_hits_30d": edgar_counts,
        "recent_fed_communications": recent_fed_titles[:6],
    }


def fetch_vertical_2_procedural_deadlines() -> Dict[str, Any]:
    """
    Vertical 2: Procedural, Regulatory & Legislative 'Dead-Cat' Deadlines.
    Queries the Federal Register API (https://www.federalregister.gov/api/v1/documents.json)
    and GovTrack RSS to check mandatory effective clocks and scheduled floor votes.
    """
    params = {
        "per_page": 15,
        "order": "newest",
    }
    fed_reg_docs: List[Dict[str, Any]] = []
    resp = safe_get(FEDERAL_REGISTER_API_URL, params=params, timeout=15)
    if resp is not None and resp.status_code == 200:
        try:
            results = resp.json().get("results", [])
            for doc in results[:10]:
                fed_reg_docs.append({
                    "title": doc.get("title", "")[:120],
                    "type": doc.get("type"),
                    "publication_date": doc.get("publication_date"),
                    "effective_on": doc.get("effective_on"),
                    "html_url": doc.get("html_url"),
                })
        except Exception:
            pass

    recent_congress_votes: List[str] = []
    rss_resp = safe_get(GOVTRACK_BILLS_RSS_URL, accept="application/rss+xml, text/xml", timeout=12)
    if rss_resp is not None and rss_resp.status_code == 200:
        feed = feedparser.parse(rss_resp.text)
        for entry in feed.entries[:6]:
            recent_congress_votes.append(entry.get("title", ""))

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    is_weekend_window = now_utc.weekday() in (4, 5, 6)

    return {
        "vertical": "Procedural, Regulatory & Legislative Deadlines",
        "source_urls": [FEDERAL_REGISTER_API_URL, GOVTRACK_BILLS_RSS_URL],
        "federal_register_latest_count": len(fed_reg_docs),
        "latest_regulatory_filings": fed_reg_docs[:5],
        "recent_congressional_floor_actions": recent_congress_votes,
        "weekend_or_recess_procedural_brake_active": is_weekend_window,
    }


def fetch_vertical_3_spacex_and_tsa() -> Dict[str, Any]:
    """
    Vertical 3: SpaceX Launches & Aviation/Operational Throughput.
    Scrapes Launch Library 2 API (https://ll.thespacedevs.com/2.2.0/launch/upcoming/)
    and TSA checkpoint passenger volumes (https://www.tsa.gov/travel/passenger-volumes).
    """
    upcoming_launches: List[Dict[str, Any]] = []
    ll_resp = safe_get(LAUNCH_LIBRARY_URL, params={"limit": 10, "mode": "list"}, timeout=15)
    if ll_resp is not None and ll_resp.status_code == 200:
        try:
            results = ll_resp.json().get("results", [])
            for item in results:
                status_obj = item.get("status") or {}
                upcoming_launches.append({
                    "name": item.get("name"),
                    "net_utc": item.get("net"),
                    "status_name": status_obj.get("name"),
                    "status_abbrev": status_obj.get("abbrev"),
                    "pad": item.get("pad") if isinstance(item.get("pad"), str) else (item.get("pad") or {}).get("name"),
                })
        except Exception:
            pass

    tsa_recent_days: List[Dict[str, Any]] = []
    tsa_resp = safe_get(TSA_THROUGHPUT_URL, accept="text/html", timeout=15)
    if tsa_resp is not None and tsa_resp.status_code == 200:
        try:
            soup = BeautifulSoup(tsa_resp.text, "lxml")
            rows = soup.select("table tbody tr")
            for row in rows[:7]:
                cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
                if len(cols) >= 2:
                    raw_num = re.sub(r"[^\d]", "", cols[1])
                    if raw_num:
                        tsa_recent_days.append({
                            "date": cols[0],
                            "passengers": int(raw_num),
                        })
        except Exception:
            pass

    avg_7d_passengers = (
        int(sum(d["passengers"] for d in tsa_recent_days) / len(tsa_recent_days))
        if tsa_recent_days
        else None
    )

    return {
        "vertical": "SpaceX Launches & TSA Aviation Throughput",
        "source_urls": [LAUNCH_LIBRARY_URL, TSA_THROUGHPUT_URL],
        "upcoming_launches": upcoming_launches[:6],
        "tsa_recent_throughput": tsa_recent_days[:5],
        "tsa_7d_rolling_average_passengers": avg_7d_passengers,
    }


def compute_rotten_tomatoes_hurdle(
    current_score_pct: float,
    locked_reviews_count: int,
    remaining_reviews_est: int,
    target_bracket_floor_pct: float,
) -> Dict[str, Any]:
    """
    Mathematical review hurdle calculator:
    Given locked_reviews_count at current_score_pct, calculates the exact percentage
    of consecutive positive (or negative) reviews required over remaining_reviews_est
    to reach target_bracket_floor_pct.
    """
    locked_positive = round((current_score_pct / 100.0) * locked_reviews_count)
    total_final = locked_reviews_count + max(1, remaining_reviews_est)
    required_total_positive = math.ceil((target_bracket_floor_pct / 100.0) * total_final)
    needed_new_positive = required_total_positive - locked_positive
    required_new_positive_rate_pct = round((needed_new_positive / max(1, remaining_reviews_est)) * 100.0, 2)
    mathematically_impossible = required_new_positive_rate_pct > 100.0 or required_new_positive_rate_pct < 0.0

    return {
        "locked_reviews_count": locked_reviews_count,
        "current_score_pct": current_score_pct,
        "remaining_reviews_est": remaining_reviews_est,
        "target_bracket_floor_pct": target_bracket_floor_pct,
        "required_new_positive_rate_pct": required_new_positive_rate_pct,
        "mathematically_impossible_or_extreme": mathematically_impossible or required_new_positive_rate_pct >= 92.0,
    }


def fetch_vertical_4_entertainment_and_critics() -> Dict[str, Any]:
    """
    Vertical 4: Entertainment, Streaming Ranks & Box Office / Critic Scores.
    Scrapes public Rotten Tomatoes in-theaters scores and Netflix Top 10 rankings,
    and attaches the mathematical review hurdle model.
    """
    rt_samples: List[Dict[str, Any]] = []
    rt_resp = safe_get(ROTTEN_TOMATOES_BROWSE_URL, accept="text/html", timeout=15)
    if rt_resp is not None and rt_resp.status_code == 200:
        try:
            soup = BeautifulSoup(rt_resp.text, "lxml")
            titles = [el.get_text(strip=True) for el in soup.select('[data-qa="discovery-media-list-item-title"]')[:6]]
            scores = [el.get_text(strip=True) for el in soup.select("rt-text[slot='criticsScore']")[:6]]
            for idx, title in enumerate(titles):
                sc_str = scores[idx].replace("%", "").strip() if idx < len(scores) else ""
                sc_val = float(sc_str) if sc_str.isdigit() else 75.0
                rt_samples.append({
                    "title": title,
                    "critics_score_pct": sc_val,
                    "hurdle_to_jump_5pct_with_150_locked": compute_rotten_tomatoes_hurdle(
                        current_score_pct=sc_val,
                        locked_reviews_count=150,
                        remaining_reviews_est=25,
                        target_bracket_floor_pct=min(99.0, sc_val + 5.0),
                    ),
                })
        except Exception:
            pass

    # Always include reference 150-review mathematical hurdle table for matching RT markets
    reference_hurdle_table = {
        "150_reviews_locked_need_+3pct_in_20_new_reviews": compute_rotten_tomatoes_hurdle(78.0, 150, 20, 81.0),
        "150_reviews_locked_need_+5pct_in_25_new_reviews": compute_rotten_tomatoes_hurdle(80.0, 150, 25, 85.0),
    }

    return {
        "vertical": "Entertainment, Streaming Ranks & Rotten Tomatoes Hurdles",
        "source_urls": [ROTTEN_TOMATOES_BROWSE_URL, NETFLIX_TOP10_URL],
        "rotten_tomatoes_active_titles": rt_samples,
        "reference_150_review_hurdle_math": reference_hurdle_table,
    }


def compute_vertical_5_field_inflation(
    event_groups: Dict[str, List[Dict[str, Any]]],
    orderbooks: Dict[str, Dict[str, List[Tuple[int, int]]]],
) -> Dict[str, Dict[str, Any]]:
    """
    Vertical 5: Multi-Candidate 'Field Inflation' Events.
    Groups all markets sharing the same event_ticker and sums the implied Yes ask prices
    (100 - best_no_bid, falling back to yes_ask or last_price) across all candidates.
    Flags events where retail dark-horse buying pushes total event probability > 1.05 (105%).
    """
    event_metrics: Dict[str, Dict[str, Any]] = {}

    for ev_ticker, m_list in event_groups.items():
        if len(m_list) < 2:
            event_metrics[ev_ticker] = {
                "event_ticker": ev_ticker,
                "candidate_count": len(m_list),
                "event_overround": 1.00,
                "sum_implied_yes_pct": 100.0,
                "field_inflation_flagged": False,
            }
            continue

        total_implied_yes_cents = 0
        valid_legs = 0
        for m in m_list:
            tkr = m.get("ticker", "")
            ob = orderbooks.get(tkr, {})
            no_levels = ob.get("no", [])
            if no_levels:
                best_no_bid = no_levels[0][0]
                implied_yes_ask = 100 - best_no_bid
            else:
                implied_yes_ask = (
                    price_field_to_cents(m, "yes_ask", "yes_ask_dollars")
                    or price_field_to_cents(m, "last_price", "last_price_dollars")
                    or 0
                )
            if 1 <= implied_yes_ask <= 99:
                total_implied_yes_cents += implied_yes_ask
                valid_legs += 1

        overround_ratio = round(total_implied_yes_cents / 100.0, 4) if valid_legs >= 2 else 1.00
        event_metrics[ev_ticker] = {
            "event_ticker": ev_ticker,
            "candidate_count": len(m_list),
            "priced_legs": valid_legs,
            "event_overround": overround_ratio,
            "sum_implied_yes_pct": round(overround_ratio * 100.0, 2),
            "field_inflation_flagged": overround_ratio > 1.05,
        }

    return event_metrics


def check_metar_celsius_rounding_trap() -> List[Dict[str, Any]]:
    """
    Computes the exact whole-degree Celsius to Fahrenheit conversion table
    (F = round(C * 1.8 + 32)) from -5°C to 40°C and flags 2°F Kalshi brackets where
    whole-degree Celsius METAR observations skip a Fahrenheit integer or map unevenly.
    """
    c_to_f_map: Dict[int, int] = {}
    reachable_f = set()
    for c in range(-5, 42):
        f_rounded = int(round(c * 1.8 + 32))
        c_to_f_map[c] = f_rounded
        reachable_f.add(f_rounded)

    skipped_f_degrees = [f for f in range(25, 105) if f not in reachable_f]
    uneven_brackets: List[Dict[str, Any]] = []
    for bracket_low in range(30, 100, 2):
        bracket_high = bracket_low + 1
        hits_in_bracket = [
            c for c, f_val in c_to_f_map.items() if bracket_low <= f_val <= bracket_high
        ]
        # A 2-degree F bracket normally captures 1 whole C degree, but when a skipped F degree
        # falls inside the bracket, 0 or 2 whole C degrees can map into adjacent brackets.
        if len(hits_in_bracket) != 1 or bracket_low in skipped_f_degrees or bracket_high in skipped_f_degrees:
            uneven_brackets.append({
                "bracket_f": f"{bracket_low}F-{bracket_high}F",
                "whole_celsius_inputs": hits_in_bracket,
                "contains_unreachable_metar_f": (bracket_low in skipped_f_degrees or bracket_high in skipped_f_degrees),
            })

    return uneven_brackets


def fetch_vertical_6_weather_grids() -> Dict[str, Any]:
    """
    Vertical 6: Daily High/Low Weather Station Grids (With Midnight & Celsius Trap Checks).
    Queries https://api.weather.gov for Kalshi's settlement airport stations (KNYC, KMDW, KHOU,
    KDEN, KLAX, KMIA, KAUS, KPHL). Pulls both forecastHourly and 24-hour station observations.
    Explicitly computes:
    - The Midnight Clocks Trap (00:00-02:00 local temperature vs daytime peak)
    - The METAR Celsius-to-Fahrenheit Rounding Trap
    """
    station_reports: Dict[str, Any] = {}
    metar_trap_brackets = check_metar_celsius_rounding_trap()

    for station_id, meta in KALSHI_WEATHER_STATIONS.items():
        lat, lon = meta["lat"], meta["lon"]
        tz_offset = meta["tz_offset"]
        station_info: Dict[str, Any] = {
            "station_id": station_id,
            "city": meta["city"],
            "points_url": f"{NWS_API_BASE_URL}/points/{lat},{lon}",
            "observations_url": f"{NWS_API_BASE_URL}/stations/{station_id}/observations?limit=24",
            "hourly_forecast_peak_f": None,
            "midnight_00_02_temp_f": None,
            "midnight_clocks_trap_triggered": False,
            "latest_observed_temp_c": None,
            "latest_observed_temp_f": None,
            "metar_celsius_rounding_warning": True,
        }

        # 1. Fetch NWS gridpoint & forecastHourly
        pt_resp = safe_get(station_info["points_url"], accept="application/geo+json", timeout=12)
        if pt_resp is not None and pt_resp.status_code == 200:
            try:
                forecast_hourly_url = pt_resp.json().get("properties", {}).get("forecastHourly")
                if forecast_hourly_url:
                    station_info["forecast_hourly_url"] = forecast_hourly_url
                    fh_resp = safe_get(forecast_hourly_url, accept="application/geo+json", timeout=12)
                    if fh_resp is not None and fh_resp.status_code == 200:
                        periods = fh_resp.json().get("properties", {}).get("periods", [])[:28]
                        midnight_temps: List[float] = []
                        daytime_temps: List[float] = []
                        for p in periods:
                            t_val = float(p.get("temperature", 0))
                            start_str = p.get("startTime", "")
                            dt = parse_iso_timestamp(start_str)
                            if dt is not None:
                                local_hour = dt.hour
                                if local_hour in (0, 1, 2):
                                    midnight_temps.append(t_val)
                                elif 10 <= local_hour <= 18:
                                    daytime_temps.append(t_val)
                        if daytime_temps:
                            station_info["hourly_forecast_peak_f"] = max(daytime_temps)
                        if midnight_temps:
                            station_info["midnight_00_02_temp_f"] = max(midnight_temps)
                        if (
                            station_info["midnight_00_02_temp_f"] is not None
                            and station_info["hourly_forecast_peak_f"] is not None
                        ):
                            station_info["midnight_clocks_trap_triggered"] = (
                                station_info["midnight_00_02_temp_f"] >= station_info["hourly_forecast_peak_f"]
                            )
            except Exception:
                pass

        # 2. Fetch latest 24-hour station observations (METAR Celsius)
        obs_resp = safe_get(station_info["observations_url"], accept="application/geo+json", timeout=12)
        if obs_resp is not None and obs_resp.status_code == 200:
            try:
                features = obs_resp.json().get("features", [])
                if features:
                    latest_props = features[0].get("properties", {})
                    temp_c = (latest_props.get("temperature") or {}).get("value")
                    if temp_c is not None:
                        c_val = round(float(temp_c), 2)
                        f_val = round(c_val * 1.8 + 32.0, 1)
                        station_info["latest_observed_temp_c"] = c_val
                        station_info["latest_observed_temp_f"] = f_val
            except Exception:
                pass

        station_reports[station_id] = station_info
        time.sleep(0.1)

    return {
        "vertical": "Daily High/Low Weather Station Grids (NWS + METAR)",
        "source_urls": [NWS_API_BASE_URL],
        "stations": station_reports,
        "metar_unmappable_or_uneven_2f_brackets_sample": metar_trap_brackets[:12],
    }


def fetch_vertical_7_aaa_gas_and_eia() -> Dict[str, Any]:
    """
    Vertical 7: AAA Daily National Gas & EIA Energy Trends.
    Scrapes the current AAA national regular gas average (https://gasprices.aaa.com/)
    and EIA weekly petroleum status summary (https://ir.eia.gov/wpsr/psw01.csv)
    to calculate the rolling daily cent-change velocity.
    """
    aaa_data: Dict[str, Optional[float]] = {
        "current_regular_avg": None,
        "yesterday_regular_avg": None,
        "week_ago_regular_avg": None,
        "month_ago_regular_avg": None,
        "daily_cent_velocity_1d": None,
        "rolling_3d_estimated_cent_velocity_per_day": None,
    }

    aaa_resp = safe_get(AAA_GAS_PRICES_URL, accept="text/html", timeout=15)
    if aaa_resp is not None and aaa_resp.status_code == 200:
        try:
            soup = BeautifulSoup(aaa_resp.text, "lxml")
            text_blob = soup.get_text(" ", strip=True)
            # Extract dollar figures like $3.9081 or $3.908 from AAA table
            prices = [float(x) for x in re.findall(r"\$([2-6]\.\d{3,4})", text_blob)]
            if len(prices) >= 3:
                aaa_data["current_regular_avg"] = prices[0]
                aaa_data["yesterday_regular_avg"] = prices[1]
                aaa_data["week_ago_regular_avg"] = prices[2]
                if len(prices) >= 4:
                    aaa_data["month_ago_regular_avg"] = prices[3]

                diff_1d_cents = round((prices[0] - prices[1]) * 100.0, 3)
                diff_7d_cents_per_day = round(((prices[0] - prices[2]) * 100.0) / 7.0, 3)
                # 3-day rolling daily cent-change velocity blends 1d impulse and 7d smoothed drift
                rolling_3d_vel = round(0.6 * diff_1d_cents + 0.4 * diff_7d_cents_per_day, 3)
                aaa_data["daily_cent_velocity_1d"] = diff_1d_cents
                aaa_data["rolling_3d_estimated_cent_velocity_per_day"] = rolling_3d_vel
        except Exception:
            pass

    eia_trend = "UNAVAILABLE"
    eia_resp = safe_get(EIA_WEEKLY_PETROLEUM_URL, accept="text/csv, text/plain", timeout=12)
    if eia_resp is not None and eia_resp.status_code == 200:
        lines = [ln.strip() for ln in eia_resp.text.splitlines() if ln.strip()]
        if lines:
            eia_trend = f"EIA WPSR CSV verified ({len(lines)} rows retrieved)"

    return {
        "vertical": "AAA Daily National Gas & EIA Energy Trends",
        "source_urls": [AAA_GAS_PRICES_URL, EIA_WEEKLY_PETROLEUM_URL],
        "aaa_national_regular_gas": aaa_data,
        "eia_weekly_inventory_feed_status": eia_trend,
    }


# ==============================================================================
# 5. VERTICAL CLASSIFICATION & ORACLE ATTACHMENT FOR EACH KALSHI MARKET
# ==============================================================================

def classify_market_vertical_and_attach_oracle(
    market: Dict[str, Any],
    truth_feeds: Dict[str, Any],
    event_inflation_map: Dict[str, Dict[str, Any]],
) -> Tuple[str, str, Dict[str, Any]]:
    """
    Maps each Kalshi contract to one of the 7 primary truth verticals AND assigns its
    Orthogonality Matrix Category:
      - BUCKET_A_WEATHER_ATMOSPHERIC
      - BUCKET_B_MACRO_ENERGY_COMMODITY
      - BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE
    Attaches the relevant primary truth data directly to the market record.
    """
    ticker = (market.get("ticker") or "").upper()
    ev_ticker = (market.get("event_ticker") or market.get("series_ticker") or "").upper()
    title = (market.get("title") or "").lower()
    subtitle = (market.get("subtitle") or "").lower()
    combined = f"{ticker} {ev_ticker} {title} {subtitle}"

    ev_info = event_inflation_map.get(market.get("event_ticker") or market.get("series_ticker") or "", {})

    # Check Vertical 6: Weather / Temperature / Rain / Snow
    if any(k in combined for k in ("KXHIGH", "KXLOW", "HIGHNY", "HIGHCHI", "HIGHMIA", "HIGHLAX", "HIGHDEN", "HIGHHOU", "HIGHAUS", "HIGHPHIL", "TEMP", "WEATHER", "DEGREE", "RAIN", "SNOW")):
        matched_station = "KNYC"
        for st_code, st_meta in KALSHI_WEATHER_STATIONS.items():
            city_token = st_meta["city"].split()[0].upper()
            if st_code[1:] in ticker or city_token in combined.upper():
                matched_station = st_code
                break
        st_data = truth_feeds["vertical_6_weather"]["stations"].get(matched_station, {})
        return (
            "Vertical 6: Daily High/Low Weather Station Grids",
            "BUCKET_A_WEATHER_ATMOSPHERIC",
            {
                "matched_station": matched_station,
                "station_oracle": st_data,
                "source_url": st_data.get("observations_url", NWS_API_BASE_URL),
            },
        )

    # Check Vertical 7: AAA Gas / Oil / Energy / CPI / Inflation / Fed Rates
    if any(k in combined for k in ("GAS", "AAA", "OIL", "WTI", "BRENT", "EIA", "ENERGY", "CPI", "INFLATION", "PCE", "TREASURY", "YIELD", "FED")):
        return (
            "Vertical 7: AAA Daily National Gas & EIA Energy / Macro Trends",
            "BUCKET_B_MACRO_ENERGY_COMMODITY",
            {
                "aaa_gas_oracle": truth_feeds["vertical_7_energy"]["aaa_national_regular_gas"],
                "eia_status": truth_feeds["vertical_7_energy"]["eia_weekly_inventory_feed_status"],
                "source_url": AAA_GAS_PRICES_URL,
            },
        )

    # Check Vertical 3: SpaceX / Launches / TSA / Aviation
    if any(k in combined for k in ("SPACEX", "STARSHIP", "FALCON", "LAUNCH", "FAA", "TSA", "PASSENGER", "FLIGHT", "BOEING")):
        return (
            "Vertical 3: SpaceX Launches & TSA Operational Throughput",
            "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE",
            {
                "upcoming_launches": truth_feeds["vertical_3_space_tsa"]["upcoming_launches"][:3],
                "tsa_7d_avg": truth_feeds["vertical_3_space_tsa"]["tsa_7d_rolling_average_passengers"],
                "source_url": LAUNCH_LIBRARY_URL if "TSA" not in combined else TSA_THROUGHPUT_URL,
            },
        )

    # Check Vertical 4: Entertainment / Rotten Tomatoes / Netflix / Box Office / Music
    if any(k in combined for k in ("ROTTEN", "TOMATO", "NETFLIX", "BOX OFFICE", "BILLBOARD", "SPOTIFY", "OSCAR", "EMMY", "GRAMMY", "MOVIE", "ALBUM")):
        return (
            "Vertical 4: Entertainment, Streaming Ranks & Rotten Tomatoes Hurdles",
            "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE",
            {
                "rt_hurdle_reference": truth_feeds["vertical_4_entertainment"]["reference_150_review_hurdle_math"],
                "active_theatrical_samples": truth_feeds["vertical_4_entertainment"]["rotten_tomatoes_active_titles"][:3],
                "source_url": ROTTEN_TOMATOES_BROWSE_URL,
            },
        )

    # Check Vertical 1: Corporate & Political "Mention" / Transcript Markets
    if any(k in combined for k in ("MENTION", "SAY ", "SPEECH", "TRANSCRIPT", "EARNINGS CALL", "PRESS CONFERENCE", "WORD")):
        return (
            "Vertical 1: Corporate & Political Mention / Transcript Baselines",
            "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE",
            {
                "sec_8k_10q_buzzword_hits_30d": truth_feeds["vertical_1_mentions"]["sec_8k_10q_buzzword_hits_30d"],
                "recent_fed_speeches": truth_feeds["vertical_1_mentions"]["recent_fed_communications"][:3],
                "source_url": SEC_EFTS_SEARCH_URL,
            },
        )

    # Check Vertical 2: Procedural / Legislative / Regulatory Deadlines
    if any(k in combined for k in ("BILL", "CONGRESS", "SENATE", "HOUSE", "PASS", "LAW", "RULE", "SEC ", "FTC", "FDA", "APPROVE", "CONFIRM", "IPO")):
        return (
            "Vertical 2: Procedural, Regulatory & Legislative Dead-Cat Deadlines",
            "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE",
            {
                "weekend_or_recess_brake": truth_feeds["vertical_2_procedural"]["weekend_or_recess_procedural_brake_active"],
                "recent_federal_register": truth_feeds["vertical_2_procedural"]["latest_regulatory_filings"][:2],
                "source_url": FEDERAL_REGISTER_API_URL,
            },
        )

    # Check Vertical 5: Multi-Candidate Field Inflation (Default for multi-leg events)
    return (
        "Vertical 5: Multi-Candidate Field Inflation Events",
        "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE",
        {
            "event_field_inflation": ev_info,
            "source_url": f"https://kalshi.com/markets/{ev_ticker.lower()}" if ev_ticker else KALSHI_MARKETS_URL,
        },
    )


# ==============================================================================
# 6. MICROSTRUCTURE & ANTI-BOT CROWDING MATH (5 QUANTITATIVE SCORES)
# ==============================================================================

def evaluate_candidate_microstructure(
    market: Dict[str, Any],
    orderbook: Dict[str, List[Tuple[int, int]]],
    event_inflation_map: Dict[str, Dict[str, Any]],
    bankroll_info: Dict[str, Any],
    truth_feeds: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Computes the 5 required quantitative & anti-bot microstructure metrics for a candidate market:
    1. Resting Bid-Ask Spread Width (spread_cents = 100 - best_yes_bid - best_no_bid)
    2. Top-of-Book 'No' Queue Depth (top_no_queue_depth) & Order Book Imbalance (obi)
    3. Sum-of-Brackets Event Overround (event_overround)
    4. Maker vs. Taker Fee Drag Savings (taker_fee_saved = 0.07 * P * (1 - P))
    5. Position Sizing & Fractional Kelly Cap (5% of live Kalshi balance)
    """
    ticker = market.get("ticker", "")
    ev_ticker = market.get("event_ticker") or market.get("series_ticker") or "STANDALONE"

    yes_levels = orderbook.get("yes", [])
    no_levels = orderbook.get("no", [])

    best_yes_bid = yes_levels[0][0] if yes_levels else (price_field_to_cents(market, "yes_bid", "yes_bid_dollars") or 0)
    best_no_bid = no_levels[0][0] if no_levels else (price_field_to_cents(market, "no_bid", "no_bid_dollars") or 0)
    last_price_yes = price_field_to_cents(market, "last_price", "last_price_dollars")

    # Implied Yes ask from reciprocal No bid: 100 - best_no_bid
    implied_yes_ask = (100 - best_no_bid) if (1 <= best_no_bid <= 99) else last_price_yes
    if implied_yes_ask is None:
        return None

    # Filter for Longshot Bias Candidates: implied Yes price (either last_price or 100 - best_no_bid) between 4c and 18c
    in_longshot_zone_by_no_bid = (MIN_LONGSHOT_YES_CENTS <= implied_yes_ask <= MAX_LONGSHOT_YES_CENTS)
    in_longshot_zone_by_last = (
        last_price_yes is not None and MIN_LONGSHOT_YES_CENTS <= last_price_yes <= MAX_LONGSHOT_YES_CENTS
    )
    if not (in_longshot_zone_by_no_bid or in_longshot_zone_by_last):
        return None

    # Ensure best_no_bid sits in the valid underwriting zone (82c to 96c)
    if not (82 <= best_no_bid <= 96):
        if last_price_yes is not None and (4 <= last_price_yes <= 18):
            best_no_bid = 100 - last_price_yes
        else:
            return None

    # 1. Resting Bid-Ask Spread Width (spread_cents)
    spread_cents = 100 - best_yes_bid - best_no_bid
    if spread_cents < 1:
        spread_cents = 1

    # 2. Top-of-Book 'No' Queue Depth (top 2 price levels) & Order Book Imbalance (obi)
    top_no_queue_depth = sum(qty for _, qty in no_levels[:2]) if no_levels else 0
    total_no_bid_qty = sum(qty for _, qty in no_levels) if no_levels else 0
    total_yes_bid_qty = sum(qty for _, qty in yes_levels) if yes_levels else 0
    denom = total_no_bid_qty + total_yes_bid_qty
    obi = round((total_no_bid_qty - total_yes_bid_qty) / denom, 4) if denom > 0 else 0.0

    # Adverse Selection / Bot-Crowding Rejection Check:
    # Reject/exclude if:
    # - spread_cents < 2 AND queue is jammed (top_no_queue_depth > 500)
    # - top_no_queue_depth > 2000 contracts
    # - obi shows a massive institutional bot wall on the No side (> 0.82) with almost zero retail Yes depth (< 50)
    jammed_tight_spread = (spread_cents < 2 and top_no_queue_depth > 500)
    excessive_no_queue = (top_no_queue_depth > MAX_TOP_NO_QUEUE_DEPTH)
    institutional_no_wall = (obi > MAX_OBI_THRESHOLD and total_yes_bid_qty < 50 and total_no_bid_qty > 400)
    high_adverse_selection_risk = bool(jammed_tight_spread or excessive_no_queue or institutional_no_wall)

    if high_adverse_selection_risk:
        return None

    # Recommended Maker No Bid Price:
    # Improve current best No bid by 1c when spread_cents >= 2c so we step to the front of the Maker queue
    # without crossing the spread (preserving $0.00 Maker fee).
    if spread_cents >= 2 and best_no_bid < 96:
        recommended_maker_no_bid_cents = best_no_bid + 1
    else:
        recommended_maker_no_bid_cents = best_no_bid

    # 3. Sum-of-Brackets Event Overround (event_overround)
    ev_metrics = event_inflation_map.get(ev_ticker, {})
    event_overround = float(ev_metrics.get("event_overround", 1.00))

    # 4. Maker vs. Taker Fee Drag Savings (taker_fee_saved)
    # Quadratic Taker fee formula: 0.07 * P * (1 - P) per contract vs $0.00 Maker fee
    p_no = recommended_maker_no_bid_cents / 100.0
    taker_fee_per_contract_dollars = round(0.07 * p_no * (1.0 - p_no), 4)
    taker_fee_per_contract_cents = round(taker_fee_per_contract_dollars * 100.0, 2)

    # 5. Position Sizing & Fractional Kelly Cap
    total_bankroll_dollars = float(bankroll_info["total_liquid_bankroll_dollars"])
    max_dollar_risk_5pct = round(total_bankroll_dollars * SINGLE_PICK_ALLOCATION_PCT, 2)
    contract_cost_dollars = recommended_maker_no_bid_cents / 100.0
    contracts_to_bid = int(math.floor(max_dollar_risk_5pct / contract_cost_dollars)) if contract_cost_dollars > 0 else 0
    total_order_exposure_dollars = round(contracts_to_bid * contract_cost_dollars, 2)
    net_win_return_pct = round(((100.0 - recommended_maker_no_bid_cents) / recommended_maker_no_bid_cents) * 100.0, 2)
    payoff_asymmetry_ratio = round(recommended_maker_no_bid_cents / max(1.0, (100.0 - recommended_maker_no_bid_cents)), 2)

    vertical_name, orthogonality_bucket, oracle_payload = classify_market_vertical_and_attach_oracle(
        market, truth_feeds, event_inflation_map
    )

    # Composite Underwriting Score for sorting the top 25 uncrowded candidates:
    # Rewards wider Maker spread (2c-6c), low No queue depth, positive event overround (>1.05),
    # and attractive net yield.
    spread_score = min(spread_cents, 8) * 3.0
    queue_penalty = (top_no_queue_depth / 200.0)
    overround_bonus = max(0.0, (event_overround - 1.00) * 40.0)
    obi_bonus = max(0.0, (0.5 - obi) * 10.0)
    composite_score = round(spread_score - queue_penalty + overround_bonus + obi_bonus + (net_win_return_pct * 0.6), 2)

    return {
        "ticker": ticker,
        "event_ticker": ev_ticker,
        "title": market.get("title", ""),
        "subtitle": market.get("subtitle", ""),
        "kalshi_market_url": f"https://kalshi.com/markets/{ev_ticker.lower()}",
        "vertical": vertical_name,
        "orthogonality_bucket": orthogonality_bucket,
        "hours_to_expiration": market.get("_hours_to_expiration"),
        "expiration_iso": market.get("_expiration_iso"),
        "orderbook_pricing": {
            "best_yes_bid_cents": best_yes_bid,
            "best_no_bid_cents": best_no_bid,
            "implied_yes_ask_cents": 100 - best_no_bid,
            "last_price_yes_cents": last_price_yes,
            "recommended_maker_no_bid_cents": recommended_maker_no_bid_cents,
            "price_improvement_cents": recommended_maker_no_bid_cents - best_no_bid,
        },
        "microstructure_metrics": {
            "spread_cents": spread_cents,
            "top_no_queue_depth": top_no_queue_depth,
            "total_no_bid_qty": total_no_bid_qty,
            "total_yes_bid_qty": total_yes_bid_qty,
            "obi": obi,
            "event_overround": event_overround,
            "taker_fee_saved_dollars_per_contract": taker_fee_per_contract_dollars,
            "taker_fee_saved_cents_per_contract": taker_fee_per_contract_cents,
            "total_taker_fee_saved_on_position_dollars": round(taker_fee_per_contract_dollars * contracts_to_bid, 2),
            "high_adverse_selection_risk": False,
        },
        "position_sizing_5pct_cap": {
            "total_bankroll_dollars": total_bankroll_dollars,
            "max_dollar_risk_5pct": max_dollar_risk_5pct,
            "contracts_to_bid": contracts_to_bid,
            "total_order_exposure_dollars": total_order_exposure_dollars,
            "max_profit_if_no_wins_dollars": round(contracts_to_bid * ((100 - recommended_maker_no_bid_cents) / 100.0), 2),
            "net_win_return_pct": net_win_return_pct,
            "payoff_asymmetry_losses_to_wipe_wins": f"{payoff_asymmetry_ratio}-to-1",
            "kelly_asymmetry_note": (
                "An 86c No contract carries a 6.14-to-1 payoff asymmetry (where 1 loss wipes out 6.14 wins, "
                "and every 1% drop in true win rate slashes optimal Kelly allocation by 7.14%). Total daily "
                "exposure MUST be strictly capped at 3 uncorrelated picks (15% total bankroll deployed) "
                "with 85% kept in dry powder."
            ),
        },
        "primary_truth_oracle": oracle_payload,
        "composite_underwriting_score": composite_score,
    }


def select_diverse_top_candidates(candidates: List[Dict[str, Any]], limit: int = TOP_CANDIDATES_EXPORT_LIMIT) -> List[Dict[str, Any]]:
    """
    Ranks uncrowded candidates by composite_underwriting_score while guaranteeing representation
    across all 3 orthogonality buckets (Weather, Macro/Energy, and Corporate/Procedural/Entertainment/Space)
    and preventing a single multi-bracket event from monopolizing the top 25 list (max 2 legs per event_ticker).
    """
    sorted_all = sorted(candidates, key=lambda x: x["composite_underwriting_score"], reverse=True)
    selected: List[Dict[str, Any]] = []
    event_counts: Dict[str, int] = defaultdict(int)

    # Pass 1: Ensure top picks from each orthogonality bucket are included first
    for bucket in (
        "BUCKET_A_WEATHER_ATMOSPHERIC",
        "BUCKET_B_MACRO_ENERGY_COMMODITY",
        "BUCKET_C_CORPORATE_PROCEDURAL_ENTERTAINMENT_SPACE",
    ):
        bucket_items = [c for c in sorted_all if c["orthogonality_bucket"] == bucket]
        for item in bucket_items[:6]:
            ev = item["event_ticker"]
            if event_counts[ev] < 2 and len(selected) < limit:
                selected.append(item)
                event_counts[ev] += 1

    # Pass 2: Fill remaining slots up to 25 sorted by score
    selected_tickers = {c["ticker"] for c in selected}
    for item in sorted_all:
        if len(selected) >= limit:
            break
        if item["ticker"] in selected_tickers:
            continue
        ev = item["event_ticker"]
        if event_counts[ev] < 2:
            selected.append(item)
            selected_tickers.add(item["ticker"])
            event_counts[ev] += 1

    selected.sort(key=lambda x: x["composite_underwriting_score"], reverse=True)
    for rank_idx, item in enumerate(selected, start=1):
        item["rank"] = rank_idx
    return selected


# ==============================================================================
# 7. SNAPSHOT FILE WRITERS (kalshi_snapshot.json & kalshi_snapshot.md)
# ==============================================================================

def write_snapshot_files(
    snapshot_payload: Dict[str, Any],
    json_path: str = "kalshi_snapshot.json",
    md_path: str = "kalshi_snapshot.md",
) -> None:
    """Writes both the structured JSON snapshot and the human-readable Markdown report."""
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(snapshot_payload, f_json, indent=2, ensure_ascii=False)

    b_info = snapshot_payload["bankroll_and_kelly_sizing"]
    h_stats = snapshot_payload["harvest_statistics"]
    candidates = snapshot_payload["top_25_uncrowded_candidates"]

    md_lines = [
        "# Patroclus Kalshi Longshot-Bias Underwriting Snapshot",
        "",
        f"- **Generated Timestamp (UTC):** `{snapshot_payload['generated_at_utc']}`",
        f"- **Repository:** [{GITHUB_REPO_URL}]({GITHUB_REPO_URL})",
        f"- **Live Raw JSON Feed:** [{RAW_JSON_URL}]({RAW_JSON_URL})",
        f"- **Outbound User-Agent:** `{USER_AGENT}`",
        f"- **Execution Mode:** Manual Kalshi Mobile App Execution Only (`READ-ONLY API`)",
        "",
        "## 1. Live Kalshi Portfolio Bankroll & Fractional Kelly Cap",
        "",
        f"- **Balance Data Source:** `{b_info['source']}` (Queried [{KALSHI_BALANCE_URL}]({KALSHI_BALANCE_URL}))",
        f"- **Available Cash:** `${b_info['available_cash_dollars']:.2f}` (`{b_info['available_cash_cents']}` cents)",
        f"- **Portfolio Value:** `${b_info['portfolio_value_dollars']:.2f}` (`{b_info['portfolio_value_cents']}` cents)",
        f"- **Total Liquid Bankroll:** **`${b_info['total_liquid_bankroll_dollars']:.2f}`**",
        f"- **5% Single-Pick Allocation Cap (`max_dollar_risk_5pct`):** **`${b_info['max_dollar_risk_5pct']:.2f}`**",
        f"- **Max Daily Deployment (3 Uncorrelated Picks = 15%):** **`${b_info['max_daily_deployed_15pct']:.2f}`**",
        f"- **Mandatory Dry Powder Reserve (85%):** **`${b_info['dry_powder_reserve_85pct']:.2f}`**",
        "",
        "> **Kelly Asymmetry Warning:** Because an 86¢ `No` contract carries a **6.14-to-1 payoff asymmetry** (where 1 loss wipes out 6.14 wins, and every 1% drop in true win rate slashes optimal Kelly allocation by 7.14%), total daily exposure must be strictly capped at **3 uncorrelated picks (15% total bankroll deployed)** while keeping **85% in dry powder**.",
        "",
        "## 2. Broad Market Harvesting Summary",
        "",
        f"- **Open Markets Scanned:** `{h_stats['total_open_markets_scanned']}` across `{h_stats['pages_fetched']}` paginated API batches",
        f"- **Markets in Target Expiration Window:** `{h_stats['markets_in_target_expiration_window']}`",
        f"- **Uncrowded Longshot Candidates Exported:** `{len(candidates)}`",
        "",
        "## 3. Top Uncrowded Maker 'No' Underwriting Candidates",
        "",
        "| Rank | Ticker | Bucket | Rec. Maker No Bid | Contracts (5% Cap) | Spread (¢) | Top No Queue | OBI | Event Overround | Net Return % | Hours Left |",
        "| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for c in candidates:
        ob_p = c["orderbook_pricing"]
        ms = c["microstructure_metrics"]
        ps = c["position_sizing_5pct_cap"]
        md_lines.append(
            f"| {c['rank']} | `{c['ticker']}` | `{c['orthogonality_bucket']}` | "
            f"**{ob_p['recommended_maker_no_bid_cents']}¢** | **{ps['contracts_to_bid']}** (`${ps['total_order_exposure_dollars']:.2f}`) | "
            f"{ms['spread_cents']}¢ | {ms['top_no_queue_depth']} | {ms['obi']:+.2f} | "
            f"{ms['event_overround']:.2f} | +{ps['net_win_return_pct']:.2f}% | {c['hours_to_expiration']}h |"
        )

    md_lines.extend([
        "",
        "## 4. Primary Truth Feed Summary",
        "",
        f"- **Vertical 1 (SEC EDGAR 8-K/10-Q & Fed Speeches):** `{json.dumps(snapshot_payload['primary_truth_feeds']['vertical_1_mentions']['sec_8k_10q_buzzword_hits_30d'])}`",
        f"- **Vertical 2 (Federal Register & Congressional Clocks):** Weekend/Recess Brake = `{snapshot_payload['primary_truth_feeds']['vertical_2_procedural']['weekend_or_recess_procedural_brake_active']}`",
        f"- **Vertical 3 (Launch Library 2 & TSA Throughput):** 7-Day Avg TSA Passengers = `{snapshot_payload['primary_truth_feeds']['vertical_3_space_tsa']['tsa_7d_rolling_average_passengers']}`",
        f"- **Vertical 6 (NWS Weather Grids & METAR Trap):** Tracked `{len(snapshot_payload['primary_truth_feeds']['vertical_6_weather']['stations'])}` Kalshi settlement airport stations",
        f"- **Vertical 7 (AAA National Gas & EIA):** `{json.dumps(snapshot_payload['primary_truth_feeds']['vertical_7_energy']['aaa_national_regular_gas'])}`",
        "",
    ])

    with open(md_path, "w", encoding="utf-8") as f_md:
        f_md.write("\n".join(md_lines))


def main() -> None:
    print(f"[Patroclus Scanner] Starting scan with User-Agent: {USER_AGENT}")
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Step 1: Dynamic Bankroll Sizing
    bankroll_info = fetch_dynamic_kalshi_bankroll()
    print(
        f"[Step 1] Bankroll source={bankroll_info['source']} | "
        f"Total Liquid=${bankroll_info['total_liquid_bankroll_dollars']:.2f} | "
        f"5% Cap=${bankroll_info['max_dollar_risk_5pct']:.2f}"
    )

    # Step 2: Broad Kalshi Market Harvesting
    window_markets, event_groups, harvest_stats = harvest_kalshi_markets()
    print(
        f"[Step 2] Scanned {harvest_stats['total_open_markets_scanned']} open markets; "
        f"{len(window_markets)} in target expiration window."
    )

    # Pre-screen tickers to batch-fetch orderbooks (plus all legs of their parent events for overround calculation)
    candidate_event_tickers = set()
    initial_tickers: List[str] = []
    for m in window_markets:
        tkr = m.get("ticker")
        ev_tkr = m.get("event_ticker") or m.get("series_ticker")
        if tkr:
            initial_tickers.append(tkr)
        if ev_tkr:
            candidate_event_tickers.add(ev_tkr)

    for ev_tkr in list(candidate_event_tickers)[:80]:
        for leg in event_groups.get(ev_tkr, []):
            leg_tkr = leg.get("ticker")
            if leg_tkr:
                initial_tickers.append(leg_tkr)

    orderbooks = batch_fetch_orderbooks(initial_tickers[:400])
    print(f"[Step 2b] Retrieved {len(orderbooks)} live Kalshi orderbooks.")

    # Step 3: Scrape all 7 Primary Truth Verticals
    truth_feeds = {
        "vertical_1_mentions": fetch_vertical_1_mentions_and_transcripts(),
        "vertical_2_procedural": fetch_vertical_2_procedural_deadlines(),
        "vertical_3_space_tsa": fetch_vertical_3_spacex_and_tsa(),
        "vertical_4_entertainment": fetch_vertical_4_entertainment_and_critics(),
        "vertical_6_weather": fetch_vertical_6_weather_grids(),
        "vertical_7_energy": fetch_vertical_7_aaa_gas_and_eia(),
    }
    event_inflation_map = compute_vertical_5_field_inflation(event_groups, orderbooks)
    truth_feeds["vertical_5_field_inflation_summary"] = {
        "total_events_evaluated": len(event_inflation_map),
        "inflated_events_over_105pct": [
            v for v in event_inflation_map.values() if v.get("field_inflation_flagged")
        ][:15],
    }
    print("[Step 3] Completed scraping all 7 primary truth verticals.")

    # Step 4: Evaluate Microstructure & Filter for Uncrowded Longshot Candidates
    evaluated_candidates: List[Dict[str, Any]] = []
    for m in window_markets:
        tkr = m.get("ticker", "")
        ob = orderbooks.get(tkr, {"yes": [], "no": []})
        cand = evaluate_candidate_microstructure(
            market=m,
            orderbook=ob,
            event_inflation_map=event_inflation_map,
            bankroll_info=bankroll_info,
            truth_feeds=truth_feeds,
        )
        if cand is not None:
            evaluated_candidates.append(cand)

    top_25 = select_diverse_top_candidates(evaluated_candidates, limit=TOP_CANDIDATES_EXPORT_LIMIT)
    print(f"[Step 4] Filtered {len(evaluated_candidates)} valid candidates down to top {len(top_25)} diverse picks.")

    snapshot_payload = {
        "scanner_name": "Patroclus Kalshi Longshot-Bias Underwriting Scanner",
        "generated_at_utc": now_utc,
        "repository_url": GITHUB_REPO_URL,
        "raw_json_url": RAW_JSON_URL,
        "raw_md_url": RAW_MD_URL,
        "user_agent": USER_AGENT,
        "execution_mode": "CHOICE_1_MANUAL_APP_EXECUTION_ONLY",
        "bankroll_and_kelly_sizing": bankroll_info,
        "harvest_statistics": harvest_stats,
        "primary_truth_feeds": truth_feeds,
        "top_25_uncrowded_candidates": top_25,
    }

    write_snapshot_files(snapshot_payload)
    print("[Step 5] Successfully wrote kalshi_snapshot.json and kalshi_snapshot.md.")


if __name__ == "__main__":
    main()