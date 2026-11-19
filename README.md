# The World in One Image — 19 November 2026

[![News Image 20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/renprayoga/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261119/renprayoga/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

One poster that sums up Thursday, 19 November 2026, drawn entirely in code — no photographs, no downloads, no randomness. Every line, flag and letter is plotted by `draw.py` with Pillow, so the same command always produces the same picture.

## What the image says

The front page leads with the day's biggest story and then gives three more, plus a short "Also" strip at the bottom.

**GTA VI is here (hero).** After thirteen years of waiting, Grand Theft Auto VI is playable worldwide from midnight local time on 19 November, on PlayStation 5 and Xbox. The game returns to Vice City with two protagonists, Lucia Caminos and Jason Duval. The hero panel shows that homecoming as a Vice City sunset over a lit-up skyline.

**Trump, Xi and Putin meet in Shenzhen.** The three presidents sit down together for the first time — a trilateral meeting of three nuclear powers, held on the sidelines of APEC. Nuclear arms, Iran and Ukraine are on the agenda. At the time this image was made, the meeting had produced no outcome yet.

**Gulf war widens: Iran hits US bases.** Iran struck American bases in Kuwait (Ali Al Salem) and Bahrain, answering the US strike on Qeshm Island. The attacks were intercepted, and no casualties or damage were reported.

**Europe unites for Ukraine in Berlin.** The European allies of the Coalition of the Willing met in Berlin, joined by the US envoys Witkoff and Kushner.

**Also:** NASA briefed on Voyager 1, now a full light-day from Earth, and Cyclone Akvan approached the coast of India.

## How to run it

```bash
python3 draw.py          # draws entry.png (1024x1024, under 1 MiB)
python3 main.py          # copies entry.png into ./output/
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # ...or into a folder you choose
```

Requirements: Python 3 and Pillow (`pip install pillow`). Nothing else — no network, no API keys, no fonts to fetch; the DejaVu fonts already on the system are used.

## Sources

- AP
- Reuters
- BBC
- NASA
- The Hindu

## License

MIT — see [LICENSE](LICENSE).
