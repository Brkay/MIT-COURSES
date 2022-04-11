###########################
# 6.0002 Problem Set 1a: Space Cows
# Name: Berkay Yaldız
# Collaborators:
# Time:

from tabnanny import check
from ps1_partition import get_partitions
import time

# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1


def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    inFile = open(filename, 'r')
    cow_weight_pair = {}
    for line in inFile:
        temp_list = line.split(',')
        cow_weight_pair[temp_list[0]] = int(temp_list[1])
    return cow_weight_pair

# Problem 2


""" def sublist(sub_list, test_list):
    checker = len(test_list)
    if sub_list[-checker:] == test_list:
        return True
    return False
 """


# def greedy_cow_first_trip(cows, limit=10):
"""
All possibilities for first trip:

Does not mutate the given dictionary of cows.

Parameters:
cows - a dictionary of name (string), weight (int) pairs
limit - weight limit of the spaceship (an int)

Returns:
A list of lists, with each inner list containing the names of cows
of possible first round trips.
"""
"""sorted_cows = sorted(cows, key=cows.get, reverse=True)
trip_lists = []
max_index2_length = len(sorted_cows)
for keys in sorted_cows:
    total_value = cows[keys]
    if cows[keys] > limit:
        continue
    if total_value + cows[sorted_cows[-1]] > limit:
        trip_lists.append([keys])
        continue
    temp_list = [keys]
    index1 = sorted_cows.index(keys)
    for index2 in range(index1+1, max_index2_length):
        if total_value + cows[sorted_cows[index2]] < limit:
            temp_list.append(sorted_cows[index2])
            total_value += cows[sorted_cows[index2]]
    if trip_lists != []:
        if not sublist(trip_lists[-1], temp_list):
            trip_lists.append(temp_list)
    else:
        trip_lists.append(temp_list)

return trip_lists
"""


def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    sorted_cows = sorted(cows, key=cows.get, reverse=True)
    trip_list = []
    while sorted_cows != []:
        total_value = 0
        temp_list = []
        for keys in sorted_cows:
            if cows[keys] >= limit:
                sorted_cows.remove(keys)
            if total_value + cows[keys] < limit:
                temp_list.append(keys)
                total_value += cows[keys]
        if temp_list != []:
            trip_list.append(temp_list)
        for elem in temp_list:
            sorted_cows.remove(elem)
    return trip_list


# Problem 3


def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    smallest_trip = list(cows.keys())
    copied_dict = cows.copy()
    for keys in smallest_trip:
        if limit <= cows[keys]:
            del copied_dict[keys]

    for partition in get_partitions(copied_dict.keys()):
        for elem in partition:
            total = 0
            flag = False
            for cow_keys in elem:
                total += copied_dict[cow_keys]
                if total >= limit:
                    flag = True
                    break
            if flag:
                break
            elif not flag and elem is partition[-1] and len(smallest_trip) > len(partition):
                smallest_trip = partition
    return smallest_trip


# Problem 4

def compare_cow_transport_algorithms(cows):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    start = time.perf_counter()
    greedy_cow_transport(cows)
    end = time.perf_counter()
    print("Elapsed time for greedy algorithm:" + str(end-start))
    start = time.perf_counter()
    brute_force_cow_transport(cows)
    end = time.perf_counter()
    print("Elapsed time for brute-force algorithm:" + str(end-start))


if __name__ == "__main__":
    cows = {"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5}
    result_greedy = greedy_cow_transport(cows)
    result_brute = brute_force_cow_transport(cows)
    print("Result of the greedy algorithm for the example in assignment:")
    print(result_greedy)
    print("Result of the brute force algorithm for the example in assignment:")
    print(result_brute)
    print("\n")
    print("Compare the algorithms for this set:")
    compare_cow_transport_algorithms(cows)

    filename = "ps1_cow_data.txt"
    cows = load_cows(filename)
    result_greedy = greedy_cow_transport(cows)
    result_brute = brute_force_cow_transport(cows)
    print()
    print("Result of the greedy algorithm for first dataset:")
    print(result_greedy)
    print("Result of the brute force algorithm for first dataset:")
    print(result_brute)
    print()
    print("Compare the algorithms for this set:")
    compare_cow_transport_algorithms(cows)

    filename = "ps1_cow_data_2.txt"
    cows = load_cows(filename)
    result_greedy = greedy_cow_transport(cows)
    result_brute = brute_force_cow_transport(cows)
    print()
    print("Result of the greedy algorithm for second dataset:")
    print(result_greedy)
    print("Result of the brute force algorithm for second dataset:")
    print(result_brute)
    print()
    print("Compare the algorithms for this set:")
    compare_cow_transport_algorithms(cows)
    # Problem A.5
    # QUESTION - 1
    # As we can see greedy algorithm runs much faster than the brute force algorithm.
    # This is because the fact that brute force algorithm checks all possibilities.
    # QUESTION - 2 and 3
    # From the results, we can see that for these 3 datasets greedy and brute force algorithms return
    # the same number of trips. Hence, greedy algorithm returns the optimal solution for the number of trips
    # because brute force algorithm always returns the optimal solution by checking the all posibilities.
