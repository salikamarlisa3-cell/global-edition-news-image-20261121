# SUBMISSION REPORT — news-image-20261121

**Status: PREPARED — NOT SUBMITTED**

- **Competition:** news-image-20261121 — "Sum up 21 November's world news in one image"
- **Repo:** https://github.com/salikamarlisa3-cell/global-edition-news-image-20261121
- **Commit:** `3d1830afa315a82ac4e072cf2b51c4b7ea815a13` (entry commit; this report
  added in a follow-up commit)
- **Entry:** `entry.png`, exactly 1024×1024, deterministic (two runs byte-identical,
  sha256 `7d46677c01a3586a35bdb8d60f733e200eab33fcb5fdc0c31921c3962c25feca`,
  188,909 bytes)
- **Prepared:** 2026-11-21 (build session, ~09:24–09:50 WIB)
- **Deadline:** 2026-11-23 07:00 WIB (2026-11-23T00:00:00Z)

## What the poster contains

- **56 stories, 7 regions** (8 stories per region: North America, Latin America,
  Europe, Middle East, Africa, Asia, Oceania), every story published or reported
  in the 21 Nov 2026 news cycle with its outlet tag on the page.
- **3 lead stories:** Houthi missiles fired at Riyadh, Saudi coalition intercepts
  three; Denmark expels a Russian diplomat over an alleged plot to kill a
  Ukrainian rapper; Mamdani unveils a plan to close Rikers Island jail by 2032.
- **Dot-matrix world map** with 7 numbered region pins + region key.
- **16 illustrated panels** (3 leads + 13 feature tiles) drawn from the day's stories.
- **UTC timeline** (6 timed events), **by-the-numbers** strip (6 stats),
  **weather strip** (day highs for 7 capitals, Open-Meteo forecast for 21 Nov) +
  **"left out & why"** date-check box.
- **SOURCES.md** in the repo lists every story with outlet, date and
  verification URL.

## Research note

The **Just Security Early Edition for 21 Nov 2026 was not yet published** at
build time (09:30 WIB / 02:30 UTC — the latest edition available was 20 Nov).
Stories were therefore verified against Reuters, AP, BBC, The Guardian,
Al Jazeera, ABC, Variety, The Hindu, Rio Times, AppiSToS and the aggregators
listed in SOURCES.md. Items published late on 20 Nov UTC and carried as
today's news in the 21 Nov editions are marked as such in SOURCES.md — the
same overnight-cycle standard the 20 Nov edition used.

## What remains

**NOT submitted.** The news-image kit refuses transcript bundles for subagent
sessions, so this entry was prepared only. To submit, the user pastes the
prompt into the **'make.fun — Ruang Build'** side chat before the deadline
**2026-11-23 07:00 WIB**; the build there regenerates/submits this repo@commit.

## Build notes

- Generator (`main.py`) written **fresh in this session** — no earlier
  news-image entry's code was read, copied or reused (only the 20261120
  SUBMISSION-REPORT.md was read, for format reference).
- `entry.png` visually inspected at full size and at 2× crops (region key,
  weather strip); two defects found and fixed (region-key "8 stories" labels
  clipped by the panel edge; weather credit overlapping Sydney's values).
- Repo is public and contains LICENSE (MIT, SPDX line), `.makefun/owner.json`,
  README (badges + About), SOURCES.md, `main.py`, `entry.png`; description,
  homepage (https://make.fun) and topics set on GitHub.
