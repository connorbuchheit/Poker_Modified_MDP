import random

class TexasHoldEm:
    def __init__(self, num_players=3, starting_stack=1000):
        self.deck = [(rank, suit) for rank in range(1, 14) for suit in 'ABCD']
        self.players = [{'id': i, 'hole_cards': [], 'stack': starting_stack, 'current_bet': 0, 'active': True} for i in range(num_players)]
        self.community_cards = []
        self.current_bet = 50
        self.pot = 0

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_hole_cards(self):
        for player in self.players:
            player['hole_cards'] = [self.deck.pop(), self.deck.pop()]
            print(f"Player {player['id']}'s cards: {player['hole_cards']}")
    
    def deal_community_cards(self, num_cards=5): # Deal three cards
        for _ in range(num_cards):
            self.community_cards.append(self.deck.pop())

    def reset_bets(self):
        for player in self.players:
            player['current_bet'] = 0

    def betting_round(self):
        num_active = sum(player['active'] for player in self.players)
        if num_active <= 1:
            return

        for player in self.players:
            if player['active']:
                self.pot += self.current_bet # may not work
                player['stack'] -= self.current_bet
                print(f"Player {player['id']}'s stack: {player['stack']}")
                action = random.choice(['fold', 'call', 'raise']) # TODO — Fix different action
                if action == 'fold':
                    player['active'] = False 
                    print(f"Player {player['id']} folds")
                elif action == 'call':
                    call_amount = self.current_bet - player['current_bet']
                    call_amount = min(call_amount, player['stack'])  # Handle "all-in" cases
                    player['stack'] -= call_amount
                    player['current_bet'] += call_amount
                    print(f"Player {player['id']} bets {call_amount}")
                    self.pot += call_amount
                elif action == 'raise':
                    raise_amount = 100  
                    difference = (self.current_bet + raise_amount) - player['current_bet']
                    print(f"Player {player['id']} raises {difference}")
                    difference = min(difference, player['stack'])  # Handle "all-in" cases
                    player['stack'] -= difference
                    player['current_bet'] += difference
                    self.pot += difference
                    self.current_bet += raise_amount

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

        # Flop
        self.deal_community_cards(3)
        print("Flop:", self.community_cards)
        self.reset_bets()
        self.betting_round()

        # Turn
        self.deal_community_cards(1)
        print("Turn:", self.community_cards)
        self.reset_bets()
        self.betting_round()

        # River
        self.deal_community_cards(1)
        print("River:", self.community_cards)
        self.reset_bets()
        self.betting_round()

        # Showdown
        self.determine_winner()

if __name__ == "__main__":
    game = TexasHoldEm()
    game.play_hand()