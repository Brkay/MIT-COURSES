
import math
import random
import string

from numpy import number

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))
    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    values = list(hand.values())
    if values.count(1) is not 0:
        index_with_1 = values.index(1)
        hand.pop(list(hand)[index_with_1])
        hand['*'] = 1
    else:
        hand[list(hand)[0]] -= 1
        hand['*'] = 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

        The score for a word is the product of two components:

        The first component is the sum of the points for letters in the word.
        The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

        Letters are scored as in Scrabble; A is worth 1, B is
        worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    if word == "":
        return 0

    lowercase_word = word.lower()
    print(lowercase_word)
    points1 = 0
    word_length = len(word)
    for i in range(word_length):
        points1 += SCRABBLE_LETTER_VALUES[lowercase_word[i]]

    points2 = 7*word_length-3*(n-word_length)
    if points2 < 1:
        points2 = 1
    return (points1*points2)


if __name__ == '__main__':
    get_word_score()
