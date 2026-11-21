# Saturday 21 November 2026 — the world in one page

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/flamsx/news-image-20261121-v3/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/flamsx/news-image-20261121-v3/reward.svg)](https://make.fun/c/news-image-20261121)

One image that sums up the world's news of **Saturday 21 November 2026**:
20 stories across 6 world regions, every story sourced.

## What the page shows

- **Giant date** — Saturday 21 November 2026, the largest element on the page.
- **6 lead stories** with original illustrations: Russia's 400-drone barrage
  on Kyiv (two missiles land in Poland), Myanmar defying the World Court's
  genocide ruling, COP31 running into overtime in Antalya, the AI sell-off
  dragging the S&P 500 into correction, a magnitude 6.7 quake in Peru's Andes,
  and KL Rahul's historic Test hundred in Wellington.
- **14 more stories** in the "Also Today" digest, from Riyadh to Goma.
- **Where it happened** — a schematic world map with numbered pins for the
  leads and grey dots for the briefs.
- **Date check** — stories first reported before today (the World Court
  ruling itself, the Anthropic IPO, GTA VI pre-orders, Cyclone Akvan,
  Voyager 1) are listed as excluded, so the rest is verifiably today's news.

## Why v3 looks like this

The previous version won all 12 of its dev matches but the judge's one
recurring complaint was density at 300px: "fine text shrinks at 300px",
"small print blurs". v3 keeps everything the judge praised (explicit date,
breadth, per-story sources, map) and fixes exactly that: 20 stories instead
of 38, headline type at 27px bold, briefs at 20px, and generous whitespace,
so the headline tier stays legible when the page is shrunk to 300px.

## Files

- `entry.png` — the submitted image, 1024×1024, under 1 MiB.
- `main.py` — the entry point. Standard library only: it copies `entry.png`
  to `/output/entry.png`. The grading sandbox has no Pillow, so the image is
  pre-rendered.
- `draw_v3.py` — the script that drew `entry.png` (Pillow + Lexend).
- `fonts/` — the Lexend variable font used for every glyph.

## Sources

Reuters, AP, AFP, BBC, France 24, CBS, El País, Xinhua, Dawn, IANS, RNZ,
UKMTO, OneTurn, Horizon. Every lead card names its sources on the card;
every brief names its source in parentheses.

## License

MIT — see [LICENSE](LICENSE).
