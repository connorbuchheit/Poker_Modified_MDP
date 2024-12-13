import random
# This implementation is what we are using for the neural network due to its greater complexity. 
# Different design choices scale this up from the other version for Q-Learning.
class TexasHoldEm:
    def __init__(self, num_players=3, starting_stack=1000):
        self.deck = [(rank, suit) for rank in range(1, 14) for suit in 'ABCD']
        self.players = [{'id': i, 'hole_cards': [], 'stack': starting_stack, 'current_bet': 0, 'active': True} for i in range(num_players)]
        self.community_cards = []
        self.current_bet = 100
        self.pot = 0

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_hole_cards(self):
        for player in self.players:
            player['hole_cards'] = [self.deck.pop(), self.deck.pop()]
            print(f"Player {player['id']}'s cards: {player['hole_cards']}")
    
    def deal_community_cards(self, num_cards=5): # Deal three cards normally in actual implementation
        for _ in range(num_cards):
            self.community_cards.append(self.deck.pop())

    def reset_bets(self):
        for player in self.players:
            player['current_bet'] = 0

    def betting_round(self):
        num_active = sum(player['active'] for player in self.players)
        if num_active <= 1:
            return

        for idx, player in enumerate(self.players):
            if player['active']:
                # print(f"Player {player['id']}'s stack: {player['stack']}")
                action = random.choice(['fold', 'call', 'raise']) # TODO — Fix different action
                if action == 'fold':
                    self.players[idx]['active'] = False 
                    print(f"Player {player['id']} folds")

                elif action == 'call':
                    print(f"Player {player['id']} CALLING!")
                    call_amount = self.current_bet - self.players[idx]['current_bet']
                    call_amount = min(call_amount, self.players[idx]['stack']) # in case of all-in
                    self.players[idx]['stack'] -= call_amount
                    self.players[idx]['current_bet'] += call_amount
                    self.pot += call_amount
                    print(f"Current bet: {self.current_bet}")

                elif action == 'raise':
                    print(f"Player {player['id']} RAISING!")
                    raise_amount = 100  
                    difference = (self.current_bet + raise_amount) - player['current_bet']
                    difference = min(difference, player['stack'])  
                    player['stack'] -= difference
                    player['current_bet'] += difference
                    self.pot += difference
                    self.current_bet += raise_amount
                    print(f"Current bet: {self.current_bet}")
                    

    def determine_winner(self):
        active_players = [p for p in self.players if p['active']]
        if not active_players:
            print("Everyone folded! No winner.")
            return None

        def hand_strength(player):
            hole_cards = player['hole_cards']
            return max(card[0] for card in hole_cards)

        winner = max(active_players, key=hand_strength)
        print(f"Player {winner['id']} wins the pot of {self.pot} chips!")
        winner['stack'] += self.pot
        return winner['id'] # TODO: Maybe modify to handle different winning hands.

    def play_hand(self):
        self.shuffle_deck()
        self.deal_hole_cards()
        print("Hole cards dealt.")
        self.betting_round()

        self.deal_community_cards(3)
        print("Flop:", self.community_cards)
        self.betting_round()

        self.deal_community_cards(1)
        print("Turn:", self.community_cards)
        self.betting_round()

        self.deal_community_cards(1)
        print("River:", self.community_cards)
        self.betting_round()

        self.determine_winner()
        self.reset_bets()

if __name__ == "__main__":
    game = TexasHoldEm()
    game.play_hand()