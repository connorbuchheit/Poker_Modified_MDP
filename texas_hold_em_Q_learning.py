import random
from texas_hold_em_final import HoldEm

class QLearningAgent:
    def __init__(self, action_space, state_space, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha        # Learning rate
        self.gamma = gamma        # Discount factor
        self.epsilon = epsilon    # Exploration rate
        self.action_space = action_space
        self.q_table = {}         # Q-table (a dictionary for storing state-action pairs and their values)
    
    def choose_action(self, state):
        """Choose an action using epsilon-greedy strategy."""
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.action_space)  # Explore: choose a random action
        else:
            raise_flag = False
            if state not in self.q_table:
                self.q_table[state] = {action: 0 for action in self.action_space}  # Initialize if not present
                raise_flag = True
            # print(self.q_table[state])
            # Exploit: choose the action with the highest Q-value for the current state
            if raise_flag == True:
                return 'raise'
            return max(self.q_table[state], key=self.q_table[state].get)

    def update_q_table(self, state, action, reward, next_state):
        """Update the Q-table based on the Q-learning update rule."""
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in self.action_space}
        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0 for action in self.action_space}
        # print(reward)
        best_next_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        self.q_table[state][action] += self.alpha * (td_target - self.q_table[state][action])

        # print(state, action)
        # print(self.q_table[state][action])

    def get_state(self, game):
        """Convert the current game state into a state representation."""
        pair = False
        total_cards = game.player_a_hand + game.community_cards
        if len(set(card.rank for card in total_cards)) < 5:
            pair = True

        return tuple([pair] +
                     [max([card.rank for card in game.community_cards])])
    
    def train(self, game, episodes=1000):
        """Train the agent over a number of episodes."""
        for episode in range(episodes):
            game.start_game()  # Reset game state for the start of the episode
            
            done = False
            while not done:
                state = self.get_state(game)
                # print(state)
                action = self.choose_action(state)  # Choose action using the epsilon-greedy policy
                
                # Take the action and observe the outcome
                result = game.take_action(action)
                reward_a, reward_b, done = result["reward_a"], result["reward_b"], result["done"]
                
                # Update the Q-table using the reward received for Player A
                next_state = self.get_state(game)  # Get the next state
                self.update_q_table(state, action, reward_a, next_state)  # Update Q-values based on the reward

                # Player A's profit is calculated as reward_a - their bet
                # You could optionally store stats here (e.g., to track total profit)
    
def test_agent(agent, games=1000):
    """Test the agent against the same fixed strategy for a given number of games."""
    total_profit = 0
    
    for _ in range(games):
        game = HoldEm()  # Use your poker game class
        game.start_game()
        
        done = False
        while not done:
            # Get the current state before taking an action
            state = agent.get_state(game)
            
            # Choose an action using the agent's policy (epsilon-greedy)
            action = agent.choose_action(state)
            # action = 'raise'
            # print(action)
            
            # Take action and receive the next state and reward from the environment
            result = game.take_action(action)
            reward_a, reward_b, done = result["reward_a"], result["reward_b"], result["done"]
            
            # Update the Q-table based on the reward received and next state
            next_state = agent.get_state(game)
            agent.update_q_table(state, action, reward_a, next_state)
            
            # Player A's profit is their reward minus their bet
            total_profit += reward_a

    # Calculate average profit after all games
    average_profit = total_profit / games
    print(f"Average profit for Player A after {games} games: ${average_profit:.2f}")

# Train agent A
agent_a = QLearningAgent(action_space=["check", "raise"], state_space="state_space")
game = HoldEm()
agent_a.train(game, episodes=10000)

# Test agent A against fixed strategy (Player B)
test_agent(agent_a, games=10000)