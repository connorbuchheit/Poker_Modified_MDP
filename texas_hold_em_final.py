import random

class Card:
    """Represents a single card with a rank, ignoring suits."""
    
    def __init__(self, rank):
        self.rank = rank

    def __repr__(self):
        return f"{self.rank}"

    def __lt__(self, other):
        return self.rank < other.rank
    
    def __eq__(self, other):
        return self.rank == other.rank

class Deck:
    """Represents a deck of 52 cards with ranks from 1 to 13 (ignoring suits)."""
    
    def __init__(self):
        self.cards = [Card(rank) for rank in range(1, 14)] * 4  # 4 suits, but suits are ignored
        random.shuffle(self.cards)
    
    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]
    
    def reset(self):
        """Reshuffle the deck."""
        self.cards = [Card(rank) for rank in range(1, 14)] * 4  # 4 suits, but suits are ignored
        random.shuffle(self.cards)

class PokerGame:
    """Represents the poker game between two players A and B."""

    def __init__(self):
        self.deck = Deck()
        self.pot = 200  # Each player starts with a 100 bet
        self.player_a_hand = []
        self.player_b_hand = []
        self.community_cards = []
        self.player_a_bet = 100
        self.player_b_bet = 100
        self.current_bet = 100

    def start_game(self):
        """Initialize game state, deal cards, and start a round."""
        self.deck.reset()
        self.pot = 200  # Reset the pot
        self.player_a_hand = self.deck.deal(2)
        self.player_b_hand = self.deck.deal(2)
        self.community_cards = self.deck.deal(3)
        self.player_a_bet = 100
        self.player_b_bet = 100
        self.current_bet = 100  # Initial bet amount

    def take_action(self, action):
        """Take an action and update the game state."""
        if action == "raise":
            self.pot += 100  # Increase the pot by $100
            self.player_a_bet += 100  # Player A raises
            self.current_bet = self.player_a_bet  # New bet is Player A's bet
        elif action == "check":
            pass  # Do nothing if Player A checks (Player B's turn)
        
        # Now it's Player B's turn (following a fixed strategy)
        result = self.simulate_game()
        reward = result["reward"]
        done = result["done"]
        return self.get_state(), reward, done

    def simulate_game(self):
        """Simulate the game after Player A's action and determine the result."""
        # For simplicity, let's assume Player B always calls if Player A raises.
        # We can implement Player B's strategy here.
        winner = self.determine_winner()
        if winner == "Player A":
            reward = 1  # Player A wins
        elif winner == "Player B":
            reward = 0  # Player B wins
        else:
            reward = 0  # Tie
        
        done = True  # The game ends after Player B's action
        return {"reward": reward, "done": done}

    def determine_winner(self):
        """Determine the winner based on the cards."""
        # Simple comparison based on high card or pair
        a_hand_eval = self.evaluate_hand(self.player_a_hand)
        b_hand_eval = self.evaluate_hand(self.player_b_hand)
        if len(a_hand_eval["pairs"]) > len(b_hand_eval["pairs"]):
            return "Player A"
        elif len(b_hand_eval["pairs"]) > len(a_hand_eval["pairs"]):
            return "Player B"
        else:
            if a_hand_eval["high_card"] > b_hand_eval["high_card"]:
                return "Player A"
            elif b_hand_eval["high_card"] > a_hand_eval["high_card"]:
                return "Player B"
            else:
                return "Tie"

    def evaluate_hand(self, hand):
        """Evaluate the hand strength (pairs and high card)."""
        full_hand = hand + self.community_cards
        ranks = [card.rank for card in full_hand]
        count_ranks = {rank: ranks.count(rank) for rank in ranks}
        pairs = [rank for rank, count in count_ranks.items() if count == 2]
        high_card = max(full_hand, key=lambda card: card.rank)
        return {"pairs": pairs, "high_card": high_card}
    
    def get_state(self):
        """Return the current state as a tuple of Player A's hand, community cards, and bet."""
        return tuple([card.rank for card in self.player_a_hand] +
                     [card.rank for card in self.community_cards] +
                     [self.player_a_bet])

