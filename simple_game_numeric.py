import numpy as np
import pandas as pd
from numeric_update import update

n_pairs = 13 * 12 / 2 + 13

def compute_pair_prob(my_cards, your_cards):
    remaining = np.ones(14) * 4
    remaining[my_cards[0]] -= 1
    remaining[my_cards[1]] -= 1

    prob = 0

    # if you don't hold a pair:
    if your_cards[0] != your_cards[1]:
        possible_hands = remaining[your_cards[0]] * remaining[your_cards[1]]
        total_hands = 50 * 49 / 2
        prob = possible_hands / total_hands
    else:
        # if you hold a pair:
        rem_of_pair = remaining[your_cards[0]]
        possible_hands = rem_of_pair * (rem_of_pair - 1) / 2
        total_hands = 50 * 49 / 2
        prob = possible_hands / total_hands

    return prob

def get_single_hand_probs(all_pairs):

    ans = []

    for pair in all_pairs:
        if pair[0] != pair[1]:
            ans.append(4 * 4 / (52 * 51 / 2))
        else:
            ans.append(6 / (52 * 51 / 2))

    return pd.Series(ans, index = all_pairs)


def get_table_of_opp_probs(all_pairs):

    df_opponent_probs = pd.DataFrame(index = all_pairs,
                                     columns = all_pairs)

    for pair1 in all_pairs:
        for pair2 in all_pairs:
            prob_of_opp_having_pair2 = compute_pair_prob(pair1, pair2)
            df_opponent_probs.loc[[pair1], [pair2]] = prob_of_opp_having_pair2

    return df_opponent_probs

def get_all_pairs():

    all_pairs = []

    for a in range(1, 14):
        for b in range(a, 14):
            all_pairs.append((a, b))

    return all_pairs

####################################################

all_pairs = get_all_pairs()
single_hand_probs = get_single_hand_probs(all_pairs)

# opp_probs = get_table_of_opp_probs(all_pairs)
# opp_probs.to_csv('opp_probs.csv')

opp_probs = pd.read_csv('opp_probs.csv', index_col = 0)
opp_probs.columns = [eval(x) for x in opp_probs.columns]
opp_probs.index = [eval(x) for x in opp_probs.index]

# in the table of optimal probs, initialize everyone at 0.5 to start

df_probabilities = pd.DataFrame(0.5,
                                index = ['A', 'B (not raised)', 'B (raised)'],
                                columns = all_pairs)

# if A did not raise, B should always play
df_probabilities.loc['B (not raised)'] = 1

eta = 0.02
episodes = 1000

for i in range(5000):
    df_probabilities = update(df_probabilities,
                              eta,
                              all_pairs,
                              opp_probs,
                              i)
    if i % 100 == 0:
        df_probabilities.to_csv(f'data/opt_probs_iter_{i}.csv')

print(df_probabilities)
