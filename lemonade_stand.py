#!/usr/bin/env python3
"""Text-mode port of the bundled 1979 Applesoft Lemonade Stand listing.

Original program: Bob Jamison / MECC. Apple adaptation: Charlie Kellner.
BASIC line numbers below identify behavior that is easy to accidentally change.
Only the Python standard library is required. See README.md for fidelity limits.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import os
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import IntEnum
import math
import random
import re
from typing import Callable


class Weather(IntEnum):
    SUNNY = 2
    THUNDERSTORM = 5
    HOT = 7
    CLOUDY = 10


WEATHER_NAMES = {Weather.SUNNY: "SUNNY", Weather.HOT: "HOT AND DRY",
                 Weather.CLOUDY: "CLOUDY", Weather.THUNDERSTORM: "THUNDERSTORMS!"}
SIGN_COST = 0.15
STARTING_ASSETS = 2.0


@dataclass
class Player:
    assets: float = STARTING_ASSETS
    bankrupt: bool = False
    glasses_made: int = 0
    signs_made: int = 0
    price_per_glass: int = 0
    glasses_sold: int = 0
    income: float = 0.0
    expenses: float = 0.0
    profit: float = 0.0


def basic_val(text: str) -> float:
    """VAL reads a numeric prefix; unrecognized text yields zero."""
    match = re.match(r"^[\s]*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?)", text)
    if not match:
        return 0.0
    value = float(match.group(1))
    return value if math.isfinite(value) else 0.0


def money(amount: float) -> str:
    # BASIC 4010 uses INT(x * 100 + .5), not Python's ties-to-even round.
    cents = math.floor(amount * 100 + 0.5)
    return f"${'-' if cents < 0 else ''}{abs(cents) // 100}.{abs(cents) % 100:02d}"


class Game:
    """Game rules independent of input/display, with injectable random draws."""

    def __init__(self, players: int = 1, rng=None):
        if not 1 <= players <= 30:
            raise ValueError("There must be 1 to 30 stands")
        self._stands = [Player() for _ in range(30)]
        self.players = self._stands[:players]
        self.day = 0
        self.weather = Weather.SUNNY
        self.cost = 0.02
        self.multiplier = 1.0
        self.street_crews_buy_all = False
        self.storm = False
        self.rain_chance = 0
        self.rng = rng if rng is not None else random.Random()

    def start_day(self) -> list[str]:
        # 410-510: draw even on forced-sunny days, BEFORE incrementing D.
        draw = self.rng.random()
        self.weather = (Weather.SUNNY if draw < .6 else
                        Weather.CLOUDY if draw < .8 else Weather.HOT)
        if self.day < 3:
            self.weather = Weather.SUNNY
        self.day += 1
        self.cost = .02 if self.day <= 2 else .04 if self.day <= 6 else .05
        self.multiplier = 1.0
        self.street_crews_buy_all = False
        self.storm = False
        self.rain_chance = 0
        messages = []
        if self.day == 3:
            messages.append("(YOUR MOTHER QUIT GIVING YOU FREE SUGAR)")
        if self.day == 7:
            messages.append("(THE PRICE OF LEMONADE MIX JUST WENT UP)")
        if self.day <= 2:
            return messages
        # 2010/2030 branch directly past the unused X1/X2/X4 guards.
        if self.weather == Weather.CLOUDY:
            self.rain_chance = 30 + math.floor(self.rng.random() * 5) * 10
            self.multiplier = 1 - self.rain_chance / 100
            messages += [f"THERE IS A {self.rain_chance}% CHANCE OF LIGHT RAIN,",
                         "AND THE WEATHER IS COOLER TODAY."]
        elif self.weather == Weather.HOT:
            self.multiplier = 2.0
            messages.append("A HEAT WAVE IS PREDICTED FOR TODAY!")
        elif self.rng.random() < .25:
            messages += ["THE STREET DEPARTMENT IS WORKING TODAY.",
                         "THERE WILL BE NO TRAFFIC ON YOUR STREET."]
            # 2230 is RND(-1), NOT RND(1). Apple's reference manual gives
            # about 2.88e-8 for that fixed seed: always below .5. Thus the
            # buy-everything branch is unreachable in this exact listing.
            # Reseed the portable generator as well; subsequent numbers are
            # repeatable, though not the Apple ROM's bit-for-bit sequence.
            if hasattr(self.rng, "seed"):
                self.rng.seed(-1)
            self.multiplier = .1
        return messages

    def finish_weather(self) -> bool:
        # 1120: storm is drawn ONCE, after every stand has committed.
        # Applesoft AND eagerly evaluates both sides: even a sunny day
        # consumes this draw, unlike a short-circuit Python expression.
        draw = self.rng.random()
        self.storm = self.weather == Weather.CLOUDY and draw < .25
        if self.storm:
            self.weather = Weather.THUNDERSTORM
        return self.storm

    def settle(self, player: Player) -> None:
        # 1186-1300: even bankrupt stands are calculated using their old orders.
        player.assets = max(0.0, player.assets)
        if self.street_crews_buy_all:  # 1187 precedes the G(I)=0 storm factor.
            sold = player.glasses_made
        else:
            price = player.price_per_glass
            n1 = ((10 - price) / 10 * .8 * 30 + 30 if price < 10
                  else 10 ** 2 * 30 / price ** 2)
            v = 1 - math.exp(-player.signs_made * .5)
            n2 = self.multiplier * (n1 + n1 * v)
            sold = min(math.floor(n2 * (0 if self.storm else 1)), player.glasses_made)
        player.glasses_sold = sold
        player.income = sold * player.price_per_glass * .01
        player.expenses = player.signs_made * SIGN_COST + player.glasses_made * self.cost
        player.profit = player.income - player.expenses
        player.assets += player.profit
        # The CLI tests bankruptcy after displaying the report (1350).


class EndGame(Exception):
    """Space/escape continuation routine requested the replay prompt."""


class Terminal:
    def __init__(self, read: Callable[[str], str] = input, write: Callable[[str], None] = print,
                 screen=None, speaker=None):
        self.read = read
        self.write = write
        self.screen = screen
        self.speaker = speaker

    def page(self):
        if self.screen is not None:
            self.screen.clear()

    def play_sound(self, name):
        if self.speaker is not None:
            self.speaker.play(name)

    def wait_sound(self):
        if self.speaker is not None:
            self.speaker.wait()

    def opening(self):
        from lemonade_crt import TITLE
        self.play_sound('opening')
        if self.screen is not None:
            self.screen.opening()
        else:
            self.write('\n'.join(TITLE))
            self.write('COPYRIGHT 1979 APPLE COMPUTER INC.')
        self.wait_sound()

    def show_weather(self, weather):
        self.play_sound({Weather.SUNNY: 'sunny', Weather.HOT: 'hot',
                         Weather.CLOUDY: 'cloudy', Weather.THUNDERSTORM: 'storm'}[weather])
        if self.screen is not None:
            self.screen.weather(weather)
            self.write('LEMONSVILLE WEATHER REPORT')
            self.write(WEATHER_NAMES[weather])
            import time
            time.sleep(.7)
            self.wait_sound()
            self.page()

    def ask(self, prompt: str) -> str:
        return self.read(prompt)

    def pause(self):
        while True:
            if self.screen is not None:
                answer = self.screen.wait_key("PRESS SPACE TO CONTINUE, ESC TO END...")
            else:
                answer = self.ask("PRESS RETURN TO CONTINUE, TYPE ESC TO END... ")
            if answer == " " or answer == "":
                return
            if answer.startswith("\x1b") or answer.upper() == "ESC":
                raise EndGame

    def yes_no(self, prompt: str) -> bool:
        while True:
            answer = self.ask(prompt).upper()
            if answer.startswith(("Y", "N")):
                return answer.startswith("Y")

    def integer(self, prompt: str, low: int, high: int) -> int:
        while True:
            try:
                value = Decimal(self.ask(prompt).strip())
                if value.is_finite() and low <= value <= high and value == value.to_integral_value():
                    return int(value)
            except InvalidOperation:
                pass
            self.write("COME ON, LET'S BE REASONABLE NOW!!! TRY AGAIN")

    def instructions(self):
        self.page()
        self.write("""TO MANAGE YOUR LEMONADE STAND, YOU WILL
NEED TO MAKE THESE DECISIONS EVERY DAY:

1. HOW MANY GLASSES OF LEMONADE TO MAKE
   (ONLY ONE BATCH IS MADE EACH MORNING)
2. HOW MANY ADVERTISING SIGNS TO MAKE
   (THE SIGNS COST FIFTEEN CENTS EACH)
3. WHAT PRICE TO CHARGE FOR EACH GLASS

YOU WILL BEGIN WITH $2.00 CASH (ASSETS).
BECAUSE YOUR MOTHER GAVE YOU SOME SUGAR,
YOUR COST TO MAKE LEMONADE IS TWO CENTS
A GLASS (THIS MAY CHANGE IN THE FUTURE).""")
        self.pause()
        self.page()
        self.write("""YOUR EXPENSES ARE THE SUM OF THE COST OF
THE LEMONADE AND THE COST OF THE SIGNS.

YOUR PROFITS ARE THE DIFFERENCE BETWEEN
THE INCOME FROM SALES AND YOUR EXPENSES.

THE NUMBER OF GLASSES YOU SELL EACH DAY
DEPENDS ON THE PRICE YOU CHARGE, AND ON
THE NUMBER OF ADVERTISING SIGNS YOU USE.

KEEP TRACK OF YOUR ASSETS, BECAUSE YOU
CAN'T SPEND MORE MONEY THAN YOU HAVE!""")
        self.pause()

    def setup(self, rng, previous: Game | None = None) -> Game:
        self.page()
        self.write("""LEMONADE STAND
FROM AN ORIGINAL PROGRAM BY BOB JAMISON / MECC
MODIFIED FOR THE APPLE, FEBRUARY 1979, BY CHARLIE KELLNER

HI! WELCOME TO LEMONSVILLE, CALIFORNIA!

IN THIS SMALL TOWN, YOU ARE IN CHARGE OF
RUNNING YOUR OWN LEMONADE STAND. YOU CAN
COMPETE WITH AS MANY OTHER PEOPLE AS YOU
WISH, BUT HOW MUCH PROFIT YOU MAKE IS UP
TO YOU (THE OTHER STANDS' SALES WILL NOT
AFFECT YOUR BUSINESS IN ANY WAY). IF YOU
MAKE THE MOST MONEY, YOU'RE THE WINNER!!""")
        new = self.yes_no("ARE YOU STARTING A NEW GAME? (YES OR NO) ")
        # 12230 accepts VAL(N$); fractional N runs floor(N) loop iterations.
        while True:
            count = basic_val(self.ask("HOW MANY PEOPLE WILL BE PLAYING ==> "))
            if 1 <= count <= 30:
                break
        game = Game(math.floor(count), rng)
        # Replay jumps to 150, not RUN: D and the decision arrays survive.
        if previous is not None:
            game.day = previous.day
            for index, old in enumerate(previous._stands):
                fresh = game._stands[index]
                fresh.glasses_made = old.glasses_made
                fresh.signs_made = old.signs_made
                fresh.price_per_glass = old.price_per_glass
        if new:
            self.instructions()
        else:
            self.page()
            self.write("HI AGAIN! WELCOME BACK TO LEMONSVILLE!")
            attempts = 0
            prompt = "DO YOU REMEMBER WHAT DAY NUMBER IT WAS? "
            while True:
                answer = self.ask(prompt).upper()
                value = basic_val(answer)
                if value != 0:
                    if 1 <= value <= 99 and value == math.floor(value):
                        game.day = int(value)
                    break
                if answer.startswith("Y"):
                    attempts += 1
                    prompt = "GOOD! WHAT DAY WAS IT? "
                elif answer.startswith("N") or attempts > 0:
                    break
                else:
                    attempts += 1
                    prompt = "YES OR NO? "
            self.write(f"OKAY - WE'LL START WITH DAY NO. {game.day + 1}")
            for i, player in enumerate(game.players, 1):
                value = basic_val(self.ask(f"PLAYER NO. {i}, HOW MUCH MONEY (ASSETS) DID YOU HAVE? "))
                if value < 2:
                    self.write("O.K. - WE'LL START YOU OUT WITH $2.00")
                    value = 2
                elif value > 40:
                    self.write("JUST TO BE FAIR, LET'S MAKE THAT $10.00")
                    value = 10
                player.assets = math.floor(value * 100 + .5) / 100
            if self.ask("...READY TO BEGIN? ").upper().startswith("N"):
                self.instructions()
        return game

    def decisions(self, game: Game):
        i = 0
        while i < len(game.players):
            p = game.players[i]
            self.page()
            self.write(f"DAY {game.day}  {WEATHER_NAMES[game.weather]}  COST {money(game.cost)}")
            if game.rain_chance:
                self.write(f"{game.rain_chance}% CHANCE OF RAIN / COOLER TODAY")
            elif game.multiplier == .1:
                self.write("STREET WORK: NO TRAFFIC TODAY")
            elif game.multiplier == 2:
                self.write("A HEAT WAVE IS PREDICTED FOR TODAY!")
            p.assets += .000000001  # 815: preserve the affordability allowance.
            self.write(f"\nLEMONADE STAND {i + 1}             ASSETS {money(p.assets)}")
            if p.bankrupt:
                self.write("YOU ARE BANKRUPT, NO DECISIONS\nFOR YOU TO MAKE.")
                if len(game.players) == 1 and p.assets < game.cost * 100:
                    raise EndGame
            else:
                while True:
                    glasses = self.integer("HOW MANY GLASSES OF LEMONADE DO YOU WISH TO MAKE? ", 0, 1000)
                    if glasses * game.cost <= p.assets:
                        p.glasses_made = glasses
                        break
                    self.write(f"THINK AGAIN!!! YOU HAVE ONLY {money(p.assets)}\n"
                               f"IN CASH AND TO MAKE {glasses} GLASSES OF\n"
                               f"LEMONADE YOU NEED {money(glasses * game.cost)} IN CASH.")
                while True:
                    signs = self.integer("HOW MANY ADVERTISING SIGNS (15 CENTS EACH) DO YOU WANT TO MAKE? ", 0, 50)
                    if signs * SIGN_COST <= p.assets - p.glasses_made * game.cost:
                        p.signs_made = signs
                        break
                    self.write(f"THINK AGAIN, YOU HAVE ONLY {money(p.assets - p.glasses_made * game.cost)}\n"
                               "IN CASH LEFT AFTER MAKING YOUR LEMONADE.")
                p.price_per_glass = self.integer("WHAT PRICE (IN CENTS) DO YOU WISH TO CHARGE FOR LEMONADE? ", 0, 100)
            # 1060 GOTO 810 resets the entire FOR loop, not just this player.
            if self.ask("WOULD YOU LIKE TO CHANGE ANYTHING? ").upper().startswith("Y"):
                i = 0
            else:
                i += 1

    def play_day(self, game: Game):
        messages = game.start_day()
        self.show_weather(game.weather)
        self.page()
        self.write(f"\nLEMONSVILLE WEATHER REPORT\n{WEATHER_NAMES[game.weather]}")
        self.write(f"ON DAY {game.day}, THE COST OF LEMONADE IS {money(game.cost)}")
        for message in messages:
            self.write(message)
        if self.screen is not None:
            import time
            time.sleep(1.2)
        self.decisions(game)
        if game.finish_weather():
            self.show_weather(game.weather)
            self.page()
            self.write("""\nTHUNDERSTORMS!
WEATHER REPORT: A SEVERE THUNDERSTORM
HIT LEMONSVILLE EARLIER TODAY, JUST AS
THE LEMONADE STANDS WERE BEING SET UP.
UNFORTUNATELY, EVERYTHING WAS RUINED!!""")
        else:
            self.page()
            self.play_sound('report')
            self.write("\n$$ LEMONSVILLE DAILY FINANCIAL REPORT $$")
        if game.street_crews_buy_all:
            self.write("THE STREET CREWS BOUGHT ALL YOUR\nLEMONADE AT LUNCHTIME!!")
        for i, p in enumerate(game.players, 1):
            if i > 1:
                self.page()
                self.write("$$ LEMONSVILLE DAILY FINANCIAL REPORT $$")
            was_bankrupt = p.bankrupt
            game.settle(p)
            if was_bankrupt:
                self.write(f"STAND {i}   BANKRUPT")
                self.pause()
                continue
            self.write(f"""\n   DAY {game.day}                  STAND {i}

  {p.glasses_sold} GLASSES SOLD
  {money(p.price_per_glass / 100)} PER GLASS        INCOME {money(p.income)}

  {p.glasses_made} GLASSES MADE
  {p.signs_made} SIGNS MADE            EXPENSES {money(p.expenses)}

                       PROFIT {money(p.profit)}
                       ASSETS {money(p.assets)}""")
            self.pause()
            if p.assets <= game.cost:
                p.bankrupt = True
                self.write(f"STAND {i}\n...YOU DON'T HAVE ENOUGH MONEY LEFT\n"
                           "TO STAY IN BUSINESS YOU'RE BANKRUPT!")
                self.pause()
                if len(game.players) == 1:
                    raise EndGame

    def run(self, seed: int | None = None, skip_intro: bool = False):
        rng = random.Random(seed)
        game = None
        try:
            if not skip_intro:
                self.opening()
            while True:
                try:
                    game = self.setup(rng, game)
                    while True:
                        self.play_day(game)
                except EndGame:
                    self.page()
                    if not self.ask("WOULD YOU LIKE TO PLAY AGAIN ").upper().startswith("Y"):
                        return
        except (EOFError, KeyboardInterrupt):
            self.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, help="Repeatable Python random sequence (not Apple ROM emulation)")
    parser.add_argument("--plain", action="store_true", help="Scrolling text instead of the centered CRT screen")
    parser.add_argument("--mute", action="store_true", help="Disable music and speaker effects")
    parser.add_argument("--title-only", action="store_true", help="Show the animated title and dripping sound, then wait")
    parser.add_argument("--skip-intro", action="store_true", help="Skip the opening title animation")
    args = parser.parse_args()
    from lemonade_crt import CRT, Speaker
    interactive = sys.stdin.isatty() and sys.stdout.isatty()
    use_crt = interactive and not args.plain and os.environ.get('TERM') != 'dumb'
    with ExitStack() as stack:
        speaker = stack.enter_context(Speaker(enabled=interactive and not args.mute))
        if use_crt:
            screen = stack.enter_context(CRT())
            terminal = Terminal(screen.ask, screen.write, screen, speaker)
        else:
            terminal = Terminal(speaker=speaker)
        if args.title_only:
            try:
                terminal.opening()
                terminal.ask("PRESS RETURN TO EXIT THE TITLE SCREEN... ")
            except (EOFError, KeyboardInterrupt):
                pass
        else:
            terminal.run(args.seed, skip_intro=args.skip_intro)


if __name__ == "__main__":
    main()
