import numpy as np

class SimpleGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.deck = list(range(1,14)) # cards from 1-13 
        np.random.shuffle(self.deck)

        self.player0_card = self.deck.pop() # deal one card each
        self.player1_card = self.deck.pop() # I say player 0 and player 1 for easier boolean logic in simple case
        self.pot = 0 # initialize reward pot
        self.current_player = 0 # player 1 begins the game
        self.done = False
        self.winner = None 
        return self.get_state()
    
    def get_state(self):
        return {'pot': self.pot, 
                'current_player': self.current_player,
                'player1_card': self.player0_card,
                'player2_card': self.player1_card} # TODO: Do we wanna reveal both cards?
    
    def step(self, action, bet_amt):
        if self.done:
            raise ValueError('Game over. Call reset()')
        
   
        if action == 'bet': # is it better to rep as 0 and 1? prob not
            self.pot += bet_amt # TODO: Play with the bet amt and see how things change
            self.current_player = (self.current_player + 1) % 2 # should appropriately update
        elif action == 'fold':
            self.done = True 
            self.current_player = (self.current_player + 1) % 2
            self.winner = self.current_player 

        return self.get_state(), self.done, self.winner 
    
    def determine_winner(self):
        if self.player0_card > self.player1_card:
            self.winner = 0
        elif self.player0_card < self.player1_card:
            self.winner = 1
        else:
            self.winner = 0 # Tie — probably play again in this case.


