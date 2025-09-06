#!/usr/bin/env python3
"""
Lemonade Stand Game - Python Implementation
Based on the original BASIC version by Bob Jamison
"""

import random
import time
import os
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Weather(Enum):
    SUNNY = 2
    HOT = 7  
    CLOUDY = 10
    THUNDERSTORM = 5


class RandomEvent(Enum):
    NONE = 0
    LIGHT_RAIN = 1
    STREET_WORK = 2
    HEAT_WAVE = 3


@dataclass
class GameConstants:
    """Game constants matching the original BASIC version"""
    OPTIMAL_PRICE = 10  # P9 = 10 cents
    SIGN_COST = 0.15    # S3 = .15
    BASE_CUSTOMERS = 30  # S2 = 30
    STARTING_ASSETS = 2.00  # A2 = 2.00
    SIGN_EFFECTIVENESS = 0.5  # C9 = .5
    ADVERTISING_MULTIPLIER = 1  # C2 = 1


@dataclass
class Player:
    """Represents a player in the game"""
    id: int
    assets: float
    bankrupt: bool = False
    glasses_made: int = 0
    signs_made: int = 0
    price_per_glass: int = 0
    glasses_sold: int = 0
    income: float = 0.0
    expenses: float = 0.0
    profit: float = 0.0


class GameState:
    """Manages the overall game state"""
    def __init__(self):
        self.day = 0
        self.players: List[Player] = []
        self.weather = Weather.SUNNY
        self.weather_multiplier = 1.0
        self.random_event = RandomEvent.NONE
        self.lemonade_cost = 0.02
        self.constants = GameConstants()
        
    def get_lemonade_cost(self) -> float:
        """Calculate lemonade cost based on day"""
        if self.day <= 2:
            return 0.02
        elif self.day <= 6:
            return 0.04
        else:
            return 0.05


class WeatherSystem:
    """Handles weather generation and effects"""
    
    @staticmethod
    def generate_weather() -> Weather:
        """Generate random weather based on original probabilities"""
        rand = random.random()
        if rand < 0.6:
            return Weather.SUNNY
        elif rand < 0.8:
            return Weather.CLOUDY  
        else:
            return Weather.HOT
    
    @staticmethod
    def get_weather_multiplier(weather: Weather, day: int) -> float:
        """Get weather effect on sales"""
        if day < 3:
            return 1.0  # No weather effects first 2 days
            
        if weather == Weather.HOT:
            return 2.0
        elif weather == Weather.THUNDERSTORM:
            return 0.0  # Everything ruined
        else:
            return 1.0
    
    @staticmethod
    def display_weather(weather: Weather):
        """Display weather report"""
        print("\n" + "="*40)
        print("   LEMONSVILLE WEATHER REPORT")
        print("="*40)
        
        weather_messages = {
            Weather.SUNNY: "☀️  SUNNY",
            Weather.HOT: "🌡️  HOT AND DRY", 
            Weather.CLOUDY: "☁️  CLOUDY",
            Weather.THUNDERSTORM: "⛈️  THUNDERSTORMS!"
        }
        
        message = weather_messages.get(weather, "UNKNOWN")
        print(f"        {message}")
        print("="*40)


class RandomEventSystem:
    """Handles random events that can occur"""
    
    @staticmethod
    def check_random_event(day: int, weather: Weather) -> tuple[RandomEvent, float]:
        """Check for random events and return event and multiplier"""
        if day <= 2:
            return RandomEvent.NONE, 1.0
            
        if weather == Weather.CLOUDY and random.random() < 0.25:
            return RandomEvent.LIGHT_RAIN, 0.7  # Reduced sales
            
        if weather == Weather.HOT:
            print("A HEAT WAVE IS PREDICTED FOR TODAY!")
            return RandomEvent.HEAT_WAVE, 2.0
            
        if random.random() < 0.25:
            event_type = random.choice([RandomEvent.LIGHT_RAIN, RandomEvent.STREET_WORK])
            
            if event_type == RandomEvent.LIGHT_RAIN:
                chance = 30 + random.randint(0, 4) * 10
                print(f"THERE IS A {chance}% CHANCE OF LIGHT RAIN,")
                print("AND THE WEATHER IS COOLER TODAY.")
                return event_type, 1 - chance/100
                
            elif event_type == RandomEvent.STREET_WORK:
                print("THE STREET DEPARTMENT IS WORKING TODAY.")
                print("THERE WILL BE NO TRAFFIC ON YOUR STREET.")
                if random.random() < 0.5:
                    print("THE STREET CREWS BOUGHT ALL YOUR LEMONADE AT LUNCHTIME!!")
                    return event_type, -1  # Special handling - sell all
                else:
                    return event_type, 0.1  # Very few customers
                    
        return RandomEvent.NONE, 1.0


class SalesCalculator:
    """Calculates sales based on price, advertising, and conditions"""
    
    @staticmethod
    def calculate_demand(price: int, constants: GameConstants) -> float:
        """Calculate base demand based on price vs optimal price"""
        optimal = constants.OPTIMAL_PRICE
        base = constants.BASE_CUSTOMERS
        
        if price >= optimal:
            # Demand drops quadratically for high prices
            demand = (optimal ** 2) * base / (price ** 2)
        else:
            # Linear increase for prices below optimal
            demand = (optimal - price) / optimal * 0.8 * base + base
            
        return demand
    
    @staticmethod
    def apply_advertising_effect(base_demand: float, signs: int, constants: GameConstants) -> float:
        """Apply advertising effect using exponential formula"""
        w = -signs * constants.SIGN_EFFECTIVENESS
        v = 1 - (2.71828 ** w) * constants.ADVERTISING_MULTIPLIER  # Using e ≈ 2.71828
        return base_demand + (base_demand * v)
    
    @staticmethod
    def calculate_sales(player: Player, weather_multiplier: float, 
                       random_event: RandomEvent, constants: GameConstants) -> int:
        """Calculate final number of glasses sold"""
        if weather_multiplier == 0.0:  # Thunderstorm
            return 0
            
        # Calculate base demand
        base_demand = SalesCalculator.calculate_demand(player.price_per_glass, constants)
        
        # Apply advertising
        demand_with_ads = SalesCalculator.apply_advertising_effect(
            base_demand, player.signs_made, constants)
        
        # Apply weather and random event multipliers
        final_demand = demand_with_ads * weather_multiplier
        
        # Handle special case: street crews buy all
        if random_event == RandomEvent.STREET_WORK and weather_multiplier == -1:
            return player.glasses_made
        
        # Limit to supply
        glasses_sold = min(int(final_demand), player.glasses_made)
        return max(0, glasses_sold)


class InputValidator:
    """Validates user input"""
    
    @staticmethod
    def get_int_input(prompt: str, min_val: int, max_val: int) -> int:
        """Get validated integer input within range"""
        while True:
            try:
                value = input(prompt)
                if value.lower() in ['quit', 'exit']:
                    raise KeyboardInterrupt
                    
                num = int(float(value))  # Handle decimal input
                if min_val <= num <= max_val:
                    return num
                else:
                    print(f"COME ON, LET'S BE REASONABLE NOW!!! (Enter {min_val}-{max_val})")
            except (ValueError, KeyboardInterrupt):
                if value.lower() in ['quit', 'exit']:
                    raise KeyboardInterrupt
                print("PLEASE ENTER A VALID NUMBER!")
    
    @staticmethod
    def get_yes_no(prompt: str) -> bool:
        """Get yes/no input"""
        while True:
            response = input(prompt).upper().strip()
            if response.startswith('Y'):
                return True
            elif response.startswith('N'):
                return False
            else:
                print("PLEASE ANSWER YES OR NO!")


class Display:
    """Handles game display and formatting"""
    
    @staticmethod
    def clear_screen():
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount as currency"""
        return f"${amount:.2f}"
    
    @staticmethod
    def show_title():
        """Show game title"""
        Display.clear_screen()
        print("*" * 50)
        print("*" + " " * 48 + "*")
        print("*" + "    🍋 LEMONADE STAND 🍋".center(48) + "*")
        print("*" + " " * 48 + "*") 
        print("*" * 50)
        print()
    
    @staticmethod
    def show_instructions():
        """Show game instructions"""
        Display.clear_screen()
        print("TO MANAGE YOUR LEMONADE STAND, YOU WILL")
        print("NEED TO MAKE THESE DECISIONS EVERY DAY:")
        print()
        print("1. HOW MANY GLASSES OF LEMONADE TO MAKE")
        print("   (ONLY ONE BATCH IS MADE EACH MORNING)")
        print("2. HOW MANY ADVERTISING SIGNS TO MAKE")
        print("   (THE SIGNS COST FIFTEEN CENTS EACH)")
        print("3. WHAT PRICE TO CHARGE FOR EACH GLASS")
        print()
        print("YOU WILL BEGIN WITH $2.00 CASH (ASSETS).")
        print("BECAUSE YOUR MOTHER GAVE YOU SOME SUGAR,")
        print("YOUR COST TO MAKE LEMONADE IS TWO CENTS")
        print("A GLASS (THIS MAY CHANGE IN THE FUTURE).")
        print()
        input("PRESS ENTER TO CONTINUE...")
        
        Display.clear_screen()
        print("YOUR EXPENSES ARE THE SUM OF THE COST OF")
        print("THE LEMONADE AND THE COST OF THE SIGNS.")
        print()
        print("YOUR PROFITS ARE THE DIFFERENCE BETWEEN")
        print("THE INCOME FROM SALES AND YOUR EXPENSES.")
        print()
        print("THE NUMBER OF GLASSES YOU SELL EACH DAY")
        print("DEPENDS ON THE PRICE YOU CHARGE, AND ON")
        print("THE NUMBER OF ADVERTISING SIGNS YOU USE.")
        print()
        print("KEEP TRACK OF YOUR ASSETS, BECAUSE YOU")
        print("CAN'T SPEND MORE MONEY THAN YOU HAVE!")
        print()
        input("PRESS ENTER TO CONTINUE...")
    
    @staticmethod
    def show_daily_report(player: Player, day: int):
        """Show daily financial report for a player"""
        print(f"\n$$ LEMONSVILLE DAILY FINANCIAL REPORT $$")
        print(f"DAY {day}                        STAND {player.id}")
        print()
        print(f"  {player.glasses_sold} GLASSES SOLD")
        print(f"  {Display.format_currency(player.price_per_glass/100)} PER GLASS" + 
              f"                INCOME {Display.format_currency(player.income)}")
        print()
        print(f"  {player.glasses_made} GLASSES MADE")
        print(f"  {player.signs_made} SIGNS MADE" + 
              f"                EXPENSES {Display.format_currency(player.expenses)}")
        print()
        print(f"                PROFIT  {Display.format_currency(player.profit)}")
        print(f"                ASSETS  {Display.format_currency(player.assets)}")
        print()
        input("PRESS ENTER TO CONTINUE...")


class LemonadeStandGame:
    """Main game controller"""
    
    def __init__(self):
        self.game_state = GameState()
        self.weather_system = WeatherSystem()
        self.random_event_system = RandomEventSystem()
        self.sales_calculator = SalesCalculator()
        self.display = Display()
    
    def setup_game(self) -> bool:
        """Setup new game or continue existing"""
        self.display.show_title()
        
        print("HI! WELCOME TO LEMONSVILLE, CALIFORNIA!")
        print()
        print("IN THIS SMALL TOWN, YOU ARE IN CHARGE OF")
        print("RUNNING YOUR OWN LEMONADE STAND. YOU CAN")
        print("COMPETE WITH AS MANY OTHER PEOPLE AS YOU")
        print("WISH, BUT HOW MUCH PROFIT YOU MAKE IS UP")
        print("TO YOU (THE OTHER STANDS' SALES WILL NOT")
        print("AFFECT YOUR BUSINESS IN ANY WAY). IF YOU")
        print("MAKE THE MOST MONEY, YOU'RE THE WINNER!!")
        print()
        
        new_game = InputValidator.get_yes_no("ARE YOU STARTING A NEW GAME? (YES OR NO) ")
        
        if new_game:
            self.display.show_instructions()
            num_players = InputValidator.get_int_input(
                "HOW MANY PEOPLE WILL BE PLAYING ==> ", 1, 30)
            
            # Initialize players
            for i in range(num_players):
                player = Player(
                    id=i+1,
                    assets=self.game_state.constants.STARTING_ASSETS
                )
                self.game_state.players.append(player)
            
            self.game_state.day = 0
        else:
            return self.continue_game()
            
        return True
    
    def continue_game(self) -> bool:
        """Continue existing game"""
        try:
            day = InputValidator.get_int_input(
                "WHAT DAY NUMBER WAS IT? ", 1, 99)
            self.game_state.day = day
            
            num_players = InputValidator.get_int_input(
                "HOW MANY PLAYERS? ", 1, 30)
            
            for i in range(num_players):
                assets = float(input(f"PLAYER {i+1}, HOW MUCH MONEY (ASSETS) DID YOU HAVE? "))
                if assets < 2:
                    print("O.K. - WE'LL START YOU OUT WITH $2.00")
                    assets = 2.0
                elif assets > 40:
                    print("JUST TO BE FAIR, LET'S MAKE THAT $10.00")
                    assets = 10.0
                    
                player = Player(id=i+1, assets=assets)
                self.game_state.players.append(player)
                
        except (ValueError, KeyboardInterrupt):
            return False
            
        return True
    
    def play_day(self):
        """Play one day of the game"""
        self.game_state.day += 1
        self.game_state.lemonade_cost = self.game_state.get_lemonade_cost()
        
        self.display.clear_screen()
        print(f"ON DAY {self.game_state.day}, THE COST OF LEMONADE IS " +
              f"{Display.format_currency(self.game_state.lemonade_cost)}")
        print()
        
        # Current events
        if self.game_state.day == 3:
            print("(YOUR MOTHER QUIT GIVING YOU FREE SUGAR)")
        if self.game_state.day == 7:
            print("(THE PRICE OF LEMONADE MIX JUST WENT UP)")
        
        # Generate weather
        if self.game_state.day < 3:
            self.game_state.weather = Weather.SUNNY
        else:
            self.game_state.weather = self.weather_system.generate_weather()
        
        self.weather_system.display_weather(self.game_state.weather)
        
        # Check for random events
        if self.game_state.day > 2:
            event, multiplier = self.random_event_system.check_random_event(
                self.game_state.day, self.game_state.weather)
            self.game_state.random_event = event
            
            if event == RandomEvent.STREET_WORK and multiplier == -1:
                self.game_state.weather_multiplier = -1  # Special flag
            else:
                self.game_state.weather_multiplier = multiplier
        else:
            self.game_state.weather_multiplier = self.weather_system.get_weather_multiplier(
                self.game_state.weather, self.game_state.day)
        
        # Get player decisions
        self.get_player_decisions()
        
        # Check for thunderstorm
        if (self.game_state.weather == Weather.CLOUDY and 
            random.random() < 0.25):
            self.game_state.weather = Weather.THUNDERSTORM
            self.game_state.weather_multiplier = 0.0
            print("\nWEATHER REPORT: A SEVERE THUNDERSTORM")
            print("HIT LEMONSVILLE EARLIER TODAY, JUST AS")
            print("THE LEMONADE STANDS WERE BEING SET UP.")
            print("UNFORTUNATELY, EVERYTHING WAS RUINED!!")
            input("PRESS ENTER TO CONTINUE...")
        
        # Calculate results
        self.calculate_daily_results()
        
        # Check for bankruptcy
        self.check_bankruptcy()
    
    def get_player_decisions(self):
        """Get decisions from each player"""
        for player in self.game_state.players:
            if player.bankrupt:
                print(f"\nLEMONADE STAND {player.id}")
                print(f"ASSETS {Display.format_currency(player.assets)}")
                print("YOU ARE BANKRUPT, NO DECISIONS FOR YOU TO MAKE.")
                continue
            
            while True:  # Allow player to change decisions
                self.display.clear_screen()
                print(f"LEMONADE STAND {player.id}")
                print(f"ASSETS {Display.format_currency(player.assets)}")
                print()
                
                # Get glasses to make
                max_glasses = int(player.assets / self.game_state.lemonade_cost)
                player.glasses_made = InputValidator.get_int_input(
                    "HOW MANY GLASSES OF LEMONADE DO YOU WISH TO MAKE? ", 
                    0, min(1000, max_glasses))
                
                if player.glasses_made * self.game_state.lemonade_cost > player.assets:
                    print(f"THINK AGAIN!!! YOU HAVE ONLY {Display.format_currency(player.assets)}")
                    print(f"IN CASH AND TO MAKE {player.glasses_made} GLASSES OF")
                    print(f"LEMONADE YOU NEED {Display.format_currency(player.glasses_made * self.game_state.lemonade_cost)} IN CASH.")
                    continue
                
                # Get advertising signs
                remaining_cash = player.assets - (player.glasses_made * self.game_state.lemonade_cost)
                max_signs = int(remaining_cash / self.game_state.constants.SIGN_COST)
                
                print(f"\nHOW MANY ADVERTISING SIGNS ({self.game_state.constants.SIGN_COST * 100:.0f} CENTS")
                player.signs_made = InputValidator.get_int_input(
                    "EACH) DO YOU WANT TO MAKE? ", 0, min(50, max_signs))
                
                if player.signs_made * self.game_state.constants.SIGN_COST > remaining_cash:
                    print(f"THINK AGAIN, YOU HAVE ONLY {Display.format_currency(remaining_cash)}")
                    print("IN CASH LEFT AFTER MAKING YOUR LEMONADE.")
                    continue
                
                # Get price
                player.price_per_glass = InputValidator.get_int_input(
                    "\nWHAT PRICE (IN CENTS) DO YOU WISH TO CHARGE FOR LEMONADE? ", 
                    0, 100)
                
                # Ask if they want to change anything
                change = InputValidator.get_yes_no("\nWOULD YOU LIKE TO CHANGE ANYTHING? ")
                if not change:
                    break
    
    def calculate_daily_results(self):
        """Calculate sales and profits for each player"""
        for player in self.game_state.players:
            if player.bankrupt:
                continue
                
            # Calculate sales
            player.glasses_sold = self.sales_calculator.calculate_sales(
                player, self.game_state.weather_multiplier, 
                self.game_state.random_event, self.game_state.constants)
            
            # Calculate finances
            player.income = player.glasses_sold * player.price_per_glass * 0.01
            player.expenses = (player.signs_made * self.game_state.constants.SIGN_COST + 
                             player.glasses_made * self.game_state.lemonade_cost)
            player.profit = player.income - player.expenses
            player.assets += player.profit
            
            # Show daily report
            if not player.bankrupt:
                self.display.show_daily_report(player, self.game_state.day)
    
    def check_bankruptcy(self):
        """Check and handle player bankruptcy"""
        for player in self.game_state.players:
            if (not player.bankrupt and 
                player.assets <= self.game_state.lemonade_cost):
                print(f"\nSTAND {player.id}")
                print("...YOU DON'T HAVE ENOUGH MONEY LEFT")
                print("TO STAY IN BUSINESS  YOU'RE BANKRUPT!")
                player.bankrupt = True
                input("PRESS ENTER TO CONTINUE...")
    
    def is_game_over(self) -> bool:
        """Check if game should end"""
        active_players = [p for p in self.game_state.players if not p.bankrupt]
        return len(active_players) == 0
    
    def show_final_results(self):
        """Show final game results"""
        print("\n" + "="*50)
        print("FINAL RESULTS")
        print("="*50)
        
        # Sort players by assets
        sorted_players = sorted(self.game_state.players, 
                              key=lambda p: p.assets, reverse=True)
        
        for i, player in enumerate(sorted_players, 1):
            status = " (BANKRUPT)" if player.bankrupt else ""
            print(f"{i}. STAND {player.id}: {Display.format_currency(player.assets)}{status}")
        
        if not sorted_players[0].bankrupt:
            print(f"\n🏆 STAND {sorted_players[0].id} WINS! 🏆")
    
    def run(self):
        """Main game loop"""
        try:
            if not self.setup_game():
                return
            
            print("\n...READY TO BEGIN? ", end="")
            input()
            
            while not self.is_game_over():
                self.play_day()
                
                if self.is_game_over():
                    break
                    
                # Optional: Add a way to quit mid-game
                
            self.show_final_results()
            
            play_again = InputValidator.get_yes_no("\nWOULD YOU LIKE TO PLAY AGAIN? ")
            if play_again:
                self.__init__()  # Reset game
                self.run()
                
        except KeyboardInterrupt:
            print("\n\nThanks for playing Lemonade Stand!")


if __name__ == "__main__":
    game = LemonadeStandGame()
    game.run()
