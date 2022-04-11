# Problem Set 4A
# Name: Berkay Yaldız
# Collaborators:
# Time Spent: x:xx

from itertools import permutations
from tokenize import String
from numpy import concatenate


def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    if len(sequence) == 1:
        return [sequence]
    else:
        res = []
        for elt in sequence:
            permutations = get_permutations(sequence.replace(elt, ""))
            for permutation in permutations:
                res.append(elt + permutation)
        return res


"""
        returned_list = concatenated_string.split(' ')
        for index2 in range(len(returned_list)):
            returned_list[index2] = letter + returned_list[index2] """


if __name__ == '__main__':
    #    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    example_input = 'but'
    print('Input:', example_input)
    print('Expected Output:', ['but', 'btu', 'utb', 'ubt', 'tub', 'tbu'])
    print('Actual Output:', get_permutations(example_input))
    example_input = 'bust'
    print('Input:', example_input)

    print('Actual Output:', get_permutations(example_input))
