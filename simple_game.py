import numpy as np

class SimpleGame:
    def __init__(self):
        self.reset()

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

    # def step(self, action, bet_amt=100):
    #     if self.done:
    #         raise ValueError('Game over. Call reset()')
   
    #     if action == 'bet': 
    #         self.pot += bet_amt # TODO: Play with the bet amt and see how things change
    #         self.current_player = (self.current_player + 1) % 2 # should appropriately update
    #     elif action == 'fold':
    #         self.done = True 
    #         self.current_player = (self.current_player + 1) % 2
    #         if self.pot != 0:
    #             self.winner = self.current_player 
    #         else:
    #             self.winner = 2 # Tie
            
    #     if self.turns >= self.max_turns:
    #         self.done = True
    #         self.determine_winner()

    #     return self.max_card(), self.done, self.winner, self.current_player

    def step(self, action_a, bet_amt=100):
        if self.done:
            raise ValueError("Game over. Call reset().")

        # player 0 action
        if action_a == "raise":
            self.pot += bet_amt
            self.bet_a += bet_amt
            self.player1_response = "call" if max(self.player1_cards) >= 8 else "fold"
        elif action_a == "check":
            self.player1_response = "call"
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


def simulate_games(num_games):
    results = {'Player 0 wins': 0, 'Player 1 wins': 0, 'Ties': 0}
    total_profit = 0 # for player a, keeping track of profit
    for _ in range(num_games):
        game = SimpleGame()  
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
results, avg_profit = simulate_games(n) # with a random strategy
# print(f"Player 0 wins: {results.count(0) / n}%, Player 1 wins: {results.count(1) / n}%")
print(f"Avg profit for a w random strat: {avg_profit}")