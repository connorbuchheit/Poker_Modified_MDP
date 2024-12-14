import torch
import numpy as np
from texas_hold_em_complex import TexasHoldEm
from deep_Q_learning import DQLAgent
import matplotlib.pyplot as plt

# Hyperparameters
NUM_EPISODES = 1000
STATE_DIM = 10  # GREATER FOR FOUR PLAYERS
ACTION_DIM = 2 # ['call', 'raise']
SAVE_INTERVAL = 1000  # Save model every 1000 episodes

# Initialize env and agent
env = TexasHoldEm()
agent = DQLAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM)

# Training loop
for episode in range(NUM_EPISODES):
    print(f"Episode {episode + 1}/{NUM_EPISODES}")

    # Play a complete round
    states, actions, rewards, next_states, dones = env.play_hand()

    # Update the agent with all steps taken during the hand
    for state, action, reward, next_state, done in zip(states, actions, rewards, next_states, dones):
        agent.update(state, action, reward, next_state, done)
    env.reset()

    print(f"Episode {episode + 1} finished with total reward: {sum(rewards)}")

    # Save the mode
    if (episode + 1) % SAVE_INTERVAL == 0:
        torch.save(agent.model.state_dict(), f'dql_agent_episode_{episode + 1}.pth')
        print(f"Model saved after {episode + 1} episodes.")

# Plot the loss 
plt.figure(figsize=(10, 6))
plt.plot(agent.losses, label="Loss")
plt.title("Loss of Neural Network During Training")
plt.xlabel("Training Steps")
plt.ylabel("Loss")
plt.legend()
plt.grid()
plt.savefig("training_loss_plot.png") 
plt.show()