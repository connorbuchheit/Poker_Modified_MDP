import numpy as np

class SimpleGame:
    def __init__(self, opponent_strat='random'):
        self.opponent_strategy = opponent_strat
        self.reset()

    def reset(self):
        self.deck = list(range(1,14)) * 4 # cards from 1-13 
        np.random.shuffle(self.deck)

        self.player0_cards = [self.deck.pop(), self.deck.pop()] # deal two cars each
        self.player1_cards = [self.deck.pop(), self.deck.pop()] # I say player 0 and player 1 for easier boolean logic in simple case
        self.pot = 0 # initialize reward pot
        self.current_player = 0
        self.done = False
        self.winner = None 
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

    def step(self, action, bet_amt=100):
        if self.done:
            raise ValueError("Game over. Call reset().")

        if action == "bet": 
            self.pot += bet_amt
        elif action == "fold":
            self.done = True
            self.winner = 2  # Tie if we fold.
            return self.max_card(), self.done, self.winner

        # Opponent always raises
        self.pot += bet_amt

        # End game and determine winner
        self.done = True
        self.determine_winner()

        return self.max_card(), self.done, self.winner
    
    def determine_winner(self):
        if max(self.player0_cards) > max(self.player1_cards):
            self.winner = 0
        elif max(self.player0_cards) < max(self.player1_cards):
            self.winner = 1
        else:
            self.winner = 2 # Tie 

    def get_opponent_action(self):
        if self.opponent_strategy == 'raise':
            return 'bet'
        else:
            return np.random.choice(['bet', 'fold'])


# def simulate_random_games(num_games):
#     results = []
#     for _ in range(num_games):
#         game = SimpleGame()
#         pot, player, p0_cards = game.reset()
#         done = False
#         while not done:
#             if player == 0: # This is equal to self.current_player
#                 action = np.random.choice(['bet', 'fold'])
#             elif player == 1:
#                 action = game.get_opponent_action()
#             bet_amt = 100 if action == 'bet' else 0
#             state, done, winner, player = game.step(action, bet_amt)
#         results.append(winner)
#     return results

# Run n simulations
# n = 100000
# results = simulate_random_games(n)
# print(f"Player 0 wins: {results.count(0) / n}%, Player 1 wins: {results.count(1) / n}%")
# print(f"Ties: {results.count(2) / n}%")