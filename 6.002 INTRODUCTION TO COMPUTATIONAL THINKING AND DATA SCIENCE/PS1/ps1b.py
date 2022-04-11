###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Berkay Yaldız
# Collaborators:
# Time:
# Author: charz, cdenise

# ================================
# Part B: Golden Eggs
# ================================

# Problem 1
from cmath import inf


def min_dict_finder(memo):
    min_value = inf
    for keys in memo:
        if memo[keys] < min_value:
            min_value = memo[keys]
    return min_value


def dp_make_weight(egg_weights, target_weight, memo={}, memo2={}, smallest_target=inf):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    # Objective function is the minimum number of eggs.
    # Weight limit is the target_weight.
    # Values of each item are just ones.
    # Weights of each item are weights of eggs.
    # I really did find this problem hard because overall I am bad at recursive calls.
    # However, first constructing the three, than solving without dynamic programming was not that bad.
    # After that, I added the dynamic programming part. I recommend watcing this video:https://www.youtube.com/watch?v=oBt53YbR9Kk&t=214s
    # I tried to implement number of eggs for each distinct egg, I cannot make it work. Hence, I make it like a greedy algorithm
    # If you have any recommendations, please contact me via byaldiz604@yahoo.com
    # TODO: Your code here

    if (egg_weights, target_weight) in memo:
        result = memo[(egg_weights, target_weight)]
    elif egg_weights == (1,):
        result = target_weight
    elif egg_weights[-1] > target_weight:
        result = dp_make_weight(
            egg_weights[:-1], target_weight, memo, memo2)[0]
    else:
        # If key value with 1 is added, there is no need to check, already path is added.
        if memo2.get(1, None) == None:
            try:
                memo2[egg_weights[-1]]
                if memo != {}:
                    try:
                        memo2[1]
                    except:
                        smallest_target = min_dict_finder(memo)
                        memo2[1] = smallest_target
                else:
                    if memo2[egg_weights[-1]] < smallest_target:
                        memo2[egg_weights[-1]] += 1
            except:
                if len(memo2) == 2:
                    if memo != {}:
                        try:
                            memo2[1]
                        except:
                            smallest_target = min_dict_finder(memo)
                            memo2[1] = smallest_target
                try:
                    last_key = list(memo2.keys())[-1]
                    if smallest_target - last_key >= egg_weights[-1]:
                        memo2[egg_weights[-1]] = 1
                except:
                    memo2[egg_weights[-1]] = 1

        left_branch_val = dp_make_weight(
            egg_weights, target_weight - egg_weights[-1], memo, memo2, target_weight)
        left_branch_val[0] += 1

        right_branch_val = dp_make_weight(
            egg_weights[:-1], target_weight, memo, memo2, target_weight)

        if left_branch_val[0] < right_branch_val[0]:
            result = left_branch_val[0]
        else:
            result = right_branch_val[0]
    memo[(egg_weights, target_weight)] = result
    return [result, memo2]


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 7, 20)
    n = 938
    #print("Egg weights = (1, 5, 10, 25)")
    #print("n = 99")
    #print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()

    # Problem B.2
    # QUESTION - 1
    # This is because the fact that brute force algorithm checks all possibilities.
    # QUESTION - 2 and 3
    # It can be seen above that greedy algorithm does not return the optimal solution. For example:
    # If we have 938 as target limit, a greddy algorithm selects 46 x 20 2 x 7 and 4 x 1 with a total number of 6 eggs.
    # However, optimal solution is 46 x 20 1 x 7, 2 x 5 and 1 x 1 with a total number of 4 eggs. We should check these possibilities!
