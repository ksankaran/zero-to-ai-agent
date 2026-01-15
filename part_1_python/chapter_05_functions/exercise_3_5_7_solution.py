# From: Zero to AI Agent, Chapter 5, Section 5.7
# File: exercise_3_5_7_solution.py
# Game utilities module demonstrating classes and functions

import random

class Player:
    """Player class with name, score, and level"""
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.level = 1
        self.games_played = 0

    def add_score(self, points):
        """Add points to player's score"""
        self.score += points
        # Level up every 100 points
        new_level = (self.score // 100) + 1
        if new_level > self.level:
            self.level = new_level
            return f"Level up! You're now level {self.level}!"
        return None

    def __str__(self):
        return f"Player: {self.name} | Score: {self.score} | Level: {self.level}"

def roll_dice(sides=6):
    """Roll a dice with specified number of sides"""
    return random.randint(1, sides)

def flip_coin():
    """Flip a coin, returns 'heads' or 'tails'"""
    return random.choice(['heads', 'tails'])

def draw_card():
    """Draw a random playing card"""
    suits = ['S', 'H', 'D', 'C']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return f"{random.choice(ranks)}{random.choice(suits)}"

def generate_random_number(min_val=1, max_val=100):
    """Generate random number in range"""
    return random.randint(min_val, max_val)

class Game:
    """Main game class that uses Player class and game functions"""
    def __init__(self):
        self.players = []
        self.current_player = None
        self.high_scores = []

    def add_player(self, name):
        """Add a new player to the game"""
        player = Player(name)
        self.players.append(player)
        return player

    def set_current_player(self, player):
        """Set the active player"""
        if player in self.players:
            self.current_player = player
            return True
        return False

    def play_dice_game(self):
        """Simple dice rolling game"""
        if not self.current_player:
            return "No player selected!"

        print(f"\n{self.current_player.name}'s turn!")
        input("Press Enter to roll the dice...")

        player_roll = roll_dice()
        computer_roll = roll_dice()

        print(f"You rolled: {player_roll}")
        print(f"Computer rolled: {computer_roll}")

        if player_roll > computer_roll:
            points = 10 * player_roll
            self.current_player.add_score(points)
            result = f"You win! +{points} points"
        elif player_roll < computer_roll:
            result = "Computer wins this round!"
        else:
            points = 5
            self.current_player.add_score(points)
            result = f"It's a tie! +{points} points"

        self.current_player.games_played += 1
        return result

    def play_number_guess(self):
        """Number guessing game"""
        if not self.current_player:
            return "No player selected!"

        secret = generate_random_number(1, 10)
        max_guesses = 3
        points_possible = 30

        print(f"\n{self.current_player.name}, guess the number (1-10)!")
        print(f"You have {max_guesses} guesses.")

        for attempt in range(1, max_guesses + 1):
            guess = int(input(f"Guess #{attempt}: "))

            if guess == secret:
                points = points_possible - (attempt - 1) * 10
                level_msg = self.current_player.add_score(points)
                print(f"Correct! +{points} points")
                if level_msg:
                    print(level_msg)
                return True
            elif guess < secret:
                print("Too low!")
            else:
                print("Too high!")

        print(f"Out of guesses! The number was {secret}")
        return False

    def play_card_match(self):
        """Simple card matching game"""
        if not self.current_player:
            return "No player selected!"

        print(f"\n{self.current_player.name}, let's play Card Match!")
        input("Press Enter to draw your card...")

        your_card = draw_card()
        print(f"Your card: {your_card}")

        input("Press Enter to see if you match...")
        computer_card = draw_card()
        print(f"Computer's card: {computer_card}")

        # Check for matches (same rank or suit)
        if your_card[:-1] == computer_card[:-1]:  # Same rank
            points = 50
            self.current_player.add_score(points)
            return f"Rank match! +{points} points!"
        elif your_card[-1] == computer_card[-1]:  # Same suit
            points = 25
            self.current_player.add_score(points)
            return f"Suit match! +{points} points!"
        else:
            return "No match this time!"

    def show_scoreboard(self):
        """Display all players' scores"""
        if not self.players:
            return "No players yet!"

        print("\nSCOREBOARD")
        print("=" * 40)
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player}")
        print("=" * 40)

# Make it playable when run directly
if __name__ == "__main__":
    print("=" * 40)
    print("Welcome to Mini Game Module!")
    print("=" * 40)

    game = Game()

    # Get player name
    name = input("Enter your name: ")
    player = game.add_player(name)
    game.set_current_player(player)

    print(f"\nWelcome, {name}!")

    # Game loop
    while True:
        print(f"\n{player}")
        print("\nChoose a game:")
        print("1. Dice Rolling")
        print("2. Number Guessing")
        print("3. Card Matching")
        print("4. Show Scoreboard")
        print("5. Quit")

        choice = input("\nYour choice (1-5): ")

        if choice == "1":
            result = game.play_dice_game()
            print(result)
        elif choice == "2":
            game.play_number_guess()
        elif choice == "3":
            result = game.play_card_match()
            print(result)
        elif choice == "4":
            game.show_scoreboard()
        elif choice == "5":
            print(f"\nThanks for playing, {name}!")
            print(f"Final Score: {player.score}")
            print(f"Level Reached: {player.level}")
            break
        else:
            print("Invalid choice! Please try again.")
