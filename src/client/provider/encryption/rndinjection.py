import math
import os

# This module is used to obscure constant strings.
# Else the encrypted constant string would be a huge security vulnerability


def encrypt(string: str):
    encrypted = ''
    for char in string:
        encrypted += char + chr(ord(os.urandom(1)))
    return encrypted


def decrypt(string: str):
    decrypted = ''
    for x in range(math.floor(len(string) / 2)):
        decrypted += str(string[x * 2])
    return decrypted
