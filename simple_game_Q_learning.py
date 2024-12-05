import numpy as np
from collections import defaultdict
from simple_game import SimpleGame

class RLAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.Q = defaultdict(lambda: np.zeros(2))  # q table
        self.alpha = alpha  # learning rate — tune hyperparams
        self.gamma = gamma  # discount factor 
        self.epsilon = epsilon  # exploration rate

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:  # exploration
            return np.random.choice([0, 1])  
        else:  # exploitation 
            print(state)
            return np.argmax(self.Q[state])  

    def update(self, state, action, reward, next_state, done):
        best_next_action = np.argmax(self.Q[next_state]) if not done else 0
        td_target = reward + self.gamma * self.Q[next_state][best_next_action] * (not done)
        td_error = td_target - self.Q[state][action]
        self.Q[state][action] += self.alpha * td_error

def train_q_learning(num_episodes=100000):
    agent = RLAgent()
    game = SimpleGame()

    for _ in range(num_episodes):
        state = game.reset()  
        done = False
        while not done:
            action = agent.choose_action(state)
            action_name = 'fold' if action == 0 else 'bet'
            bet_amt = 100 if action_name == 'bet' else 0

            next_state, done, winner = game.step(action_name, bet_amt)
            if action_name == 'fold':
                if game.pot == 0:
                    reward = -10
                else:
                    reward = -1 * bet_amt  # Penalize folding slightly
            else:
                reward = game.pot if winner == game.current_player else -100

            agent.update(state, action, reward, next_state, done)
            state = next_state

    return agent

# train
agent = train_q_learning()

# evaluate policy
def evaluate_policy(agent, num_games=1000):
    game = SimpleGame()
    wins = [0, 0]
    for _ in range(num_games):
        state = game.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            action_name = 'fold' if action == 0 else 'bet'
            bet_amt = 100
            state, done, winner = game.step(action_name, bet_amt)
            if action_name == 'fold':
                reward = -bet_amt  # Penalize folding slightly
            else:
                reward = game.pot if winner == game.current_player else -100
        if winner is not None:
            wins[winner] += 1
    return wins

results = evaluate_policy(agent)
print(f"Player 0 wins: {results[0]}, Player 1 wins: {results[1]}")
