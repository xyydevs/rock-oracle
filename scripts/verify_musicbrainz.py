#!/usr/bin/env python3
"""Verify that a song exists in MusicBrainz.

Usage:
  verify_musicbrainz.py "Song Title" "Artist Name"
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path


MUSICBRAINZ_RECORDING_URL = "https://musicbrainz.org/ws/2/recording/"
USER_AGENT = "rock-oracle-skill/1.0 (https://github.com/xyydevs/rock-oracle)"
CA_BUNDLE_CANDIDATES = (
    "/etc/ssl/cert.pem",
    "/private/etc/ssl/cert.pem",
)


def normalize(value: str) -> str:
    return " ".join(value.casefold().replace("&", "and").split())


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, normalize(left), normalize(right)).ratio()


def query_musicbrainz(title: str, artist: str, limit: int) -> dict:
    query = f'recording:"{title}" AND artist:"{artist}"'
    params = urllib.parse.urlencode(
        {
            "query": query,
            "fmt": "json",
            "limit": str(limit),
        }
    )
    request = urllib.request.Request(
        f"{MUSICBRAINZ_RECORDING_URL}?{params}",
        headers={"User-Agent": USER_AGENT},
    )
    context = ssl.create_default_context(cafile=find_ca_bundle())
    with urllib.request.urlopen(request, timeout=12, context=context) as response:
        return json.loads(response.read().decode("utf-8"))


def find_ca_bundle() -> str | None:
    for candidate in CA_BUNDLE_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    try:
        import certifi  # type: ignore
    except ImportError:
        return None
    return certifi.where()


def extract_year(recording: dict) -> str | None:
    for release in recording.get("releases", []):
        date = release.get("date")
        if date and len(date) >= 4 and date[:4].isdigit():
            return date[:4]
    first_release_date = recording.get("first-release-date")
    if first_release_date and len(first_release_date) >= 4:
        return first_release_date[:4]
    return None


def artist_credit_name(recording: dict) -> str:
    credits = recording.get("artist-credit", [])
    parts: list[str] = []
    for credit in credits:
        if isinstance(credit, dict):
            parts.append(credit.get("name") or credit.get("artist", {}).get("name", ""))
        elif isinstance(credit, str):
            parts.append(credit)
    return "".join(parts).strip()


def score_recording(recording: dict, title: str, artist: str) -> float:
    title_score = similarity(recording.get("title", ""), title)
    artist_score = similarity(artist_credit_name(recording), artist)
    ext_score = float(recording.get("ext:score", 0)) / 100.0
    return (title_score * 0.45) + (artist_score * 0.45) + (ext_score * 0.10)


def verify(title: str, artist: str, limit: int) -> dict:
    started = time.time()
    try:
        payload = query_musicbrainz(title, artist, limit)
    except urllib.error.HTTPError as exc:
        return {
            "ok": False,
            "error": f"musicbrainz_http_{exc.code}",
            "title": title,
            "artist": artist,
        }
    except (urllib.error.URLError, TimeoutError) as exc:
        return {
            "ok": False,
            "error": "musicbrainz_unavailable",
            "detail": str(exc),
            "title": title,
            "artist": artist,
        }
    except json.JSONDecodeError:
        return {
            "ok": False,
            "error": "invalid_musicbrainz_response",
            "title": title,
            "artist": artist,
        }

    recordings = payload.get("recordings", [])
    if not recordings:
        return {"ok": False, "error": "no_match", "title": title, "artist": artist}

    best = max(recordings, key=lambda item: score_recording(item, title, artist))
    confidence = round(score_recording(best, title, artist), 3)
    matched_artist = artist_credit_name(best)
    matched_title = best.get("title", "")

    ok = confidence >= 0.78 and similarity(matched_title, title) >= 0.72
    result = {
        "ok": ok,
        "confidence": confidence,
        "title": matched_title or title,
        "artist": matched_artist or artist,
        "year": extract_year(best),
        "musicbrainz_id": best.get("id"),
        "musicbrainz_url": f"https://musicbrainz.org/recording/{best.get('id')}"
        if best.get("id")
        else None,
        "elapsed_ms": int((time.time() - started) * 1000),
    }
    if not ok:
        result["error"] = "low_confidence_match"
        result["requested_title"] = title
        result["requested_artist"] = artist
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a song with MusicBrainz.")
    parser.add_argument("title", help="Song title to verify")
    parser.add_argument("artist", help="Artist name to verify")
    parser.add_argument("--limit", type=int, default=5, help="MusicBrainz result limit")
    args = parser.parse_args()

    print(
        json.dumps(
            verify(args.title, args.artist, max(1, min(args.limit, 25))),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
