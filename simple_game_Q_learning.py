import numpy as np
from collections import defaultdict
from simple_game import SimpleGame

class RLAgent:
    def __init__(self, alpha=0.1, gamma=1, epsilon=0.1):
        self.Q = defaultdict(lambda: np.zeros(2))  # q table
        self.alpha = alpha  # learning rate — tune hyperparams
        self.gamma = gamma  # discount factor 
        self.epsilon = epsilon  # exploration rate

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:  # exploration
            return np.random.choice([0, 1])  
        else:  # exploitation 
            return np.argmax(self.Q[state])  

    def update(self, state, action, reward, next_state, done):
        best_next_action = np.argmax(self.Q[next_state]) if not done else 0
        td_target = reward + self.gamma * self.Q[next_state][best_next_action] * (not done)
        td_error = td_target - self.Q[state][action]
        self.Q[state][action] += self.alpha * td_error

def train_q_learning(num_episodes=1000000, opp_policy='conservative'):
    agent = RLAgent()
    game = SimpleGame(opp_policy=opp_policy)  # Train against a specific strategy

    for _ in range(num_episodes):
        state = game.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            action_name = 'check' if action == 0 else 'raise'
            bet_amt = 100 if action_name == 'bet' else 0

            next_state, done, winner = game.step(action_name)

            # Calculate reward
            if done and winner == 0:  # Player 0 wins
                reward = game.bet_b
            elif done and winner == 1:  # Player 1 wins
                reward = -game.bet_a
            elif done and winner is None:  # Tie
                reward = (game.pot / 2) - game.bet_a
            else:
                reward = 0  # Neutral reward for ongoing action

            # Update Q-table
            agent.update(state, action, reward, next_state, done)
            state = next_state

    return agent

def evaluate_policy(agent, opp_policy='conservative', num_games=1000):
    game = SimpleGame(opp_policy=opp_policy)  # Test against the same strategy
    wins = [0, 0, 0]
    total_profit = 0  # Track total profit/loss for Player 0

    for _ in range(num_games):
        state = game.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            action_name = 'check' if action == 0 else 'raise'
            bet_amt = 100 if action_name == 'raise' else 0
            state, done, winner = game.step(action_name, bet_amt)

        # Track profit/loss for Player 0
        if winner == 0:  # Player 0 wins
            profit = game.pot - game.bet_a
        elif winner == 1:  # Player 1 wins
            profit = -game.bet_a
        else:  # Tie
            profit = -(game.bet_a - (game.pot / 2))  # Player 0's share of the pot in a tie

        total_profit += profit
        wins[winner] += 1

    average_profit = total_profit / num_games
    return wins, average_profit

# Training loop across policies
agent = train_q_learning()
n_train = 1000000
n_eval = 1000000

for policy in ['random', 'always_call', 'conservative']:
    # Train and evaluate Q learning for poicy
    agent = train_q_learning(num_episodes=n_train, opp_policy=policy)
    q_learning_results, q_learning_avg_profit = evaluate_policy(agent, opp_policy=policy, num_games=n_eval)
    
    print(f"Against Player B Strategy: {policy}")
    print(f"Q-Learning Strategy Results: {q_learning_results}")
    print(f"Average Profit for Player A: {q_learning_avg_profit:.2f}")
    print()