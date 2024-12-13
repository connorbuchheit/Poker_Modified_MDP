import random

class Card:
    
    def __init__(self, rank):
        self.rank = rank

    def __repr__(self):
        return f"{self.rank}"

    def __lt__(self, other):
        return self.rank < other.rank
    
    def __eq__(self, other):
        return self.rank == other.rank

class Deck:
    
    def __init__(self):
        self.cards = [Card(rank) for rank in range(1, 14)] * 4  # 4 suits, but suits are ignored
        random.shuffle(self.cards)
    
    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]
    
    def reset(self):
        self.cards = [Card(rank) for rank in range(1, 14)] * 4  # 4 suits, but suits are ignored
        random.shuffle(self.cards)

class HoldEm:
    
    def __init__(self):
        self.deck = Deck()
        self.pot = 200  # Each player bets 100
        self.player_a_hand = []
        self.player_b_hand = []
        self.community_cards = []
        self.player_a_bet = 100
        self.player_b_bet = 100
        self.current_bet = 100  # Track the current bet after player A's action

    def start_game(self):
        """Initialize game state, deal cards, and start the round."""
        self.deck.reset()
        self.pot = 200  # Reset pot
        self.player_a_hand = self.deck.deal(2)
        self.player_b_hand = self.deck.deal(2)
        self.community_cards = self.deck.deal(3)  # Deal 3 communal cards
        self.player_a_bet = 100
        self.player_b_bet = 100
        self.current_bet = 100  # Track the current bet
    
    def show_hands(self):
        """Show the current hands of both players."""
        return {
            "Player A Hand": self.player_a_hand,
            "Player B Hand": self.player_b_hand,
            "Community Cards": self.community_cards,
            "Pot": self.pot,
            "Player A Bet": self.player_a_bet,
            "Player B Bet": self.player_b_bet
        }

    def evaluate_hand(self, hand):
        """Evaluate hand strength based on high cards and pairs."""
        full_hand = hand + self.community_cards
        ranks = [card.rank for card in full_hand]
        count_ranks = {rank: ranks.count(rank) for rank in ranks}
        
        pairs = [rank for rank, count in count_ranks.items() if count == 2]
        high_card = max(full_hand, key=lambda card: card.rank)
        
        return {"pairs": pairs, "high_card": high_card}

    def player_a_action(self, action):
        if action == 'raise':
            self.pot += 100  # Increase the pot by $100
            self.player_a_bet += 100  # Player A's new bet is $200
            self.current_bet = self.player_a_bet  # New current bet is Player A's bet
            print("Player A raises $100.")
        elif action == 'check':
            print("Player A checks.")

    def player_b_action(self):
        """Player B always follows the strategy described."""
        # Evaluate Player B's hand
        b_hand_eval = self.evaluate_hand(self.player_b_hand)
        has_pair = len(b_hand_eval["pairs"]) >= 1
        high_card_b = b_hand_eval["high_card"].rank

        if self.current_bet == 100:  # A checked, so B calls
            print("Player B calls (because A checked).")
            self.pot += self.player_b_bet  # Player B matches the bet
            self.player_b_bet = self.current_bet
            return

        if self.current_bet > 100:  # Player A raised
            if high_card_b >= 12 or has_pair:  # Player B has a high card (King or higher) or a pair
                print(f"Player B calls (high card: {high_card_b} or pair).")
                if self.player_b_bet < self.current_bet:
                    # Player B calls to match Player A's raise
                    difference = self.current_bet - self.player_b_bet
                    self.pot += difference
                    self.player_b_bet = self.current_bet  # Player B matches the raise
                return
            else:
                print("Player B folds (hand is too weak).")
                return 'Player A', self.pot  # Player B folds, so Player A wins the pot

    def determine_winner(self):
        """Determine the winner of the game based on hand strength."""
        a_hand_eval = self.evaluate_hand(self.player_a_hand)
        b_hand_eval = self.evaluate_hand(self.player_b_hand)

        # Compare based on pairs first (only consider highest pair)
        if len(a_hand_eval["pairs"]) > len(b_hand_eval["pairs"]):
            return "Player A", self.pot
        elif len(b_hand_eval["pairs"]) > len(a_hand_eval["pairs"]):
            return "Player B", self.pot
        else:
            # If pairs are equal, compare the highest card
            if a_hand_eval["high_card"] > b_hand_eval["high_card"]:
                return "Player A", self.pot
            elif b_hand_eval["high_card"] > a_hand_eval["high_card"]:
                return "Player B", self.pot
            else:
                return "Tie", self.pot // 2  # Split pot if it's a tie
    
    def end_game(self):
        """Play a round and determine the winner."""
        winner, winnings = self.determine_winner()
        return winner, winnings
    
    def reset_game(self):
        """Reset the game state for a new round."""
        self.start_game()
