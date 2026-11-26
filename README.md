# news-25-b152-numbers

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b152-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b152-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

Sum up Wednesday 25 November 2026's world news in one image — **50 stories**:
3 heroes + 10 cards + 37 also today, plus a world map and a DATE CHECK.

## Top stories

1. **Trump hits 14 partners with new tariffs** — China faces 20%, the highest
   rate, up to 40% if the truce fails. *Why it matters: a wider trade war now
   threatens global growth.*
2. **Kospi crashes 6.16% in a chip rout** — Samsung −9.87%, Hynix −11.05%.
   *Why it matters: Asia's tech selloff wipes billions in value.*
3. **Shenzhou-24 docks after a 3.5-hour flight** — launched 08:18 Beijing time;
   first foreign astronaut, Pakistan's Ali, 40. *Why it matters: China's
   station opens its doors to new partners.*

## How it is built

- `gen.py` renders `entry.png` (1024×1024) at build time with Pillow.
- `main.py` is stdlib-only: it copies `entry.png` into
  `$MAKEFUN_OUTPUT_DIR/entry.png`.

Legend: `[C]` confirmed, `[R]` reported, `[CL]` claim — every card and every
ALSO item carries one. The DATE CHECK box lists only stories that are NOT
25 November, so nothing stale slips into the front page.
