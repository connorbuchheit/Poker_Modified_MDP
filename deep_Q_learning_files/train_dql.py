import torch
import numpy as np
from texas_hold_em_complex import TexasHoldEm
from deep_Q_learning import DQLAgent

# Hyperparameters
NUM_EPISODES = 1000
STATE_DIM = 21  # Confirmed from get_state() output
ACTION_DIM = 3  # ['call', 'raise', 'fold']
SAVE_INTERVAL = 100  # Save model every 100 episodes

# Initialize environment and agent
env = TexasHoldEm()
agent = DQLAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM)

# Training loop
# Training loop
for episode in range(NUM_EPISODES):
    print(f"Episode {episode + 1}/{NUM_EPISODES}")

    # Play a single hand
    states, actions, rewards, next_states, dones = env.play_hand()

    # Update the agent with all steps taken during the hand
    for state, action, reward, next_state, done in zip(states, actions, rewards, next_states, dones):
        agent.update(state, action, reward, next_state, done)

    print(f"Episode {episode + 1} finished with total reward: {sum(rewards)}")

    # Save the model periodically
    if (episode + 1) % SAVE_INTERVAL == 0:
        torch.save(agent.model.state_dict(), f'dql_agent_episode_{episode + 1}.pth')
        print(f"Model saved after {episode + 1} episodes.")
