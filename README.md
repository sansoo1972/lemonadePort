# Lemonade Stand — lemonadePort

A Python text-mode port of `lemonade_stand.basic`, the bundled February 1979
Apple adaptation by Charlie Kellner of Bob Jamison's MECC game.

This project began on **September 6, 2019**, with the goal of converting
Lemonade to Python. On **November 12, 2026**, just over seven years later,
the working terminal recreation was committed with its display, sound, and
regression tests. The repository keeps the early conversion attempts alongside
the current implementation so the project's development remains visible.

## Current status — November 12, 2026

The current entry point is `lemonade_stand.py`. The latest implementation brings
together the BASIC-based game rules, CRT-style terminal display, title and weather
audio, keyboard controls, and audio cleanup. Earlier ports remain available for
historical comparison.

The latest documentation update records the September 6, 2019 start date,
explains the current features and gameplay, maps the repository files, and
clarifies Space/Return controls. See [CHANGELOG.md](CHANGELOG.md) for the detailed
history from the first conversion through the current working version and these
documentation changes.

### What the current version delivers

- A playable Python game for 1–30 stands, with daily production, advertising,
  pricing, weather, expenses, sales, and financial reports.
- Rules checked against the bundled 1979 Applesoft listing, including its
  unusual random-event, bankruptcy, and replay behavior.
- A centered green-screen terminal display, animated title, weather scenes,
  and synthesized music and sound effects based on the BASIC data.
- Plain-text and muted modes, repeatable Python random sequences, and the
  original manual resume process using a day number and player assets.
- Automated checks for game rules, terminal behavior, audio generation, and
  audio-process cleanup, using only Python's standard library.

## A typical day

Read the weather report and production cost, then choose how many glasses to
make, how many advertising signs to buy, and the price per glass in cents for
each stand. Keep production and advertising within your available cash. After
you confirm the decisions, the game applies demand and events and shows each
stand's sales, expenses, profit, and remaining assets. Continue to the next day
or end the session at the continuation prompt.

## Play

Requires Python 3.10 or newer; no additional packages.

```sh
python3 lemonade_stand.py
```

The game opens in a centered 4:3 monitor with a subtle, near-black bezel and
green 40-column text. The full LEMONADE STAND title stays visible as animated
drops fall beneath it, accompanied by slower music followed by evenly timed water drips
(played at a 55% tempo scale while preserving pitch). The lettering and tune data come from the
BASIC listing. Weather scenes, weather tunes, and financial-report sounds are
included. The screen recenters when you resize the terminal; 80 × 30 or larger
provides comfortable margins around the original 40 × 24 display. The outer
monitor grows up to 96 columns × 36 rows. Its 4:3 proportion assumes terminal
cells are twice as tall as wide; your terminal font may change the appearance.

Enter decisions and press Return. At continuation prompts, tap Space once to
continue immediately; Return also works. These prompts do not echo or edit
text. Tap the Escape key to open the replay prompt. Ctrl-C or end-of-input exits. You can resume a previous game by
entering its day number and each player's assets, as in the BASIC listing.

Sound uses macOS `afplay`, Windows' built-in WAV playback, or `aplay`/`paplay`
on Linux when available. If no supported player is installed, gameplay remains
silent. No packages are installed. On macOS/Linux, each audio player is owned
by a short-lived helper connected to the game's process. Closing or forcibly
stopping the game closes that connection and stops playback; the helper also
limits each cue's lifetime. No background audio service is installed.

The `previews/title-sound.wav` file, if opened manually in another application,
is controlled by that application's player rather than by the game. Helpful options:

```sh
python3 lemonade_stand.py --title-only  # Show the title and dripping sound
python3 lemonade_stand.py --mute        # CRT display without sound
python3 lemonade_stand.py --skip-intro  # Jump directly to the welcome page
python3 lemonade_stand.py --plain       # Scrolling text, no full-screen display
```

Piped input/output and terminals declaring `TERM=dumb` use plain text
automatically. In plain mode the prompt asks for Return; typing `ESC` then Return ends the game.

For a repeatable Python random sequence:

```sh
python3 lemonade_stand.py --seed 42
```

## Preserved rules and quirks

- 1–30 independent stands; $2 starting assets; 15-cent advertising signs.
- Two-cent production on days 1–2, four cents on days 3–6, five cents thereafter.
- The original demand and exponential advertising expressions, integer sales,
  production limits, and income/expense accounting.
- Weather is drawn before incrementing the day: the first **three** forecasts
  are sunny, although street work can begin on day 3.
- Later forecasts use the original 60/20/20 sunny/cloudy/hot thresholds.
- Every cloudy forecast reduces demand by a randomly selected 30–70%.
  A separate 25% storm check happens after all decisions; the storm affects
  every stand, and production and advertising expenses are still charged.
  The check consumes a draw even on sunny days, matching Applesoft’s eager AND.
- Heat doubles demand. Sunny days after day 2 have a 25% street-work check.
- BASIC line 2230 says `RND(-1)`. This is a fixed seed, not an ordinary draw;
  its result is below .5, so street work always reduces demand to 10%.
  The listing's “crews bought all your lemonade” branch is therefore unreachable.
  The Python generator is reseeded there too.
- Changing any decision restarts input from stand 1 (line 1060).
- The tiny cash allowance at line 815 is retained. Fractional decisions are
  rejected; budget failures repeat the relevant question.
- Bankruptcy uses the source's `assets <= production cost` condition after
  the financial report. Bankrupt stands in multiplayer retain their old
  orders and are still financially calculated, just as lines 1185–1327 do.
- There is no added 12-day ending, winner leaderboard, or automatic ending
  when every multiplayer stand is bankrupt. Use the continuation prompt to end.
- Replay preserves the day counter because the source jumps to line 150
  rather than restarting the BASIC program. A fresh process starts at day 0.

## Fidelity boundaries

This is a **terminal recreation, not a complete Apple II emulator**.
The source's title rows are translated into ASCII, its note data into square-wave
WAV audio, and its low-resolution weather coordinates into monochrome terminal
art. Animated drops replace the Apple-specific opening screen-memory animation. Music and drip effects play in sequence, and cues finish before the next cue starts.
Audio pitch/timing approximate the 6502 delay routine; the Apple font,
full-color graphics, thunder flashes, and analog speaker are not emulated exactly.
The centered screen preserves a 40-column layout, adapting to smaller terminals.
Decision input and replay answers require Return; continuation prompts also
accept Space in CRT mode. Lowercase yes/no answers are accepted.
ROM exit calls are replaced by normal Python cleanup, restoring the terminal.

Python uses a different PRNG and floating-point format from Applesoft. Event
thresholds and draw order are preserved, including the fixed street-work branch,
but seeded sequences and rare numerical boundary results are not guaranteed to
match an Apple II. Python's `math.exp` replaces Applesoft's EXP implementation.
All 30 stands’ decision slots survive replay, including when the player count
changes. The original 1973 Jamison source is not the comparison target; this
repository's listing is.

Apple documents negative-seed behavior in its
[Applesoft Programmer's Reference Manual, Volume 1](https://mirrors.apple2.org.za/ftp.apple.asimov.net/documentation/programming/basic/49163042-Apple-II-Applesoft-BASIC-Programmer-s-Reference-Manual-Volume-1.pdf).

## Verify

```sh
python3 -m unittest discover -s tests -v
```

The regression suite covers event boundaries, random-call timing, all-player
storms, cost changes, input retries, affordability, bankruptcy, resume/replay,
and 36,057 price/advertising/multiplier combinations against the BASIC formula.
The former `test_lemonade.py` remains an older interactive prototype and is not
part of this suite. Other legacy conversion experiments are left untouched.

The previous main implementation is preserved byte-for-byte as
`lemonade_stand.py.bak` (SHA-256
`8a181edeabae57bc28e2178e7dd7e4ac20abe4d59173285e21e3e8af038bcfd9`).

A static title preview is saved in `previews/title-screen.png`; the slowed
opening melody and water drops can be played from `previews/title-sound.wav`.

## Repository guide

| File or directory | Purpose |
| --- | --- |
| `lemonade_stand.py` | Current game entry point, rules, accounting, input, and command-line options. |
| `lemonade_crt.py` | Terminal layout, title animation, weather art, and sound synthesis/playback control. |
| `lemonade_audio.py` | Helper that manages audio-player lifetime on macOS/Linux. |
| `lemonade_stand.basic` | Bundled 1979 Applesoft listing used as the current fidelity reference. |
| `tests/` | Automated rule, display, and audio regression tests. |
| `previews/` | Saved title-screen image and opening audio preview. |
| `lemonade_stand.py.bak` | Previous main implementation, preserved before the working recreation. |
| `lemonade.basic` | Earlier imported BASIC-family source, retained from the 2019 work; distinct from the Applesoft reference above. |
| `lemonande_port.py`, `lemonade_stand_basic.py` | Earlier conversion work retained for project history. |
| `lemonade_chatGPT.py`, `lemon_chatGPT_full.py`, `# LEMONADE STAND - PYTHON VERSION.py` | Historical conversion experiments. |
| `test_lemonade.py` | Older interactive prototype; use `tests/` for automated verification. |
| `Lemonade Stand.drawio`, `Untitled Diagram.drawio` | Development flowcharts editable with diagrams.net/draw.io. |
| `Inkfree.ttf` | Font asset retained from earlier development. |
| `README.md` | Current setup, gameplay, architecture, and fidelity notes. |
| `CHANGELOG.md` | Dated implementation milestones and documentation changes. |
| `LICENSE` | GNU General Public License, version 3. |

For new changes, start with `lemonade_stand.py` and its supporting modules.
Keep the bundled reference listing and historical experiments available for
comparison. When changing a rule, identify the relevant BASIC line and run the
regression suite described above.

## Credits and license

Original game: **Bob Jamison / Minnesota Educational Computing Consortium
(MECC)**. Apple adaptation: **Charlie Kellner, February 1979**, as credited in
the bundled listing. This Python port and its development history are maintained
in **lemonadePort** by **Richard Perez**.

The repository includes the [GNU GPL v3 license](LICENSE). Original-program
credits are retained in the source and documentation.
