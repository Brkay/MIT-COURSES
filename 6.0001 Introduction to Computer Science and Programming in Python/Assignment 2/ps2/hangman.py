# Problem Set 2, hangman.py
# Name: Berkay Yaldız
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
from asyncio import constants
from asyncore import loop
from distutils.command.sdist import sdist
import random
from re import S
import string


WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    ''' Second way to implement with only for loops.'''
    # for element in secret_word:
    # for letter in letters_guessed:
    # if element == letter:
    # break
    # if letter == letters_guessed[-1]:
    # return False

    # return True

    for element in secret_word:
        if element not in letters_guessed:
            return False

    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    # Second way to implement with only for loops.
    # for element in secret_word:
    # for letter in letters_guessed:
    # if element == letter:
    # returned_string += element
    # break

    # if letter == letters_guessed[-1]:
    # returned_string += "_ "

    # return returned_string

    returned_string = ""
    for element in secret_word:
        if element not in letters_guessed:
            returned_string += "_ "
        else:
            returned_string += element

    return returned_string


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = string.ascii_lowercase
    returned_string = ""
    for letter in all_letters:
        if letter not in letters_guessed:
            returned_string += letter
    return returned_string


def vovel_or_consonant(guess):
    vowels = ['a', 'e', 'i', 'o', 'u']
    if guess in vowels:
        return 1
    else:
        return 0


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    user_guesses = 6
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " +
          str(len(secret_word)) + " letters long.")
    print("-------------")

    letters_guessed = []
    warning_number = 3
    while(user_guesses):
        print("You have " + str(user_guesses) + " guesses left.")
        print("Available letters: " + get_available_letters(letters_guessed))
        guess = (input("Please guess a letter:")[0])
        if str.isalpha(guess):
            guess = str.lower(guess)
            if guess in letters_guessed:

                if warning_number > 0:
                    warning_number -= 1
                    print("Oops! You've already guessed that letter. You have " +
                          str(warning_number) + " warnings left!")
                    print(guessed_word_output)
                    print("-------------")
                    letters_guessed.append(guess)
                else:
                    print("You do not have any warnings, you lost a guess!")
                    print(guessed_word_output)
                    print("--------------")
                    user_guesses -= 1

            else:
                letters_guessed.append(guess)
                guessed_word_output = get_guessed_word(
                    secret_word, letters_guessed)

                if guess in secret_word:
                    print("Good guess: " + guessed_word_output)
                    print("--------------")
                else:
                    print("Oops! That letter is not in my word:" +
                          guessed_word_output)
                    print("-------------")
                    if vovel_or_consonant(guess):
                        user_guesses -= 2
                    else:
                        user_guesses -= 1

                if is_word_guessed(secret_word, letters_guessed):
                    print("Congratulations, you won!")
                    print("Your total score for this game is: " +
                          str(user_guesses * len(set(secret_word))))
                    return

        else:
            print("Please enter a valid input!")
            if warning_number > 0:
                warning_number -= 1
                print("You have " + str(warning_number) + " warnings left!")
                print(guessed_word_output)
                print("-------------")
            else:
                print("You do not have any warnings, you lost a guess!")

                print("--------------")
                user_guesses -= 1
    print("Sorry, you ran out of guesses. The word was " + secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    my_word = my_word.replace(" ", "")
    if len(my_word) != len(other_word):
        return False
    else:
        i = 0
        guessed_letters = ""
        for my_char in my_word:
            if my_char != '_':
                guessed_letters += my_char
        for my_char in my_word:
            if my_char != '_' and my_char != other_word[i]:
                return False
            elif my_char == '_':
                if other_word[i] in guessed_letters:
                    return False
            i += 1
        return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    return_flag = True
    for word in wordlist:
        if match_with_gaps(my_word, word):
            print(word + "   ", end="")
            return_flag = False

    if return_flag:
        print("No matches found")
    else:
        print("")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    user_guesses = 6
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " +
          str(len(secret_word)) + " letters long.")
    print("-------------")

    letters_guessed = []
    warning_number = 3
    guessed_word_output = ""
    while(user_guesses):
        print("You have " + str(user_guesses) + " guesses left.")
        print("Available letters: " + get_available_letters(letters_guessed))
        guess = (input("Please guess a letter:")[0])
        if guess == '*':
            show_possible_matches(guessed_word_output)
            continue

        if str.isalpha(guess):
            guess = str.lower(guess)
            if guess in letters_guessed:

                if warning_number > 0:
                    warning_number -= 1
                    print("Oops! You've already guessed that letter. You have " +
                          str(warning_number) + " warnings left!")
                    print(guessed_word_output)
                    print("-------------")
                    letters_guessed.append(guess)
                else:
                    print("You do not have any warnings, you lost a guess!")
                    print(guessed_word_output)
                    print("--------------")
                    user_guesses -= 1

            else:
                letters_guessed.append(guess)
                guessed_word_output = get_guessed_word(
                    secret_word, letters_guessed)

                if guess in secret_word:
                    print("Good guess: " + guessed_word_output)
                    print("--------------")
                else:
                    print("Oops! That letter is not in my word:" +
                          guessed_word_output)
                    print("-------------")
                    if vovel_or_consonant(guess):
                        user_guesses -= 2
                    else:
                        user_guesses -= 1

                if is_word_guessed(secret_word, letters_guessed):
                    print("Congratulations, you won!")
                    print("Your total score for this game is: " +
                          str(user_guesses * len(set(secret_word))))
                    return

        else:
            print("Please enter a valid input!")
            if warning_number > 0:
                warning_number -= 1
                print("You have " + str(warning_number) + " warnings left!")
                print(guessed_word_output)
                print("-------------")
            else:
                print("You do not have any warnings, you lost a guess!")

                print("--------------")
                user_guesses -= 1
    print("Sorry, you ran out of guesses. The word was " + secret_word)


    # When you've completed your hangman_with_hint function, comment the two similar
    # lines above that were used to run the hangman function, and then uncomment
    # these two lines and run this file to test!
    # Hint: You might want to pick your own secret_word while you're testing.
if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    # secret_word = 'else'
    # hangman(secret_word)
    # print(get_available_letters(letters_guessed))

    # secret_word = choose_word(wordlist)

    # hangman(secret_word)

   # hangman(secret_word)
    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.
    #secret_word = "blurs"
    secret_word = "apple"
    hangman_with_hints(secret_word)
    # secret_word = choose_word(wordlist)
    # hangman_with_hints(secret_word)
