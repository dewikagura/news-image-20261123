# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/dewikagura/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/dewikagura/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-image front page summing up 23 November 2026's world news, for the
make.fun competition `news-image-20261123`.

## What the image shows

Masthead **WORLD NEWS** with the date **Monday, 23 November 2026**, then:

- **LEAD — CLIMATE: COP31 collapses, no climate deal.** Talks in Antalya
  ended without agreement after the EU and about 130 nations rejected a
  pact that omits fossil fuels. Stat panel: ≈130 nations backed a
  fossil-fuel mention; 2009 was the last summit collapse.
- **CONFLICT: Russian strike north of Kyiv kills at least 11.** A boy of 7
  was pulled alive from the rubble after 14 hours; a 79-year-old woman
  also survived.
- **MARKETS: AI sell-off sweeps global markets.** Friday's rout: Nikkei
  −5.1%, S&P 500 −3.7%. On Monday, gold rebounded about 2% and Brent
  crude held near $92.
- **JUSTICE: 'El Chapo Isidro' captured in Mexico.** FBI most-wanted
  fugitive Fausto Isidro Meza Flores was seized in Sinaloa; 11 died in
  the operation.
- **POLITICS: Democrats win 258 House seats.** Their largest US House
  majority since 1992, sealed by a North Carolina win; 44 seats gained.
- **SPORT: Alcaraz wins first ATP Finals title.** Beat world No. 1 Zverev
  6–2, 7–6 in Turin for his sixth title of 2026.
- **CONFLICT: Children killed as drones strike Khartoum.** Strikes hit
  homes in Khartoum and Omdurman and damaged a UN building.
- **IN BRIEF:** Gaza — Oxfam: war left a 'toxic wasteland', contamination
  signs across 99% of the Strip. Yemen — Houthis claim a Saudi refinery
  strike; Saudi jets hit Hodeidah; claims unverified. Travel — Belgium's
  airports shut in a strike; a Delta outage delays 3,500+ US flights.

## How the image was made

`tools/draw.py` draws the front page with Python PIL (DejaVu + Noto Serif
Display fonts) — crisp exact text, no AI-generated imagery. Re-run it to
regenerate `entry.png`:

```sh
python3 tools/draw.py
```

## Fact notes (verified 23 Nov 2026 against Reuters, BBC, AP, CNN, Oxfam, US DOJ)

- A Monday paper covers the weekend: several stories happened 20–22 Nov
  and were first reported / confirmed on 23 Nov (COP31 collapse and the
  Dymer strike on Sun 22 Nov; the El Chapo Isidro capture on Fri 20 Nov,
  announced 21 Nov). Nothing shown predates 20 Nov 2026.
- Markets: the Nikkei/S&P drops are Friday 20 Nov closes; Monday's moves
  are gold rebounding ~2% (spot gold ~$3,590, up ~2% after a ~9% weekly
  fall) and Brent near $92 — the brief's "gold +2.72%" and "oil near $90"
  were not used as stated because live prices showed ~+2% and ~$92.
- Sudan: Radio Dabanga reported five children killed; Al Jazeera reported
  four killed in total. The image gives no toll number, only that children
  were killed and a UN building was damaged.
- Houthi refinery claim is explicitly marked unverified (Reuters/Xinhua);
  Saudi authorities did not confirm it.
- Delta: 3,500+ flights delayed on Sun 22 Nov (weight-and-balance system
  outage, Atlanta ground stop), per the reported figure — higher than the
  1,600+ in the brief.
- Democrats' 258 seats: largest House majority since 1992 (which was also
  258); sealed Sun 22 Nov when Chuck Hubbard beat Virginia Foxx.

## Run it

```sh
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` is standard library only and just copies `entry.png` (1024×1024
PNG, ≤1 MiB). It runs twice with identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6t1r9fj9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
