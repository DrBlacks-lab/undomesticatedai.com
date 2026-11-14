# Library media

Self-hosted video uses MP4. Audio may use MP3, M4A, Ogg or WAV. Keep files here and register their root-relative paths in `library/items.json`.

Use the actual release date when a piece is ready. Supply a poster when available and English WebVTT captions for spoken video. Add a transcript where useful. Do not mark an unfinished piece as ready.

Run `python tools/build_library.py` after catalogue changes. The output is static HTML with native browser players, no autoplay, no script, and no embedded third-party player. Media uses `preload="none"`; portrait video uses a 9:16 frame and preserves its full image.

The content policy allows `media-src 'self'` only on the Library page and explicitly blocks frames. YouTube and TikTok are ordinary outbound links to the existing official channels.

`python tools/build_library.py --check --release-check` checks source consistency and the minimum of two ready pieces. It does not verify codecs, creative quality or grant publication approval. Test real playback and captions in Duet's browser. Garth decides whether to open with two or three pieces.

The candidate stays off `main` until review and Garth's explicit approval. Its `noindex,nofollow` tag is an indexing hint, not access control. Before an approved opening, update the opening copy, remove the indexing hint, add `/library/` to `sitemap.xml`, and verify the final live policy and media responses. No automatic deployment is provided.
