"""Fetch kernel releases (kernel.org) and Linux headlines (LWN) into news.json.

Runs in GitHub Actions twice a day. Standard library only.
"""
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

IST = timezone(timedelta(hours=5, minutes=30))
OUT = Path(__file__).resolve().parent.parent / "news.json"
UA = {"User-Agent": "the-machine-bot/1.0 (+https://github.com)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def kernels():
    data = json.loads(get("https://www.kernel.org/releases.json"))
    out = []
    for r in data.get("releases", []):
        out.append({
            "moniker": r.get("moniker"),
            "version": r.get("version"),
            "date": (r.get("released") or {}).get("isodate"),
            "eol": bool(r.get("iseol")),
            "link": r.get("changelog") or r.get("gitweb") or "https://www.kernel.org/",
        })
    return out


def lwn(limit=12):
    root = ET.fromstring(get("https://lwn.net/headlines/rss"))
    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        if title.lower().startswith("security updates for"):
            continue  # daily distro advisories: noisy for interview prep
        try:
            dt = parsedate_to_datetime(it.findtext("pubDate")).astimezone(IST).isoformat(timespec="minutes")
        except Exception:
            dt = None
        paid = title.startswith("[$]")
        items.append({
            "t": title[3:].strip() if paid else title,
            "link": (it.findtext("link") or "").strip(),
            "date": dt,
            "subscriber": paid,
        })
        if len(items) >= limit:
            break
    return items


def main():
    data = {"updated": datetime.now(IST).isoformat(timespec="minutes"), "kernels": [], "lwn": []}
    try:
        data["kernels"] = kernels()
    except Exception as e:
        print(f"warn: kernel.org: {e}")
    try:
        data["lwn"] = lwn()
    except Exception as e:
        print(f"warn: lwn: {e}")
    if not data["kernels"] and not data["lwn"]:
        raise SystemExit("Nothing fetched; keeping the previous news.json")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(data['kernels'])} releases, {len(data['lwn'])} headlines")


if __name__ == "__main__":
    main()
