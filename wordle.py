import re
import os
import requests
from typing import List
from colorama import init, Fore, Style

WORD_LEN = 5
WORD_FREQUENCY = 7.0
WORD_PATTERN = r'^[a-zA-Z]+$'
NUM_TRIES = 6

WORDS_API_URI = 'https://wordsapiv1.p.rapidapi.com/words/'
WORDS_API_KEY_ENV_VAR = 'WORDS_API_API_KEY'
WORDS_API_HTTP_HEADERS = {
    'x-rapidapi-host': 'wordsapiv1.p.rapidapi.com',
    'x-rapidapi-key': os.environ.get(WORDS_API_KEY_ENV_VAR)
}


def get_word() -> str:
    querystring = {
        'letterPattern': WORD_PATTERN,
        'letters': WORD_LEN,
        'frequencymin': WORD_FREQUENCY,
        'random': 'true',
    }

    response = requests.request(
        'GET',
        WORDS_API_URI,
        headers=WORDS_API_HTTP_HEADERS,
        params=querystring
    )

    if response.status_code >= 400:
        print(f'Failure making request to WordsAPI: {response.json()}\nIs your API key set correctly?')
        exit(1)

    return response.json()['word'].lower()


def does_word_exist(word: str) -> bool:
    if not re.match(WORD_PATTERN, word):
        return False

    response = requests.request(
        "GET", 
        WORDS_API_URI + word,
        headers=WORDS_API_HTTP_HEADERS
    )

    return response.status_code < 300


def get_guess(tries: int) -> str:
    guess = None
    prefix = ''
    num_style = Style.NORMAL

    while True:
        guess = input(f'{prefix}Guess the {num_style}5{Style.NORMAL} letter word ({tries} tries left) ')
        prefix = ''
        num_style = Style.NORMAL

        if len(guess) != WORD_LEN:
            num_style = Style.BRIGHT
            continue

        if not does_word_exist(guess):
            prefix = 'That\'s not a real word\n'
            continue

        break

    return guess.lower()


def get_guess_colors(guess: str, word: str) -> List[str]:
    colors = [None] * WORD_LEN

    for i, (guess_ch, word_ch) in enumerate(zip(guess, word)):
        if guess_ch == word_ch:
            colors[i] = 'green'
        elif guess_ch in word:
            colors[i] = 'yellow'
        else:
            colors[i] = 'black'

    return colors


def print_guess_colors(guess: str, colors: List[str]):
    for ch, color in zip(guess, colors):
        if color == 'green':
            term_color = Fore.GREEN
        elif color == 'yellow':
            term_color = Fore.YELLOW
        else:
            term_color = Fore.RESET

        print(term_color + ch + Style.RESET_ALL, end='')

    print()


def main():
    init()

    tries: int = NUM_TRIES
    word: str = get_word()
    guess: str = None

    while tries > 0:
        guess = get_guess(tries)
        if guess == word:
            print(f'Success! The word was "{word}"')
            exit(0)

        if tries > 1:
            colors = get_guess_colors(guess, word)
            print_guess_colors(guess, colors)
            tries -= 1
        else:
            print(f'Out of tries! The word was "{word}". You suck')
            exit(0)


if __name__ == '__main__':
    main()
    exit(0)
