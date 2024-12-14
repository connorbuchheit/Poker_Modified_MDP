import random
from collections import Counter
import numpy as np
from deep_Q_learning import DQLAgent
import numpy as np
# This implementation is what we are using for the neural network due to its greater complexity. 
# Different design choices scale this up from the other version for Q-Learning.
class TexasHoldEm:
    def __init__(self, num_players=4, starting_stack=3000):
        self.deck = [rank for rank in range(1, 14)] * 4
        self.players = [{'id': i, 'hole_cards': [], 'stack': starting_stack, 'current_bet': 0, 'active': True} for i in range(num_players)]
        self.community_cards = []
        self.current_bet = 100
        self.pot = 0
        self.agent = DQLAgent(21, 3) # 21 states (checked), 3 actions, this ONLY works for four players
        self.fixed_strategies = fixed_strategies = [None, 'random', 'always_call', 'conservative'] # give other players strategy

    def shuffle_deck(self):
        self.deck = [rank for rank in range(1, 14)] * 4
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
                # action = random.choice(['call', 'fold', 'raise])
                if idx == 0:  # Player 0 is who we are optimizing for in the neural network that we are training
                    state = self.get_state(0)
                    action_idx = self.agent.choose_action(state)
                    action = ['call', 'raise', 'fold'][action_idx]
                else:  # Fixed strategies for Players 1, 2, 3
                    if self.fixed_strategies[idx] == 'random':
                        action = random.choice(['call', 'raise', 'fold'])
                    elif self.fixed_strategies[idx] == 'always_call':
                        action = 'call'
                    elif self.fixed_strategies[idx] == 'conservative':
                        if player['stack'] > self.current_bet * 2:  # Example conservative logic
                            action = 'call'
                        else:
                            action = 'fold'
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
            full_hand = player['hole_cards'] + self.community_cards
            counts = Counter(full_hand)  # Count triples, pairs, etc
            triples = [card for card, count in counts.items() if count == 3]
            pairs = [card for card, count in counts.items() if count == 2]
            singles = [card for card, count in counts.items() if count == 1]

            # sort so if there is a tie the rank wins
            triples.sort(reverse=True)
            pairs.sort(reverse=True)
            singles.sort(reverse=True)

            if triples:
                return (3, triples[0])  # Priority 3: Three of a kind, return highest suit with all.
            elif len(pairs) >= 2:
                return (2, pairs[0])      # Priority 2: Two pairs
            elif pairs:
                return (1, pairs[0])         # Priority 1: One pair
            else:
                return (0, singles[0])                # Priority 0: High card
            
        player_scores = [(player['id'], hand_strength(player)) for player in active_players]

        winner = max(player_scores, key=lambda x: (x[1][0], x[1][1], random.random())) # Random value added in fringe case of tie. No splititng pot.

        winning_player = next(p for p in self.players if p['id'] == winner[0])
        print(f"Player {winning_player['id']} wins the pot of {self.pot} chips!")
        winning_player['stack'] += self.pot
        self.pot = 0 # give pot to winner, set back to 0
        return winning_player['id'] 
    
    def calculate_reward(self, player_id, winner_id):
        player = self.players[player_id]
        if winner_id == player_id:
            # Player wins the pot
            return self.pot
        elif not player['active']:
            # Player folded
            return -player['current_bet']
        else:
            # Player lost at showdown
            return -player['current_bet']
    
    def play_hand(self):
        self.shuffle_deck()
        self.community_cards = []  # Clear community cards
        self.reset_bets()  # Reset player bets
        self.deal_hole_cards()

        print("Hole cards dealt.")

        states, actions, rewards, next_states, dones = [], [], [], [], []

        done = False
        state = self.get_state(0)  # Initial state for Player 0
        while not done:
            action_idx = self.agent.choose_action(state)  # Choose action for Player 0
            action = ['call', 'raise', 'fold'][action_idx]
            actions.append(action_idx)

            # Simulate a round of betting
            self.betting_round()

            # Update the state and check if the hand is done
            next_state = self.get_state(0)
            next_states.append(next_state)

            if len(self.community_cards) == 0:
                self.deal_community_cards(3)
                print("Flop:", self.community_cards)
            elif len(self.community_cards) == 3:
                self.deal_community_cards(1)
                print("Turn:", self.community_cards)
            elif len(self.community_cards) == 4:
                self.deal_community_cards(1)
                print("River:", self.community_cards)

            # Check if the hand is done
            if len(self.community_cards) == 5 or sum(p['active'] for p in self.players) == 1:
                done = True
                print("Final round.")
                winner_id = self.determine_winner()
                reward = self.calculate_reward(0, winner_id)
            else:
                reward = 0

            states.append(state)
            rewards.append(reward)
            dones.append(done)
            state = next_state

        self.reset_bets()
        return states, actions, rewards, next_states, dones



    # def play_hand(self): # Note — this was commented out as it did not have a done criterion
    #     done = False
    #     self.shuffle_deck()
    #     self.deal_hole_cards()
    #     print("Hole cards dealt.")
    #     self.betting_round()

    #     self.deal_community_cards(3)
    #     print("Flop:", self.community_cards)
    #     self.betting_round()

    #     self.deal_community_cards(1)
    #     print("Turn:", self.community_cards)
    #     self.betting_round()

    #     self.deal_community_cards(1)
    #     print("River:", self.community_cards)
    #     self.betting_round()

    #     self.determine_winner()
    #     self.reset_bets()

    def get_state(self, player_id):
        """
        Create a vectorized representation of the current game state for the given player.
        """
        player = self.players[player_id]
        state = []

        # Include player hole cards
        state.extend(player['hole_cards'])

        # Include community cards, pad them with 0s so there are always 5
        state.extend(self.community_cards + [0] * (5 - len(self.community_cards)))

        # Include player stack size and current bet
        state.append(player['stack'])
        state.append(player['current_bet'])

        # Include the opponent stacks and bets. 
        for other_player in self.players:
            if other_player['id'] != player_id:
                state.append(other_player['stack'])
                state.append(other_player['current_bet'])

        # Include who's active.
        state.extend([1 if p['active'] else 0 for p in self.players])

        # Include pot size and bet.
        state.append(self.pot)
        state.append(self.current_bet)

        return np.array(state, dtype=np.float32)


if __name__ == "__main__":
    game = TexasHoldEm()
    game.play_hand()