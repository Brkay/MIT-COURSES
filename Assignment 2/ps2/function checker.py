# function checker
import string


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
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
    # returned_string = ""
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


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    secret_word = 'tact'
    letters_guessed = ['t', 'e']
    returned_string = get_guessed_word(secret_word, letters_guessed)
    print(show_poss("a_ ple", "apple"))
