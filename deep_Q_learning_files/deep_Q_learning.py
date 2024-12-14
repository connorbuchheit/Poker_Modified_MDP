import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import numpy as np
import random

# Deep Q Learning on the Texas Holdem 
class NeuralNetwork(nn.Module): # Neural network architeture — arbitrary simple choices, CHANGE IF NEED BE!
    def __init__(self, input_dim, output_dim):
        super(NeuralNetwork, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.layers(x)
    
class DQLAgent:
    def __init__(self, state_dim, action_dim, lr=0.001, gamma=1.0, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.1):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr
        self.gamma = gamma # Set to 1 cause finite horizon?
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

        self.model = NeuralNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

        self.replay_buffer = deque(maxlen=5000)

    def choose_action(self, state):
        """
        Choose an action using an epsilon-greedy policy.
        """
        if np.random.random() < self.epsilon:
            return np.random.choice([0, 1, 2])  # Exploration
        else:
            state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Exploitation, choose w max Q
            q_values = self.model(state_tensor)  
            return torch.argmax(q_values).item()  

    def update(self, state, action, reward, next_state, done):
        """
        Train the Q-network using a single step of experience replay.
        """
        # Add experience to the replay buffer
        self.replay_buffer.append((state, action, reward, next_state, done))

        # Only train if enough samples are in the buffer
        if len(self.replay_buffer) < 64:
            return

        # Sample a batch from the replay buffer
        batch = random.sample(self.replay_buffer, 64)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)

        # Compute target Q-values
        q_next = self.model(next_states).detach().max(1)[0]  # Max Q-value for next state
        targets = rewards + self.gamma * q_next * (1 - dones)

        # Compute current Q-values
        q_values = self.model(states).gather(1, actions).squeeze()

        # Compute loss
        loss = self.criterion(q_values, targets)

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Decay epsilon
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)