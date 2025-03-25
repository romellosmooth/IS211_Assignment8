class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0

    def add_to_score(self, points):
        self.total_score += points

    def reset_score(self):
        self.total_score = 0
class HumanPlayer(Player):
    def make_decision(self):
        while True:
            decision = input(f"{self.name}, enter 'r' to roll or 'h' to hold: ").lower()
            if decision in ['r', 'h']:
                return decision
            print("Invalid input. Please enter 'r' or 'h'.")
class ComputerPlayer(Player):
    def make_decision(self, turn_total):
        # Strategy: Hold at the lesser of 25 or (100 - current score)
        hold_threshold = min(25, 100 - self.total_score)
        if turn_total >= hold_threshold:
            return 'h'
        return 'r'
class PlayerFactory:

    def create_player(player_type, name):
        if player_type.lower() == "human":
            return HumanPlayer(name)
        elif player_type.lower() == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError(f"Unknown player type: {player_type}")
import time
import random

class Die:
    def __init__(self):
        random.seed(0)  # Ensuring reproducibility
        self.value = 0

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = None

    def start(self):
        self.start_time = time.time()
        while not self.game.is_game_over():
            # Check if the game has exceeded the time limit
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 60:  # Time limit of 1 minute
                print("Time's up!")
                self.declare_winner()
                return
            self.game.play_turn()
        self.declare_winner()

    def declare_winner(self):
        if self.game.player1.total_score > self.game.player2.total_score:
            print(f"Winner: {self.game.player1.name} with {self.game.player1.total_score} points!")
        elif self.game.player2.total_score > self.game.player1.total_score:
            print(f"Winner: {self.game.player2.name} with {self.game.player2.total_score} points!")
        else:
            print("It's a tie!")
class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.die = Die()
        self.current_player = self.player1
        self.turn_total = 0

    def switch_turn(self):
        self.current_player = (
            self.player2 if self.current_player == self.player1 else self.player1
        )
        self.turn_total = 0

    def play_turn(self):
        print(f"{self.current_player.name}'s turn.")
        while True:
            if isinstance(self.current_player, HumanPlayer):
                decision = self.current_player.make_decision()
            else:
                decision = self.current_player.make_decision(self.turn_total)

            if decision == 'r':
                roll = self.die.roll()
                print(f"{self.current_player.name} rolled a {roll}.")
                if roll == 1:
                    print("Rolled a 1! Turn over. No points added.")
                    self.switch_turn()
                    break
                else:
                    self.turn_total += roll
            elif decision == 'h':
                self.current_player.add_to_score(self.turn_total)
                print(f"{self.current_player.name} holds. Total score: {self.current_player.total_score}")
                self.switch_turn()
                break

    def is_game_over(self):
        return self.player1.total_score >= 100 or self.player2.total_score >= 100
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", required=True, choices=["human", "computer"], help="Type of player 1")
    parser.add_argument("--player2", required=True, choices=["human", "computer"], help="Type of player 2")
    parser.add_argument("--timed", action="store_true", help="Enable timed mode")

    args = parser.parse_args(['--player1', 'human', '--player2', 'computer'])


    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")
    game = Game(player1, player2)

    if args.timed:
        proxy = TimedGameProxy(game)
        proxy.start()
    else:
        game.play_turn()
