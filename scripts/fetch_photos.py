#!/usr/bin/env python3
"""Save booking photos named in the editions into data/photos/, so the site serves its own copy.

An entry, or a row of filings.new_list, may carry  "photo": {"url": "https://ssmugshots.blob.core.windows.net/images/...jpg", "booking": "Bkg #255702"}
(see README, "Booking photos"). This script downloads each such image once, to data/photos/<booking digits>.jpg.
Only the Baldwin County jail roster's image host is accepted. Entries the builder would refuse to show
(see build.photo_allowed) are skipped, so a disallowed photo never lands in the repo.
Exit 0 always unless a download fails; a failed download exits 1 so the workflow shows red.
"""
import json, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from build import photo_allowed, photo_key, row_photo_key, PHOTO_HOST_RE  # noqa: E402

PHOTOS = ROOT / "data" / "photos"
UA = {"User-Agent": "Mozilla/5.0 (alacrime.com site builder)"}


def main():
    PHOTOS.mkdir(parents=True, exist_ok=True)
    saved, errors = [], []
    for f in sorted((ROOT / "data" / "editions").glob("*.json")):
        ed = json.loads(f.read_text())
        items = [(en, photo_key(en) if en.get("photo") and photo_allowed(en) else None, en.get("id"))
                 for en in ed.get("entries", [])]
        items += [(n, row_photo_key(n), n.get("case")) for n in (ed.get("filings") or {}).get("new_list", [])]
        for en, key, label in items:
            ph = en.get("photo")
            if not ph or not key:
                continue
            url = ph.get("url", "")
            if not key or not PHOTO_HOST_RE.match(url):
                errors.append(f"{f.stem} {label}: photo url or booking not acceptable")
                continue
            out = PHOTOS / f"{key}.jpg"
            if out.exists():
                continue
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                    data = r.read()
                if not data.startswith(b"\xff\xd8") or len(data) > 2_000_000:
                    raise ValueError("not a JPEG or too large")
                out.write_bytes(data)
                saved.append(key)
            except Exception as err:
                errors.append(f"{f.stem} {label}: {err}")
    print("Photos saved:", ", ".join(saved) if saved else "none new")
    if errors:
        print("PHOTO ERRORS:\n  " + "\n  ".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
