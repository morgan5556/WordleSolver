"""
This is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. It is
distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
the code.  If not, see <http://www.gnu.org/licenses/>.

File name: 	main.py
Created:	9th February 2022
Author:	Morgan Lyons

Contact: morgan@morganlyons.xyz
Web: www.morganlyons.xyz

This is an algoritm that attempts to solve a game of Wordle.
"""

from collections import Counter
from english_words import english_words_lower_alpha_set

class WordleSolver:
    def __init__(self):
        """
        This function is run when this file is executed, it creates empty sets
        and lists for the program to run. It then runs the menu.
        """

        self.__all_words = []
        self.__blank_letters = set()
        self.__known_letters = set()
        self.__invalid_words = set()
        self.__common_value = 1
        self.__total_guesses = 0
        self.__total_words = 0
        self.__menu_option()
        
    def __menu_option(self):
        """
        This function is the menu. It asks the user whether they want to run the 
        WordleSolver for a single word or to simulate all the words in the list of
        words.
        """

        print("-" * 30)
        print("1. Run WordleSolver \n2. Simulate all Words")
        user_input = input("Enter Option: ")

        match user_input:
            case '1':
                self.__run_program_loop()
            case '2':
                self.__simulate_all_words()

    def __run_program_loop(self):
        """
        This runs the program loop for the WordleSolver solving a single word.
        It contains a for loop to limit it to 6 guesses and then resets when
        the guesses have all been completed.
        """

        print("-" * 30)
        self.__add_to_word_set()
        
        for turn in range(1, 7):
            word = self.__find_best_word()
            
            print(f"Guess {turn}: {word.upper()}")
            outcome = input("Enter Outcome: ")

            if outcome == "GGGGG":
                print(f"The word was {word.upper()} which was solved in {turn} guess(es)")
                break
            self.__analyse_outcome(outcome, word)

        self.__reset_wordle()
        self.__run_program_loop()

    def __simulate_all_words(self):
        """
        This function simulates all words to see if the WordleSolver can solve
        them. For each word, the computer has 10 guesses - this is to find any
        words that take more than 6 attempts. This is all logged in results.txt.
        """

        print("-" * 30)
        print("This process has been started, it may take a couple of minutes . . . ")

        self.__add_to_word_set()
        word_list_copy = self.__all_words

        for answer in word_list_copy:
            self.__total_words = self.__total_words + 1
            guess_list = []
            for turn in range(1, 11):
                self.__total_guesses = self.__total_guesses + 1
                word = self.__find_best_word()

                guess_list.append(word)
                outcome = self.__determine_outcome(answer, word)

                if outcome == "GGGGG":
                    with open('results.txt', 'a') as file:
                        file.write(f"The word was {word.upper()} which was solved in {turn} guess(es)\n{guess_list}\n")
                    break

                self.__analyse_outcome(outcome, word)
            
            self.__reset_wordle()
        
        self.__calculate_average()
        print("This process has been completed. The results can be viewed in the results.txt file.")

    def __determine_outcome(self, answer, word):
        """
        This function determines the outcome of the guess compared to
        the answer when the simulate all words function is run.

        @param answer: the answer for the Wordle.
        @param word: the guessed word by the computer.
        @return: the outcome of the guess.
        """

        outcome_list = []
        
        for index in range(0, 5):
            if answer[index] == word[index]:
                outcome_list.append("G")
            elif word[index] not in answer:
                outcome_list.append("B")
            else:
                outcome_list.append("Y")

        return ''.join(outcome_list)

    def __add_to_word_set(self):
        """
        This function adds all the 5 letter words from the english
        words set to the all words list.
        """

        for word in english_words_lower_alpha_set:
            if len(word) == 5:
                self.__all_words.append(word)

    def __find_most_common_letter(self, index):
        """
        This finds the most common letter in the list of all available
        words at a certain index.
        
        @param index: the index value to check at.
        @return: the letter most common, depending on the common value.
        """

        set_of_letters = []

        for word in self.__all_words:
            set_of_letters.append(word[index])

        freq_counter = Counter(set_of_letters)
        
        return freq_counter.most_common(self.__common_value)[self.__common_value - 1][0]

    def __find_best_word(self):
        """
        This attempts to find a good word to use as a guess based on letter
        frequency in the available words. It adjusts the common value if the 
        most common letter cannot be used.
        
        @return: a suitable guessing word.
        """

        best_word = []

        for index in range(0, 5):
            self.__common_value = 1
            while True:
                best_word.append(self.__find_most_common_letter(index))
                potential_bool = self.__check_for_potential_word(''.join(best_word))
                
                if potential_bool == True:
                    break
                else:
                    self.__common_value = self.__common_value + 1
                    best_word.pop()
 
        return ''.join(best_word)

    def __check_for_potential_word(self, word_string):
        """
        This checks if a word exists in the word list that starts with the
        word_string. False is returned if a word does not exist, and
        frequency analysis is computed to find the next most common letter.

        @param word_string: the string of letters to check by.
        @return: True or False depending on if a word exists.
        """
        for word in self.__all_words:
            if word.startswith(word_string):
                return True

        return False

    def __analyse_outcome(self, outcome, guess):
        """
        This analyses the outcome the user has entered. It goes through
        each outcome value and adds the letter to a set depending on the 
        outcome and runs a subroutine if the outcome is G or Y.

        @param outcome: the outcome of the guess.
        @param guess: the guess from the computer.
        """

        for index in range(0, 5):
            if outcome[index] == "B":
                self.__blank_letters.add(guess[index])
            elif outcome[index] == "G":
                self.__known_letters.add(guess[index])
                self.__green_letters(guess[index], index)
            elif outcome[index] == "Y":
                self.__known_letters.add(guess[index])
                self.__yellow_letters(guess[index], index)
        self.__remove_words()

    def __green_letters(self, letter, position):
        """
        This deals with outcomes that return with "G". It goes through 
        the word list, and adds words to the invalid word set that do
        not contain that letter in that certain index.

        @param letter: the letter that has turned green.
        @param position: the position of the green letter.
        """

        self.__duplicate_letters()
        for word in self.__all_words:
            if word[position] != letter:
                self.__invalid_words.add(word)

    def __yellow_letters(self, letter, position):
        """
        This deals with outcomes that return with "Y". It goes through 
        the word list, and adds words to the invalid word set that do
        contain that letter in that certain index.

        @param letter: the letter that has turned yellow.
        @param position: the position of the yellow letter.
        """
        
        self.__duplicate_letters()
        for word in self.__all_words:
            if word[position] == letter or letter not in word:
                self.__invalid_words.add(word)

    def __remove_words(self):
        """
        This removes all the words that contain blank letters. It also
        uses set comprehension to remove all the words in the invalid
        words set from the list of all words.
        """

        self.__duplicate_letters()
        for word in self.__all_words:
            for letter in self.__blank_letters:
                if letter in word:
                    self.__invalid_words.add(word)
                    break

        self.__all_words = set(self.__all_words) - self.__invalid_words

    def __duplicate_letters(self):
        """
        This deals with duplicate letters that are in both the blank letter
        set and the known letter set.
        """
        
        self.__blank_letters = self.__blank_letters - self.__known_letters

    def __calculate_average(self):
        """
        This calculates the average guess when simulating all words.
        """

        average = self.__total_guesses / self.__total_words
        print("The average is: " + str(average))

    def __reset_wordle(self):
        """
        This resets the WordleSolver to its original state with all the
        variables at their starting values.
        """

        self.__all_words = []
        self.__blank_letters.clear()
        self.__known_letters.clear()
        self.__invalid_words.clear()
        self.__common_value = 1
        self.__add_to_word_set()

if __name__ == '__main__':
    WordleSolver() # Runs the WordleSolver