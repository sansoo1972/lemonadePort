"""Regression checks against the numbered rules in lemonade_stand.basic."""
import math
import unittest
from lemonade_stand import Game, Player, Terminal, Weather, EndGame, basic_val, money


class Draws:
    def __init__(self, *values):
        self.values = iter(values)
        self.used = 0

    def random(self):
        self.used += 1
        return next(self.values)


def terminal(*answers):
    answers = iter(answers)
    output = []
    return Terminal(lambda _: next(answers), output.append), output


class ReplicaTests(unittest.TestCase):
    def test_first_three_forecasts_are_sunny(self):
        rng = Draws(.99, .99, .99, .99, .99)
        game = Game(rng=rng)
        for day in range(1, 4):
            game.start_day()
            self.assertEqual((game.day, game.weather), (day, Weather.SUNNY))
        self.assertEqual(rng.used, 4)  # Day 3 also checks street work.
        game.start_day()
        self.assertEqual(game.weather, Weather.HOT)

    def test_cost_schedule(self):
        game = Game(rng=Draws(*([.5] * 30)))
        costs = []
        for _ in range(8):
            game.start_day()
            costs.append(game.cost)
        self.assertEqual(costs, [.02, .02, .04, .04, .04, .04, .05, .05])

    def test_weather_thresholds(self):
        for draw, expected in [(.5999, Weather.SUNNY), (.6, Weather.CLOUDY),
                               (.7999, Weather.CLOUDY), (.8, Weather.HOT)]:
            game = Game(rng=Draws(draw, .99))
            game.day = 3
            game.start_day()
            self.assertEqual(game.weather, expected)

    def test_cloudy_forecasts_always_reduce_demand(self):
        for draw, chance in [(0, 30), (.2, 40), (.4, 50), (.6, 60), (.999, 70)]:
            game = Game(rng=Draws(.7, draw))
            game.day = 3
            game.start_day()
            self.assertEqual(game.rain_chance, chance)
            self.assertAlmostEqual(game.multiplier, 1 - chance / 100)

    def test_street_work_negative_seed_always_reduces_traffic(self):
        game = Game(rng=Draws(.1, .249))
        game.day = 2
        game.start_day()
        self.assertFalse(game.street_crews_buy_all)
        self.assertEqual(game.multiplier, .1)
        self.assertEqual(game.rng.used, 2)
        game = Game(rng=Draws(.1, .25))
        game.day = 2
        self.assertEqual(game.start_day(), ["(YOUR MOTHER QUIT GIVING YOU FREE SUGAR)"])

    def test_street_work_reseeds_following_random_sequence(self):
        import random
        game = Game(rng=random.Random(123))
        game.day = 2  # This seed selects sunshine and street work.
        game.start_day()
        self.assertEqual(game.multiplier, .1)
        self.assertEqual(game.rng.random(), random.Random(-1).random())

    def test_heat_wave_doubles_demand(self):
        game = Game(rng=Draws(.9))
        game.day = 3
        game.start_day()
        p = Player(glasses_made=100, price_per_glass=10)
        game.settle(p)
        self.assertEqual(p.glasses_sold, 60)

    def test_storm_shared_by_all_stands_and_expenses_remain(self):
        game = Game(2, Draws(.7, .4, .2499))
        game.day = 3
        game.start_day()
        self.assertTrue(game.finish_weather())
        for p in game.players:
            p.glasses_made, p.signs_made, p.price_per_glass = 20, 1, 10
            game.settle(p)
            self.assertEqual(p.glasses_sold, 0)
            self.assertAlmostEqual(p.profit, -.95)

    def test_storm_threshold_and_eager_draw_on_clear_days(self):
        game = Game(rng=Draws(.25, .1))
        game.weather = Weather.CLOUDY
        self.assertFalse(game.finish_weather())
        game.weather = Weather.SUNNY
        self.assertFalse(game.finish_weather())
        self.assertEqual(game.rng.used, 2)

    def test_street_crews_override_supply_demand_and_storm_factor(self):
        game = Game()
        game.street_crews_buy_all = True
        game.storm = True  # BASIC 1187 jumps over the G(I) calculation.
        p = Player(glasses_made=100, price_per_glass=100)
        game.settle(p)
        self.assertEqual(p.glasses_sold, 100)

    def test_sales_against_basic_expression(self):
        game = Game()
        for price in range(101):
            for signs in range(51):
                for multiplier in [.3, .4, .5, .6, .7, 1, 2]:
                    game.multiplier = multiplier
                    p = Player(glasses_made=1000, signs_made=signs, price_per_glass=price)
                    game.settle(p)
                    n1 = ((10 - price) / 10 * .8 * 30 + 30 if price < 10
                          else 100 * 30 / price ** 2)
                    expected = math.floor(multiplier * (n1 + n1 * (1 - math.exp(-signs * .5))))
                    self.assertEqual(p.glasses_sold, min(1000, expected))

    def test_day_one_known_report(self):
        game = Game()
        p = Player(glasses_made=50, signs_made=2, price_per_glass=10)
        game.settle(p)
        self.assertEqual(p.glasses_sold, 48)
        self.assertAlmostEqual(p.income, 4.8)
        self.assertAlmostEqual(p.expenses, 1.3)
        self.assertAlmostEqual(p.profit, 3.5)
        self.assertAlmostEqual(p.assets, 5.5)

    def test_bankrupt_stands_keep_old_orders_and_are_still_settled(self):
        game = Game()
        p = Player(assets=-1, bankrupt=True, glasses_made=10, price_per_glass=10)
        game.settle(p)
        self.assertAlmostEqual(p.assets, .8)
        self.assertTrue(p.bankrupt)

    def test_input_rejects_fractions_nonfinite_and_out_of_range(self):
        ui, output = terminal('3.9', 'NaN', 'Infinity', '-1', '1001', 'word', '4.0')
        self.assertEqual(ui.integer('?', 0, 1000), 4)
        self.assertEqual(len(output), 6)

    def test_zero_price_and_zero_supply(self):
        for glasses, price, expected in [(100, 0, 54), (0, 100, 0)]:
            p = Player(glasses_made=glasses, price_per_glass=price)
            Game().settle(p)
            self.assertEqual(p.glasses_sold, expected)

    def test_affordability_epsilon(self):
        game = Game()
        game.cost = .05
        game.players[0].assets = .3
        ui, _ = terminal('6', '0', '10', 'N')
        ui.decisions(game)
        self.assertEqual(game.players[0].glasses_made, 6)

    def test_unaffordable_signs_retry_only_signs(self):
        game = Game()
        ui, output = terminal('100', '1', '0', '10', 'N')
        ui.decisions(game)
        self.assertEqual(game.players[0].glasses_made, 100)
        self.assertEqual(game.players[0].signs_made, 0)
        self.assertTrue(any('CASH LEFT' in line for line in output))

    def test_change_decisions_restarts_from_stand_one(self):
        game = Game(2)
        ui, _ = terminal('10', '0', '10', 'N', '20', '0', '10', 'Y',
                         '30', '0', '11', 'N', '40', '0', '12', 'N')
        ui.decisions(game)
        self.assertEqual([p.glasses_made for p in game.players], [30, 40])

    def test_single_player_bankruptcy_exits_after_report(self):
        game = Game(rng=Draws(.5, .5))
        ui, output = terminal('100', '0', '0', 'N', '', '')
        with self.assertRaises(EndGame):
            ui.play_day(game)
        self.assertTrue(game.players[0].bankrupt)
        self.assertTrue(any('100 GLASSES MADE' in line for line in output))

    def test_exact_cost_threshold_preserves_basic_epsilon(self):
        game = Game(rng=Draws(.5, .5))
        ui, _ = terminal('99', '0', '0', 'N', '')
        ui.play_day(game)
        # BASIC adds 1e-9, so 2 - 99*.02 remains just ABOVE .02.
        self.assertFalse(game.players[0].bankrupt)

    def test_continue_rounds_and_clamps_assets(self):
        ui, _ = terminal('N', '3', '6', '1', '41', '2.345', 'Y')
        game = ui.setup(Draws())
        self.assertEqual(game.day, 6)
        self.assertEqual([p.assets for p in game.players], [2, 10, 2.35])

    def test_continue_unknown_day_defaults_to_zero(self):
        ui, _ = terminal('N', '1', 'N', '2', 'Y')
        self.assertEqual(ui.setup(Draws()).day, 0)

    def test_replay_preserves_day_like_goto_150(self):
        previous = Game()
        previous.day = 8
        ui, _ = terminal('Y', '1', '', '')
        self.assertEqual(ui.setup(Draws(), previous).day, 8)

    def test_pause_escape_and_full_run(self):
        ui, _ = terminal('ESC')
        with self.assertRaises(EndGame):
            ui.pause()
        ui, output = terminal('Y', '1', 'ESC', 'N')
        ui.run(seed=1)
        self.assertTrue(output)

    def test_numeric_prefix_and_display_rounding(self):
        self.assertEqual(basic_val('  12.5 dollars'), 12.5)
        self.assertEqual(basic_val('NO'), 0)
        self.assertEqual(money(.125), '$0.13')
        self.assertEqual(money(-.125), '$-0.12')


if __name__ == '__main__':
    unittest.main()
