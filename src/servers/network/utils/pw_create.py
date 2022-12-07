import secrets

LOW_LETTERS = [chr(l+97) for l in range(26)]
CAP_LETTERS = [chr(l+65) for l in range(26)]
NUMBERS = [str(i) for i in range(10)]
SYMBOLS = ['#', '@', '$', '+', '%', '&', '=', '?']


def create(length, low_letters, cap_letters, numbers, symbols):
    possible_chars = []
    if low_letters:
        possible_chars = [*possible_chars, *LOW_LETTERS]
    if cap_letters:
        possible_chars = [*possible_chars, *CAP_LETTERS]
    if numbers:
        possible_chars = [*possible_chars, *NUMBERS]
    if symbols:
        possible_chars = [*possible_chars, *SYMBOLS]
    
    password = ''
    for _ in range(length):
        password += secrets.choice(possible_chars)
    
    return password