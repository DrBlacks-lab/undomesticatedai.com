# Library candidate for Duet review

Status: built as an unpublished candidate. No merge or website deployment is authorized by this handoff. Garth decides whether to open the Library once it holds two or three finished pieces.

## Source and reuse

Base: `DrBlacks-lab/undomesticatedai.com` at `bc08f54b85848a0b065c34c3c9c618e98e7bd5ed`.

The complete starting tree was recovered and matched Git tree `3437799de262862bb4e9f143c0d497b390a85bb9`. Inspected and reused: `README.md`, both Village HTML routes, `village/village.css`, the original map, `style.css`, and the official channel registry in `identity/identity.json`. No repository-specific instruction file exists in this starting tree.

The unassigned east-side roundhouse becomes the fifth destination. Original artwork is byte-for-byte unchanged. Its Library polygon uses normalized map coordinates `81,48 84,46.8 88.5,50 89,55.5 85.5,60 80.3,58.7 79,54`; the card points at `84%,55%`. The same accessible anchor becomes a normal card at the existing mobile breakpoints.

The addition is a static media catalogue and a small authoring-time Python renderer. It generates ordinary HTML and native browser players; it adds no browser JavaScript, framework, third-party player or service.

## Media route

Selected route **(a)**: self-hosted MP4, with `media-src 'self'` on `/library/`. Frames remain explicitly blocked with `frame-src 'none'`; scripts and connections remain blocked. Other pages keep their existing policies. Official YouTube and TikTok links come from the existing identity registry and are ordinary outbound links, not embeds.

Reference: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/media-src>.

Ready items render a title, actual release date, description, Garth Noel byline and native player. Video uses controls, `playsinline`, `preload="none"`, a 9:16 display and optional captions/poster. Audio uses its native player and a download fallback. All media paths must resolve to nonempty files under `/library/media/`.

`The Vibe Coders` is registered as **in production**. No final MP4, poster or actual release date has been supplied. The page therefore presents a production notice and the existing essay link; it exposes no pretend player or invented date. Test fixture bytes are not published as media.

## Validation performed

- `python -B -m unittest discover -s tests -v`: **14 tests passed**, including video/audio markup, captions, strict date syntax, pending state, escaped content, rejected remote/traversal media paths, matching five-destination maps, official channel URLs and policy limits.
- `python -B tools/build_library.py --check`: passed.
- `python -B tools/build_library.py --check --release-check`: **expected exit 1**, with zero ready pieces. This is a content-presence check, not playback proof or publication authority.
- `git diff --check`: passed.
- Original map Git blob remains `f5a80f2f26d52f6791b75b8b334fa6f6431e660f`.

Browser/layout and real media playback remain unverified here. The browser panel could not open, and local HTTP requests were blocked by the execution environment. No screenshot-based visual pass is claimed.

## Live header read

Read-only HEAD of `https://undomesticatedai.com/` on 14 November 2026 at 23:16:28 UTC (19:16:28 Trinidad and Tobago): HTTP 200, GitHub server, `Content-Type: text/html; charset=utf-8`, `Content-Length: 4617`, `Accept-Ranges: bytes`. No `Content-Security-Policy` response header was present; the current root HTML supplies its CSP through a meta tag. This observation covers the root response at that time, not every route or a future deployment.

## Duet acceptance pass

1. Serve this branch locally and inspect `/` and `/village/` at desktop, tablet, phone and short landscape sizes. Check the east-side polygon, label placement, card reflow, keyboard focus and unchanged existing destinations.
2. Open `/library/` through both map links. Confirm the pending item, Garth Noel byline and outbound channel links. The first media file is still required.
3. Once the real assets arrive, add them under `library/media/`, enter the actual release dates and `ready` status in `library/items.json`, and run `python tools/build_library.py`.
4. Test the actual MP4/audio codecs, seeking, volume, captions, download fallback and portrait fit in the browser. Check response MIME types and byte-range behavior on the eventual host. Static tests do not establish these.
5. Repeat the consistency and release checks. Two pieces meet the minimum check; Garth may choose to wait for three.
6. Only after Garth explicitly approves opening: update the closed-page copy, remove the `noindex,nofollow` indexing hint, add `/library/` to the sitemap and merge/deploy the reviewed source. The indexing hint is not access control. Until then keep this candidate off the live publishing branch.

## Other reported work

PR #1 remains a separate conflicted draft; no conflict repair or merge is included. The two near-duplicate Notes introduction lines remain for a separate copy decision. The approved Wiki content and all current essays are untouched.
