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

class HoldEm:
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
        b_action = self.simulate_b_action()

        result = self.simulate_game(b_action)
        reward_a = result["reward_a"]
        reward_b = result["reward_b"]
        done = result["done"]
        print(self.player_a_hand)
        print(self.player_b_hand)
        print(self.community_cards)
        print(action)
        print(b_action)
        print(reward_a)

        return {"reward_a": reward_a, "reward_b": reward_b, "done": done}

    def simulate_b_action(self):
        """Simulate Player B's action based on the fixed strategy."""
        
        if self.player_a_bet == 100:  # Player A checked
            return "call"
        
        # return 'fold'
        
        total_cards_b = self.player_b_hand + self.community_cards
        
        # If Player A raised, Player B will call if they have a high card K or higher or a pair
        high_card_b = max(card.rank for card in total_cards_b)
        has_pair = len(set(card.rank for card in total_cards_b)) < 5
        
        if high_card_b >= 13 or has_pair:  # Player B calls
            if self.player_b_bet < self.current_bet:
                difference = self.current_bet - self.player_b_bet
                self.pot += difference
                self.player_b_bet = self.current_bet

            return "call"
        
        return "fold"
        

    def simulate_game(self, b_action):
        """Simulate the game after Player A's action and determine the result."""
        if b_action == 'call':
            winner = self.determine_winner()
        else:
            winner = "Player A"
        reward_a = 0
        reward_b = 0
        if winner == "Player A":
            reward_a = self.pot  # Player A wins the full pot
            reward_b = 0  # Player B loses
        elif winner == "Player B":
            reward_a = 0  # Player A loses
            reward_b = self.pot  # Player B wins the full pot
        else:  # Tie
            reward_a = self.pot / 2  # Split the pot
            reward_b = self.pot / 2  # Split the pot
        
        done = True  # The game ends after Player B's action
        # print("Pot:", self.pot)
        reward_a = reward_a - self.player_a_bet
        reward_b = reward_b - self.player_b_bet
        # print(reward_a)
        
        return {"reward_a": reward_a, "reward_b": reward_b, "done": done}


    def determine_winner(self):
        """Determine the winner based on pairs or high cards."""
        # Evaluate Player A's and Player B's hands
        a_hand_eval = self.evaluate_hand(self.player_a_hand)
        b_hand_eval = self.evaluate_hand(self.player_b_hand)
        
        # Check if either player has a pair
        a_has_pair = len(a_hand_eval["pairs"]) > 0
        b_has_pair = len(b_hand_eval["pairs"]) > 0
        
        if a_has_pair and b_has_pair:
            # If both have pairs, compare the highest pair
            a_high_pair = max(a_hand_eval["pairs"])
            b_high_pair = max(b_hand_eval["pairs"])
            if a_high_pair > b_high_pair:
                return "Player A"
            elif b_high_pair > a_high_pair:
                return "Player B"
            else:
                return "Tie"  # Same highest pair, split the pot

        elif a_has_pair:  # Only Player A has a pair
            return "Player A"
        elif b_has_pair:  # Only Player B has a pair
            return "Player B"
        else:
            # If neither player has a pair, compare the highest cards
            a_high_card = a_hand_eval["high_card"]
            b_high_card = b_hand_eval["high_card"]
            if a_high_card > b_high_card:
                return "Player A"
            elif b_high_card > a_high_card:
                return "Player B"
            else:
                return "Tie"  # Same high card, split the pot
    
    def evaluate_hand(self, hand):
        """Evaluate the hand strength (pairs and high card)."""
        full_hand = hand + self.community_cards
        ranks = [card.rank for card in full_hand]
        count_ranks = {rank: ranks.count(rank) for rank in ranks}
        pairs = [rank for rank, count in count_ranks.items() if count == 2]
        high_card = max(full_hand, key=lambda card: card.rank)
        return {"pairs": pairs, "high_card": high_card}

    # def get_state(self):
    #     """Return the current state as a tuple of Player A's hand, community cards, and bet."""
    #     return tuple([card.rank for card in self.player_a_hand] +
    #                  [card.rank for card in self.community_cards] +
    #                  [self.player_a_bet])

