# Wordle (But Worse)
It's Wordle but on the command line. If you want to have fun, visit the real [Wordle](https://www.nytimes.com/games/wordle).

## Usage
To use, install all requirements with pip:
```
pip install -r requirements.txt
```
Subscribe to the [WordsAPI](https://www.wordsapi.com/) (use the free plan) and receive an application key (a 50 character alphanumeric subscriber ID). Export this key into the environment variable `WORDS_API_API_KEY`:
```
export WORDS_API_API_KEY="abcdefghijklmnopqrstuvwxyz0123456789zyxwvutxrqponm"
```
Run the script: 
```
python3 wordle.py
```