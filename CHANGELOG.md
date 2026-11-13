# Changelog

Changes are listed newest first. Historical dates and milestones come from the
repository's Git history. No numbered releases have been assigned here.

## Unreleased

### Documentation — November 12, 2026

- Expanded the README with the verified project start date, September 6, 2019,
  and context for the seven-year path to the current working version.
- Added a current-status summary, feature overview, typical-day walkthrough,
  repository guide, and credits and license information.
- Clarified that CRT continuation prompts accept Space or Return, while decision
  input and replay answers require Return.
- Described title playback using its current tempo scale.
- Added this changelog and linked it from the README, moving the detailed
  historical milestones into one chronological record.

## 2026-11-12 — Working Python recreation

### Added

- CRT-style terminal presentation in `lemonade_crt.py`, with a centered monitor,
  green 40-column text, animated title drops, and weather scenes.
- Synthesized music and sound effects based on the bundled BASIC listing,
  including an opening melody followed by evenly timed drips.
- Audio lifecycle support in `lemonade_audio.py` to stop external players when
  the owning game closes or is forcibly stopped on macOS/Linux.
- Command-line options for plain text, muted playback, skipping the intro,
  displaying only the title, and repeatable Python random sequences.
- Regression tests for rules, event boundaries, accounting, input, resume/replay,
  terminal behavior, audio generation, and audio-player cleanup.
- Saved title-screen and opening-audio previews in `previews/`.

### Changed

- Reworked `lemonade_stand.py` around the bundled February 1979 Applesoft listing,
  preserving its demand formula, weather and storm checks, cost schedule,
  street-work behavior, bankruptcy rules, and replay state.
- Added Space continuation and Escape handling in CRT mode, plus automatic
  plain-text fallback for piped input/output and `TERM=dumb` terminals.
- Documented requirements, launch options, preserved quirks, fidelity limits,
  and the regression-test command.

### Preserved

- The previous main implementation as `lemonade_stand.py.bak`.
- Earlier conversion experiments and flowcharts for historical comparison.

## 2025-09-06 — Main implementation update

- Updated `lemonade_stand.py` with the version described in the commit as a
  “new version from Claude,” merged through pull request #2.

## 2023-02-02 to 2023-02-14 — Reference listing and experiments

- Added `lemonade_stand.basic`, the Applesoft listing used by the current port.
- Added `lemonade_chatGPT.py`, `lemon_chatGPT_full.py`, and
  `# LEMONADE STAND - PYTHON VERSION.py` as conversion experiments.
- Added the `Inkfree.ttf` font asset and `Lemonade Stand.drawio` flowchart.
- Updated the flowchart on February 14.

## 2022-04-04 to 2022-04-26 — Flowcharts and conversion work

- Added and expanded `Untitled Diagram.drawio`.
- Revised the original `lemonande_port.py` conversion.
- Added `lemonade_stand.py` and `lemonade_stand_basic.py` on April 5.
- Added the interactive `test_lemonade.py` prototype on April 26.

## 2019-09-06 — Project started

- Created lemonadePort to convert Lemonade from BASIC to Python.
- Added the initial README and GNU GPL v3 license.
- Uploaded `lemonade.basic` and the first Python conversion,
  `lemonande_port.py`.
- Removed page numbers left over from copied source text and merged the initial
  conversion work through pull request #1.
