# import torch
# import numpy as np
# import matplotlib.pyplot as plt
# from texas_hold_em_complex import TexasHoldEm
# from deep_Q_learning import DQLAgent

# # Hyperparameters
# NUM_EVALUATION_GAMES = 100  # Number of games to evaluate
# STATE_DIM = 10  # Confirmed from get_state() output
# ACTION_DIM = 2  # ['call', 'raise', 'fold']
# MODEL_PATH = 'dql_agent_episode_1000.pth'  # Path to the trained model

# # Initialize environment and agent
# env = TexasHoldEm()
# agent = DQLAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM)

# # Load the trained model
# agent.model.load_state_dict(torch.load(MODEL_PATH))
# agent.model.eval()  # Set the model to evaluation mode

# # Track profits (stack sizes) over games
# profits = {player_id: [] for player_id in range(len(env.players))}

# # Evaluation loop
# for game in range(NUM_EVALUATION_GAMES):
#     print(f"Game {game + 1}/{NUM_EVALUATION_GAMES}")

#     # Play a single hand
#     states, actions, rewards, next_states, dones = env.play_hand()
#     print(f"Player 0 Action: {actions[0]}")


#     # Record stack sizes of all players after the game
#     for player_id, player in enumerate(env.players):
#         profits[player_id].append(player['stack'])

# # Plot the profits of all players over games
# plt.figure(figsize=(10, 6))
# for player_id in profits:
#     plt.plot(profits[player_id], label=f"Player {player_id}")

# plt.title("Player Profits Over Evaluation Games")
# plt.xlabel("Game Number")
# plt.ylabel("Stack Size")
# plt.legend()
# plt.grid()
# plt.savefig("player_profits.png")  # Save the plot as a PNG file
# plt.show()

# print("Evaluation completed. Profit plot saved as 'player_profits.png'.")

import torch
import numpy as np
import matplotlib.pyplot as plt
from texas_hold_em_complex import TexasHoldEm
from deep_Q_learning import DQLAgent

# Hyperparameters
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
