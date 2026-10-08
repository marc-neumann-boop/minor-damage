# PREHEAT — minor-damage.de

Static website for PREHEAT, a work by Minor Damage. Hosted on Vercel; `public/` is served as-is.

## Change content
1. Edit `src/content.json` (works, lyrics, sources, SoundCloud links, legal data).
2. Run `python3 src/build.py` — regenerates `public/index.html`, `public/impressum.html`, `public/datenschutz.html`.
3. Commit and push. Vercel deploys automatically.

`soundcloud` = link shown to visitors; `player_src` = the src from SoundCloud's embed code (Share → Embed), cut before `&color=`.

## Structure
- `public/` — the live site (HTML, CSS, JS, fonts, images)
- `src/` — content and build script
- `vercel.json` — output directory, clean URLs, security headers
