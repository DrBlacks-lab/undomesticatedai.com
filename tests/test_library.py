"""Content and policy checks for the unpublished static Library candidate.

Fixture media bytes exercise HTML generation only; they are not playback evidence.
"""
from __future__ import annotations

import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_library", ROOT / "tools" / "build_library.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def named(self, tag):
        return [attrs for kind, attrs in self.tags if kind == tag]


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.item = json.loads((ROOT / "library" / "items.json").read_text(encoding="utf-8"))[0]

    def ready(self, root, kind="video"):
        media = root / "library" / "media"
        media.mkdir(parents=True)
        extension = ".mp4" if kind == "video" else ".mp3"
        (media / ("sample" + extension)).write_bytes(b"synthetic fixture only")
        item = dict(self.item, kind=kind, status="ready", date="2026-11-14", src="/library/media/sample" + extension)
        return item

    def test_pending_piece_claims_neither_date_nor_playback(self):
        build.validate_items([self.item], ROOT)
        page = Elements(build.render([self.item]))
        self.assertFalse(page.named("video") or page.named("audio") or page.named("time"))
        self.assertIn("In production", build.render([self.item]))
        self.assertIn("Garth Noel", build.render([self.item]))

    def test_ready_portrait_video_has_native_controls_and_caption_track(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            item = self.ready(root)
            (root / "library" / "media" / "captions.vtt").write_text("WEBVTT\n", encoding="utf-8")
            item["captions"] = "/library/media/captions.vtt"
            build.validate_items([item], root)
            page = Elements(build.render([item]))
            video = page.named("video")[0]
            self.assertIn("controls", video)
            self.assertIn("playsinline", video)
            self.assertNotIn("autoplay", video)
            self.assertEqual(video["preload"], "none")
            self.assertEqual((video["width"], video["height"]), ("540", "960"))
            self.assertEqual(page.named("source")[0]["type"], "video/mp4")
            self.assertEqual(page.named("track")[0]["kind"], "captions")
            self.assertEqual(page.named("time")[0]["datetime"], "2026-11-14")

    def test_audio_uses_native_audio_player(self):
        with tempfile.TemporaryDirectory() as temp:
            item = self.ready(Path(temp), "audio")
            build.validate_items([item], Path(temp))
            page = Elements(build.render([item]))
            self.assertEqual(len(page.named("audio")), 1)
            self.assertFalse(page.named("video"))
            self.assertEqual(page.named("source")[0]["type"], "audio/mpeg")
            self.assertTrue(any("download" in a for a in page.named("a")))

    def test_external_and_ambiguous_media_sources_are_rejected(self):
        for source in ("https://example.com/movie.mp4", "//example.com/movie.mp4", "data:video/mp4,x", "/library/media/../movie.mp4", "/library/media/%2e%2e/movie.mp4", "/library/media/a.mp4?x=1", "/library/media/a.mp4#x", "/library/media/a\\b.mp4"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                build.local_asset(source, ROOT, {".mp4"})

    def test_missing_media_cannot_be_marked_ready(self):
        with self.assertRaises(ValueError):
            build.validate_items([dict(self.item, status="ready", date="2026-11-14", src="/library/media/missing.mp4")], ROOT)

    def test_release_date_is_required_and_not_invented(self):
        with tempfile.TemporaryDirectory() as temp:
            item = self.ready(Path(temp))
            for value in (None, "2026-02-30", "coming soon", "20261114", "2026-W46-6"):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    build.validate_items([dict(item, date=value)], Path(temp))

    def test_production_cannot_claim_a_ready_source(self):
        with self.assertRaises(ValueError):
            build.validate_items([dict(self.item, src="/library/media/sample.mp4")], ROOT)

    def test_duplicate_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            build.validate_items([self.item, copy.deepcopy(self.item)], ROOT)

    def test_catalogue_text_is_escaped(self):
        page = build.render([dict(self.item, title='<script>alert("x")</script>', description='<img src=x onerror="alert(1)">')])
        self.assertFalse(Elements(page).named("script") or Elements(page).named("img"))

    def test_policy_allows_only_local_media_and_no_scripts_or_frames(self):
        page = Elements(build.render([self.item]))
        policy = next(m["content"] for m in page.named("meta") if m.get("http-equiv") == "Content-Security-Policy")
        directives = {entry.strip().split()[0]: entry.strip().split()[1:] for entry in policy.split(";")}
        self.assertEqual(directives["media-src"], ["'self'"])
        self.assertEqual(directives["frame-src"], ["'none'"])
        self.assertEqual(directives["script-src"], ["'none'"])
        self.assertEqual(directives["connect-src"], ["'none'"])
        self.assertFalse(page.named("iframe") or page.named("script"))

    def test_official_outbound_channels_match_existing_registry(self):
        identity = json.loads((ROOT / "identity" / "identity.json").read_text(encoding="utf-8"))
        expected = {s["url"] for s in identity["official_surfaces"] if s.get("provider") in {"YouTube", "TikTok"}}
        actual = {a["href"] for a in Elements(build.render([self.item])).named("a") if a.get("rel") == "external noreferrer"}
        self.assertEqual(actual, expected)

    def test_both_village_routes_have_five_matching_destinations(self):
        for file in (ROOT / "index.html", ROOT / "village" / "index.html"):
            page = Elements(file.read_text(encoding="utf-8"))
            cards = [a for a in page.named("a") if "data-building-id" in a]
            self.assertEqual(len(cards), 5)
            self.assertEqual(len(page.named("polygon")), 5)
            library = next(a for a in cards if a["data-building-id"] == "library")
            self.assertEqual(library["href"], "/library/")
            self.assertTrue(any(a.get("href") == "/library/" and a.get("aria-label") == "Library — video and audio" for a in page.named("a")))

    def test_unopened_library_remains_out_of_sitemap(self):
        self.assertNotIn("/library/", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertTrue(any(m.get("name") == "robots" and m["content"] == "noindex,nofollow" for m in Elements(build.render([self.item])).named("meta")))

    def test_generated_page_is_current(self):
        self.assertEqual((ROOT / "library" / "index.html").read_text(encoding="utf-8"), build.render([self.item]))


if __name__ == "__main__":
    unittest.main()
