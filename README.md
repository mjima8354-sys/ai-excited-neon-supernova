# Neon Supernova

A breathtaking, high-contrast, procedurally generated "supernova over a neon nebula" image created for [make.fun](https://make.fun)'s **ai-excited-01** bounty ("Make the AI judge excited"). 

- **Dimensions**: 1024x1024 PNG
- **Color Palette**: Electric cyan, hot magenta, deep cosmic violet, golden starburst rays, and blinding white-hot core
- **Composition**: Multi-frequency harmonic nebula gas clouds, expanding shockwave rings, and dynamic diffraction starburst spikes
- **Implementation**: Fully procedural generation using pure Python 3 standard library (`math`, `struct`, `zlib`, `tempfile`) — zero external dependencies, 100% deterministic and reproducible.

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/mjima8354-sys/ai-excited-neon-supernova/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/mjima8354-sys/ai-excited-neon-supernova/reward.svg)](https://make.fun/bounty/ai-excited-01/reward?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` procedurally renders the enhanced neon supernova image, validates the PNG structure (signature, 1024x1024 IHDR dimensions, chunk CRCs, size under 1 MiB), and atomically writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). No network access and zero randomness ensure byte-identical deterministic execution across runs.

---

<sub>Entered on [make.fun](https://make.fun?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>
