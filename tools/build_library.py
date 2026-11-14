"""Render the static Library catalogue. No browser JavaScript or third-party players.

This builds an unpublished candidate. It cannot authorize or perform publication.
"""
from __future__ import annotations

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
POLICY = "default-src 'none'; base-uri 'none'; object-src 'none'; form-action 'none'; script-src 'none'; connect-src 'none'; img-src 'self'; style-src 'self'; font-src 'self'; media-src 'self'; frame-src 'none'"
EXTENSIONS = {"video": {".mp4": "video/mp4"}, "audio": {".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".ogg": "audio/ogg", ".wav": "audio/wav"}}


def local_asset(value: str | None, root: Path, suffixes: set[str]) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Asset path must be text")
    parsed = urlsplit(value)
    parts = PurePosixPath(parsed.path).parts
    if (parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or not value.startswith("/library/media/")
            or any(p in {".", ".."} for p in parts) or "\\" in value or "%" in value):
        raise ValueError("Media must use an unambiguous /library/media/ path")
    target = (root / value.lstrip("/")).resolve()
    if not target.is_relative_to((root / "library" / "media").resolve()) or target.suffix.lower() not in suffixes:
        raise ValueError("Unsupported media asset")
    if not target.is_file() or target.stat().st_size == 0:
        raise ValueError("Media asset is missing or empty")
    return value


def validate_items(items: list[dict], root: Path) -> list[dict]:
    if not isinstance(items, list):
        raise ValueError("The catalogue must be a list")
    seen = set()
    for item in items:
        if not isinstance(item, dict) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", item.get("id", "")):
            raise ValueError("Every item needs a stable id")
        if item["id"] in seen:
            raise ValueError("Duplicate catalogue id")
        seen.add(item["id"])
        if item.get("kind") not in EXTENSIONS or item.get("status") not in {"production", "ready"}:
            raise ValueError("Unknown media kind or status")
        if any(not isinstance(item.get(key), str) or not item[key].strip() for key in ("title", "description")):
            raise ValueError("Title and description are required")
        if item.get("essay") not in {None, "/essays/the-vibe-coders/"}:
            raise ValueError("Use the approved related essay or omit it")
        for key, suffixes in (("poster", {".webp", ".png", ".jpg", ".jpeg"}), ("captions", {".vtt"}), ("transcript", {".txt", ".html"})):
            local_asset(item.get(key), root, suffixes)
        if item["status"] == "ready":
            if not isinstance(item.get("date"), str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item["date"]):
                raise ValueError("A ready item needs its actual release date")
            date.fromisoformat(item["date"])
            if local_asset(item.get("src"), root, set(EXTENSIONS[item["kind"]])) is None:
                raise ValueError("A ready item needs a local media file")
        elif item.get("src") is not None or item.get("date") is not None:
            raise ValueError("A production item cannot claim a playable source or release date")
    return items


def render_item(item: dict) -> str:
    text = lambda value: escape(str(value), quote=True)
    ready = item["status"] == "ready"
    when = (f'<time datetime="{item["date"]}">{date.fromisoformat(item["date"]).strftime("%d %B %Y")}</time>'
            if ready else '<span>In production</span>')
    player = '<div class="media-pending"><span class="media-pending-mark" aria-hidden="true">\u25cb</span><p>This piece is being prepared. Playback will be available here when it is released.</p></div>'
    links = []
    if ready:
        kind = item["kind"]
        mime = EXTENSIONS[kind][Path(item["src"]).suffix.lower()]
        attrs = f' class="media-player" controls preload="none" aria-label="{text(item["title"])}"'
        if kind == "video":
            attrs += ' playsinline width="540" height="960"'
            if item.get("poster"):
                attrs += f' poster="{text(item["poster"])}"'
        track = (f'<track kind="captions" src="{text(item["captions"])}" srclang="en" label="English" default>'
                 if item.get("captions") and kind == "video" else '')
        player = f'<{kind}{attrs}><source src="{text(item["src"])}" type="{mime}">{track}<p>Your browser does not support this player. Use the download link below.</p></{kind}>'
        links.append(f'<a href="{text(item["src"])}" download>Download {kind}</a>')
    if item.get("transcript"):
        links.append(f'<a href="{text(item["transcript"])}">Read the transcript</a>')
    if item.get("essay"):
        links.append(f'<a href="{text(item["essay"])}">Read the essay</a>')
    return f'''<li><article class="library-item" id="{item['id']}" aria-labelledby="{item['id']}-title">
<div class="media-meta"><span>{item['kind'].title()}</span>{when}</div>
<h2 id="{item['id']}-title">{text(item['title'])}</h2>
<p class="media-byline">Garth Noel</p>
<p class="media-description">{text(item['description'])}</p>
{player}
<div class="media-links">{' '.join(links)}</div>
</article></li>'''


def render(items: list[dict]) -> str:
    listing = "\n".join(render_item(item) for item in items)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{POLICY}">
<meta name="referrer" content="no-referrer">
<meta name="robots" content="noindex,nofollow">
<title>Library — Undomesticated AI</title>
<meta name="description" content="Video and audio by Garth Noel from Undomesticated AI.">
<meta name="author" content="Garth Noel">
<link rel="canonical" href="https://undomesticatedai.com/library/">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../style.css">
<link rel="stylesheet" href="library.css">
</head>
<body>
<header class="mast wrap"><div class="toprule"></div><div class="mastrow">
<a class="brand" href="../">Undomesticated AI</a>
<nav class="nav" aria-label="Primary"><a href="../">Village</a><a href="../essays/">Essays</a><a href="../notes/">Notes</a><a href="./" aria-current="page">Library</a><a href="../about/">About</a></nav>
</div></header>
<main id="main">
<section class="pagehero wrap"><p class="kicker">The Village Library</p><h1>Watch.<br>Listen.</h1>
<p class="library-intro">Video and audio from Undomesticated AI. Essays take another form here.</p>
<p class="library-status">The collection is being prepared. The Library is not open yet.</p></section>
<section class="gridsec wrap library-body" aria-labelledby="collection-title"><div class="rail" id="collection-title">The collection</div><div class="body">
<ul class="library-list">{listing}</ul>
<aside class="library-elsewhere" aria-label="Official channels"><p>Find Undomesticated AI elsewhere.</p><div class="linkrow"><a href="https://www.youtube.com/@UndomesticatedAI" rel="external noreferrer">YouTube ↗</a><a href="https://www.tiktok.com/@undomesticatedai" rel="external noreferrer">TikTok ↗</a></div></aside>
</div></section>
</main>
<footer class="footer wrap"><div class="footergrid"><span>UNDOMESTICATED AI · LIBRARY · GARTH NOEL</span><span><a href="../">Back to the Village</a> · <a href="../identity/">Official identity</a></span></div></footer>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check that generated HTML matches its catalogue")
    parser.add_argument("--release-check", action="store_true", help="Check for at least two ready pieces; grants no publication approval")
    args = parser.parse_args()
    items = validate_items(json.loads((ROOT / "library" / "items.json").read_text(encoding="utf-8")), ROOT)
    output = render(items)
    target = ROOT / "library" / "index.html"
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != output:
            parser.exit(1, "Library HTML is stale. Run tools/build_library.py.\n")
    else:
        target.write_text(output, encoding="utf-8", newline="\n")
    ready = sum(item["status"] == "ready" for item in items)
    print(f"Library: {len(items)} catalogue item(s), {ready} ready piece(s). Candidate remains unpublished.")
    if args.release_check and ready < 2:
        parser.exit(1, "Opening condition unmet: at least two ready pieces are required. Garth still decides whether to open.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
