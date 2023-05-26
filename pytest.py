from Converters import *
from pyperclip import copy

if __name__ == '__main__':
    df = htmltodf('https://en.wikipedia.org/wiki/Indigenous_languages_of_the_Americas')
    print(dftojson(df))