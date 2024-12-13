import numpy as np

class SimpleGame:
    def __init__(self, opp_policy='conservative'):
        self.reset()
        self.opp_policy='conservative'

    def reset(self):
        self.deck = list(range(1,14)) * 4 # cards from 1-13 
        np.random.shuffle(self.deck)

        self.player0_cards = [self.deck.pop(), self.deck.pop()] # deal two cars each
        self.player1_cards = [self.deck.pop(), self.deck.pop()] # I say player 0 and player 1 for easier boolean logic in simple case
        self.bet_a = 100 # initialize reward pot — costs 100 per player to play
        self.bet_b = 100
        self.pot = 200
        self.current_player = 0
        self.done = False
        self.winner = None 
        self.player1_response = None
        return self.max_card()

    def max_card(self):
        return max(self.player0_cards) # not showing player 1's cards 

    def step(self, action_a, bet_amt=100):
        if self.done:
            raise ValueError("Game over. Call reset().")
        
        # off the bat, determine player 1 action
        if self.opp_policy == 'conservative':
            if action_a == 'raise':
                self.player1_response = "call" if max(self.player1_cards) >= 8 else "fold"
            else:
                self.player1_response = "call"
        elif self.opp_policy == 'random':
            self.player1_response = np.random.choice(['call', 'fold'])
        elif self.opp_policy == 'always_call':
            self.player1_response = 'call'
        else:
            raise ValueError('invalid strategy for b')

        # player 0 action
        if action_a == "raise":
            self.pot += bet_amt
            self.bet_a += bet_amt
        elif action_a == "check":
            pass
        else:
            raise ValueError('invalid action for a. ')

        # player b action
        if self.player1_response == "call":
            if action_a == "raise":
                self.pot += bet_amt
                self.bet_b += bet_amt
            self.done = True
            self.determine_winner()
            return self.max_card(), self.done, self.winner

        elif self.player1_response == "fold":
            self.done = True
            self.winner = 0  # player a wins if player b folds
            return self.max_card(), self.done, self.winner
    
    def determine_winner(self):
        if max(self.player0_cards) > max(self.player1_cards):
            self.winner = 0
        elif max(self.player0_cards) < max(self.player1_cards):
            self.winner = 1
        else:
            self.winner = 2 # Tie 


def simulate_games(num_games, opp_policy):
    results = {'Player 0 wins': 0, 'Player 1 wins': 0, 'Ties': 0}
    total_profit = 0 # for player a, keeping track of profit
    for _ in range(num_games):
        game = SimpleGame(opp_policy=opp_policy)  
        game.reset()
        done = False

        while not done:
            action_a = np.random.choice(['raise', 'check'])
            _, done, winner = game.step(action_a) # game with random action from a

        if winner == 0:  # Player A wins
            profit_a = game.pot - game.bet_a 
        elif winner == 1: # Player B wins 
            profit_a = -game.bet_a  
        else:  # Tie
            profit_a = (game.pot / 2) - game.bet_a  

        total_profit += profit_a

        # Update results based on the winner
        if winner == 0:
            results['Player 0 wins'] += 1
        elif winner == 1:
            results['Player 1 wins'] += 1
        elif winner == 2:
            results['Ties'] += 1

    # Normalize results to percentages
    for key in results:
        results[key] = (results[key] / num_games) * 100
    average_profit_a = total_profit / num_games

    return results, average_profit_a

# Run n simulations
n = 100000
# results, avg_profit = simulate_games(n) # with a random strategy
# # print(f"Player 0 wins: {results.count(0) / n}%, Player 1 wins: {results.count(1) / n}%")
# print(f"Avg profit for a w random strat: {avg_profit}")

for policy in ['random', 'always_call', 'conservative']:
    results, avg_profit = simulate_games(n, opp_policy=policy)
    print(f"Player B Strategy: {policy}")
    print(f"Results: {results}")
    print(f"Avg Profit for Player A: {avg_profit:.2f}")
    print()