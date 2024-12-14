import torch
import numpy as np
import matplotlib.pyplot as plt
from texas_hold_em_complex import TexasHoldEm
from deep_Q_learning import DQLAgent

NUM_EVALUATION_GAMES = 10000  
STATE_DIM = 10  
ACTION_DIM = 2  # ['call', 'raise']
MODEL_PATH = 'dql_agent_episode_1000.pth'  # Path to trained model

# Initialize env and agent
env = TexasHoldEm()
agent = DQLAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM)

# Load the model
agent.model.load_state_dict(torch.load(MODEL_PATH))
agent.model.eval()  

# Initialize win counters
wins = {player_id: 0 for player_id in range(len(env.players))}

# Evaluation loop
for game in range(NUM_EVALUATION_GAMES):
    print(f"Game {game + 1}/{NUM_EVALUATION_GAMES}")
    
    # Reset the environment so we dont run out of coins
    env.reset()

    # Simulate a complete game until one player goes bankrupt
    while all(player['stack'] > 0 for player in env.players):
        states, actions, rewards, next_states, dones = env.play_hand()

    # Determine the winner (player with chips remaining)
    winner = next(player['id'] for player in env.players if player['stack'] > 0)
    wins[winner] += 1
    print(f"Game {game + 1}: Player {winner} wins!")

# Print the results
print("\nEvaluation Results:")
for player_id, win_count in wins.items():
    print(f"Player {player_id} completely won {win_count} games.")

# Plot the win counts
plt.figure(figsize=(8, 5))
plt.bar(wins.keys(), wins.values(), tick_label=[f"Player {player_id}" for player_id in wins.keys()])
plt.title("Complete Wins by Each Player (Learned Policy)")
plt.xlabel("Player")
plt.ylabel("Number of Wins")
plt.grid(axis="y")
plt.savefig("complete_wins.png")  
plt.show()
