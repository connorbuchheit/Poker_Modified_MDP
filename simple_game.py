import numpy as np

class SimpleGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.deck = list(range(1,14)) * 4 # cards from 1-13 
        np.random.shuffle(self.deck)

        self.player0_cards = [self.deck.pop(), self.deck.pop()] # deal two cars each
        self.player1_cards = [self.deck.pop(), self.deck.pop()] # I say player 0 and player 1 for easier boolean logic in simple case
        self.pot = 0 # initialize reward pot
        self.current_player = 0 # player 1 begins the game
        self.done = False
        self.winner = None 
        return self.get_state()

    def get_state(self):
        return (self.pot, self.current_player, tuple(self.player0_cards), tuple(self.player1_cards)) # TODO: Should both players be visible?

    
    def step(self, action, bet_amt=100):
        if self.done:
            raise ValueError('Game over. Call reset()')
   
        if action == 'bet': 
            self.pot += bet_amt # TODO: Play with the bet amt and see how things change
            self.current_player = (self.current_player + 1) % 2 # should appropriately update
        elif action == 'fold':
            self.done = True 
            self.current_player = (self.current_player + 1) % 2
            self.winner = self.current_player 

        return self.get_state(), self.done, self.winner 
    
    def determine_winner(self):
        if max(self.player0_cards) > max(self.player1_cards):
            self.winner = 0
        elif max(self.player0_cards) < max(self.player1_cards):
            self.winner = 1
        else:
            self.winner = 0 # Tie — probably play again in this case.


def simulate_random_games(num_games):
    results = []
    for _ in range(num_games):
        game = SimpleGame()
        state = game.reset()
        done = False
        while not done:
            action = np.random.choice(['bet', 'fold'])
            bet_amt = np.random.randint(1, 11) if action == 'bet' else 0
            try:
                state, done, winner = game.step(action, bet_amt)
            except ValueError:
                break
        results.append(winner)
    return results

# Run n simulations
n = 100000
results = simulate_random_games(n)
print(f"Player 0 wins: {results.count(0) / n}%, Player 1 wins: {results.count(1) / n}%")
