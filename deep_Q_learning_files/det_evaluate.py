import matplotlib.pyplot as plt
import numpy as np
from texas_hold_em_complex import TexasHoldEm

NUM_EVALUATION_GAMES = 10000

# Initialize the environment
env = TexasHoldEm()

# Keep win counter
wins = {player_id: 0 for player_id in range(len(env.players))}

# EvaluATE
for game in range(NUM_EVALUATION_GAMES):
    print(f"Game {game + 1}/{NUM_EVALUATION_GAMES}")

    # Reset the environment and stacks
    env.reset()

    while all(player['stack'] > 0 for player in env.players):
        env.play_hand(player_0_strategy='random')  # Player 0 uses random strategy now

    # Whoever ran out of chips lose
    winner = next(player['id'] for player in env.players if player['stack'] > 0)
    wins[winner] += 1
    print(f"Game {game + 1}: Player {winner} wins!")

print("\nEvaluation Results:")
for player_id, win_count in wins.items():
    print(f"Player {player_id} completely won {win_count} games.")

# Wins
plt.figure(figsize=(8, 5))
plt.bar(wins.keys(), wins.values(), tick_label=[f"Player {player_id}" for player_id in wins.keys()])
plt.title("Complete Wins by Each Player (Random)")
plt.xlabel("Player")
plt.ylabel("Number of Wins")
plt.grid(axis="y")
plt.savefig("random_strategy_wins.png")  
plt.show()
