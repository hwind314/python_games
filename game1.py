import string
import random

from english_words import get_english_words_set
import random

dictionary = get_english_words_set(['web2'], lower=True)

print("Welcome to Spelling Bee!")
print("You must make as many words as possible, but they must contain the centre letter at least once")
print("Enter '*' for help")


# function to generate letters for game
def generate_letters(n):
    letters = random.sample(string.ascii_lowercase, k=n)
    centre = random.choice(letters)
    outer = [let for let in letters if let != centre]

    return letters, centre, outer


# how many letters?
while True:
    num_letters = input("How many letters would you like? ")

    # Check if input is a valid number
    if not num_letters.isdigit():
        print("Invalid input. Please enter a number.")
        continue

    # Convert to integer
    num_letters = int(num_letters)

    # Check if within valid range
    if num_letters < 1 or num_letters > 26:
        print("Invalid input. Please enter a number between 1 and 26.")
    else:
        int(num_letters)
        break

answer_key = []

# get letters
while True:
    game_letters, centre_letter, outside_letters = generate_letters(num_letters)

    for word in dictionary:
        letter_count = 0
        centre_letter_count = 0
        for letter in word:
            if letter in game_letters:
                letter_count += 1
                if letter == centre_letter:
                    centre_letter_count += 1

        if letter_count == len(word):
            if len(word) > 2:
                if centre_letter_count > 0:
                    answer_key.append(word)

    if len(answer_key) > 20:
        break

print("Centre letter: " + centre_letter)
print("Other letters: " + str(outside_letters))

answer_found = []

# start game
while len(answer_found) != len(answer_key):
    attempt = input("Enter your word: ")

    # check if user needs help
    if attempt == "*":
        print("""
        Hints:
        1. Give me the first letter
        2. Give me the word length
        3. Show me the answer board
        4. Reveal one answer
        5. Never-mind, I want to solve it on my one
        """)
        user_help = input("Please choose: ")
        possible_help = ["1", "2", "3", "4", "5"]

        while user_help not in possible_help:
            user_help = input("Invalid input. Please try again: ")

        hint = random.choice([item for item in answer_key if item not in answer_found])

        if user_help == "1":
            print("First letter is: " + hint[0])
        elif user_help == "2":
            print("Word length is: " + str(len(hint)))
        elif user_help == "3":
            print("Words found: " + str(answer_found))
            hidden_answers = [
                ''.join('_' if letter.isalpha() else letter for letter in answer)
                if answer not in answer_found else answer
                for answer in answer_key
            ]
            print("Words not yet found: " + str(hidden_answers))
        elif user_help == "4":
            print("Word: " + hint)
        else:
            print("You can do it!")
            continue

    # check user input
    else:
        # check letters
        centre_letter_count = 0
        # check letters
        for letter in attempt:
            if letter not in game_letters:
                print("Invalid letter used")
                break
            if letter == centre_letter:
                centre_letter_count += 1
        else:
            # check word
            if len(attempt) < 3:
                print("Word too short")
                continue
            elif centre_letter_count == 0:
                print("Centre letter not used")
                continue
            else:
                if attempt not in answer_key:
                    print("Invalid word")
                    continue
                else:
                    print("Word found!")
                    answer_found.append(attempt)

print("You've found all the words!")
