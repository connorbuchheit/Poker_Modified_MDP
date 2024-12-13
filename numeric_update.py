import pandas as pd
import numpy as np

def update(table_probabilities,
           eta,
           all_pairs,
           opp_probs,
           num_iter):
    
    eps_error = 10 ** (-4)

    table_prob_new = table_probabilities.copy()
    # print(table_probabilities.index)

    # first, update for player A:
    for pair_A in all_pairs:

        # compute the average profit given current policy
        # if checks
        sum_checks = 0
        for pair_B in all_pairs:

            profit = 0
            if max(pair_A) > max(pair_B):
                profit = 100
            elif max(pair_A) < max(pair_B):
                profit = -100
            # this is the average contribution to the sum
            sum_checks += profit * opp_probs.loc[[pair_A],[pair_B]].iat[0,0]


        
        # if raises
        sum_raises = 0
        for pair_B in all_pairs:

            profit = 0
            if max(pair_A) > max(pair_B):
                # profit is 200 if call, 100 if they fold
                profit = 200 * table_probabilities.loc['B (raised)', [pair_B]] + 100 * (1 - table_probabilities.loc['B (raised)', [pair_B]])
            elif max(pair_A) < max(pair_B):
                # profit is -200 if call, 100 if they fold
                profit = (-200) * table_probabilities.loc['B (raised)', [pair_B]] + 100 * (1 - table_probabilities.loc['B (raised)', [pair_B]])
            elif max(pair_A) == max(pair_B):
                # profit is 0 if call, 100 if they fold
                profit = 100 * (1 - table_probabilities.loc['B (raised)', [pair_B]])

            # print(profit)
            # the average contribution to the sum
            sum_raises += profit.iloc[0] * opp_probs.loc[[pair_A],[pair_B]].iat[0,0]

        # print(sum_checks)
        # print(sum_raises)
        if sum_checks > sum_raises:
            # decrease the probability of raising
            if table_probabilities.loc['A', [pair_A]].iloc[0] > 0 + eta - eps_error:
                table_prob_new.loc['A', [pair_A]] -= eta
        elif sum_checks < sum_raises:
            # increase the probability of raising
            if table_probabilities.loc['A', [pair_A]].iloc[0] < 1 - eta + eps_error:
                table_prob_new.loc['A', [pair_A]] += eta

        if pair_A == (1,1):
            print(sum_checks, "Checks")
            print(sum_raises, "Raises")

    # now, update for player B:
    # now, we're in the situation where A raised
    # (if A checked, then B should always play)

    for pair_B in all_pairs:

        table_probabilities.loc['A (norm)'] = table_probabilities.loc['A'] / table_probabilities.loc['A'].sum()

        # if calls:
        sum_calls = 0
        for pair_A in all_pairs:

            profit = 0
            if max(pair_B) > max(pair_A):
                profit = 200
            if max(pair_B) < max(pair_A):
                profit = -200
            sum_calls += profit * table_probabilities.loc['A (norm)', [pair_A]].iloc[0]
        
        sum_folds = -100

        # now, compare the two and choose the one that gives higher reward:
        if sum_calls > sum_folds:
            if table_probabilities.loc['B (raised)', [pair_B]].iloc[0] < 1 - eta + eps_error:
                table_prob_new.loc['B (raised)', [pair_B]] += eta
        if sum_calls < sum_folds:
            if table_probabilities.loc['B (raised)', [pair_B]].iloc[0] > 0 + eta - eps_error:
                table_prob_new.loc['B (raised)', [pair_B]] -= eta

    table_prob_new = (table_prob_new / eta).round() * eta
    
    print(table_prob_new)
    print(f"Iter {num_iter} completed.")

    return table_prob_new