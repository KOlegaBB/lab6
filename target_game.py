"""
Target game is a game, where you should create words from letters in grid. Also
you must use the middle letter. This program generates grid, checks which words
in the dictionary fits the rules, receives words from player, checks if users
words are in the dictionary or if not adds it to the list of new words and
creates results.
"""
import sys
from typing import List
import random


def generate_grid() -> List[List[str]]:
    """
    Generates list of lists of letters - i.e. grid for the game.
    e.g. [['I', 'G', 'E'], ['P', 'I', 'S'], ['W', 'M', 'G']]
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    grid = []
    for _ in range(3):
        block = []
        for _ in range(3):
            block.append(random.choice(alphabet))
        grid.append(block)
    return grid


def get_words(file_f: str, letters: List[str]) -> List[str]:
    """
    Reads the file f. Checks the words with rules and returns a list of words.

    >>> print(get_words("en", ["a", "b", "y", "c", "j", "k", "l", "m",\
    "a"]))
    ['jacal', 'jack', 'jackal', 'jacky', 'jama', 'jamb', 'maja']
    """
    long_words = []
    with open(file_f) as file:
        content = file.read()
    content = content.split("\n")
    content = content[3:]
    for word in content:
        word = word.lower()
        if len(word) >= 4:
            long_words.append(word)
    iterator = 0
    letter_number = []
    middle_letter = letters[4]
    while iterator < len(letters):
        iterator_2 = iterator + 1
        number_of_letters = 1
        while iterator_2 < len(letters):
            if letters[iterator] == letters[iterator_2]:
                number_of_letters += 1
                letters = letters[:iterator_2] + letters[iterator_2 + 1:]
            else:
                iterator_2 += 1
        letter_number.append((letters[iterator], number_of_letters))
        iterator += 1
    semicorrect_words = []
    for word in long_words:
        letter_words_number = []
        iterator = 0
        while iterator < len(word):
            iterator_2 = iterator + 1
            number_of_letters = 1
            changed_word = word
            while iterator_2 < len(changed_word):
                if changed_word[iterator] == changed_word[iterator_2]:
                    number_of_letters += 1
                    changed_word = changed_word[:iterator_2] + \
                                   changed_word[iterator_2 + 1:]
                else:
                    iterator_2 += 1
            letter_words_number.append((changed_word[iterator],
                                        number_of_letters))
            iterator += 1
        word_check = True
        for tuples in letter_words_number:
            letter_check = False
            for tuples_2 in letter_number:
                if tuples[0] == tuples_2[0] and tuples[1] <= tuples_2[1]:
                    letter_check = True
                    break
            if not letter_check:
                word_check = False
                break
        if word_check:
            semicorrect_words.append(word)
    correct_words = []
    for word in semicorrect_words:
        if middle_letter in word:
            correct_words.append(word)
    return correct_words


def get_user_words() -> List[str]:
    """
    Gets words from user input and returns a list with these words.
    Usage: enter a word or press ctrl+d to finish.
    """
    user_list = []
    for user_word in sys.stdin:
        user_list.append(user_word)
    return user_list


def get_pure_user_words(user_words: List[str], letters: List[str],
                        words_from_dict: List[str]) -> List[str]:
    """
    (list, list, list) -> list

    Checks user words with the rules and returns list of those words
    that are not in dictionary.

    >>> print(get_pure_user_words(["klymja", "jaba", "jbl", "jack", "lala"], \
["a", "b", "y", "c", "j", "k", "l", "m", "a"], \
['jacal', 'jack', 'jackal', 'jama', 'jamb']))
    ['klymja', 'jaba']
    """
    new_words = []
    middle_letter = letters[4]
    iterator = 0
    letter_number = []
    while iterator < len(letters):
        iterator_2 = iterator + 1
        number_of_letters = 1
        while iterator_2 < len(letters):
            if letters[iterator] == letters[iterator_2]:
                number_of_letters += 1
                letters = letters[:iterator_2] + letters[iterator_2 + 1:]
            else:
                iterator_2 += 1
        letter_number.append((letters[iterator], number_of_letters))
        iterator += 1
    for word in user_words:
        if len(word) >= 4:
            letter_words_number = []
            iterator = 0
            while iterator < len(word):
                iterator_2 = iterator + 1
                number_of_letters = 1
                changed_word = word
                while iterator_2 < len(changed_word):
                    if changed_word[iterator] == changed_word[iterator_2]:
                        number_of_letters += 1
                        changed_word = changed_word[:iterator_2] + \
                                       changed_word[iterator_2 + 1:]
                    else:
                        iterator_2 += 1
                letter_words_number.append((changed_word[iterator],
                                            number_of_letters))
                iterator += 1
            word_check = True
            for tuples in letter_words_number:
                letter_check = False
                for tuples_2 in letter_number:
                    if tuples[0] == tuples_2[0] \
                            and tuples[1] <= tuples_2[1]:
                        letter_check = True
                        break
                if not letter_check:
                    word_check = False
                    break
            if word_check:
                if middle_letter in word:
                    being_in_dict = False
                    for word_dict in words_from_dict:
                        being_in_dict = False
                        if word == word_dict:
                            being_in_dict = True
                            break
                    if not being_in_dict:
                        new_words.append(word)
    return new_words


def results(correct_words_count, all_words, missed_words, new_words):
    """
    Creates result of the game
    :return:

    >>> results(3, ['jacal', 'jack', 'jackal', 'jama', 'jamb'], \
['jama', 'jamb'], ['klymja', 'jaba'])
    Правильні відповіді: 3
    Всі слова: ['jacal', 'jack', 'jackal', 'jama', 'jamb']
    Пропущені слова: ['jama', 'jamb']
    Нові слова: ['klymja', 'jaba']
    """
    file = "result.txt"
    text = "Правильні відповіді: " + str(correct_words_count) + "\n" \
           + "Всі слова: " + str(all_words) + "\n" + "Пропущені слова: " + \
           str(missed_words) + "\n" + "Нові слова: " + str(new_words)
    with open(file, 'w') as output_file:
        output_file.write(text)
    print(text)
