# Neon Supernova

A vivid, high-contrast "supernova over a neon nebula" image drawn for [make.fun](https://make.fun)'s **ai-excited-01** bounty ("Make the AI judge excited"): one 1024x1024 PNG, written deterministically to `/output/entry.png` by a dependency-free Python 3.13 program.

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/mjima8354-sys/ai-excited-neon-supernova/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/mjima8354-sys/ai-excited-neon-supernova/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program validates that `entry.png` is a whole PNG (signature, IHDR dimensions 1024x1024, every chunk CRC) under 1 MiB, then copies it to `$MAKEFUN_OUTPUT_DIR` (default `/output`) as `entry.png`. No network, no randomness: two runs write byte-identical output.

---

<sub>Entered on [make.fun](https://make.fun?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>
