#!/usr/bin/env python3
from os import path
from random import uniform
from math import floor
import sys

def get_term(name):

    # the file that holds the terms
    if getattr(sys, 'frozen', False):
        input_file = path.join(sys._MEIPASS, 'terms.txt')
    else:
        input_file = 'terms.txt'

    # we need it
    if not path.isfile(input_file):
        raise Exception("terms.txt file not found")

    # open the terms file
    with open(input_file) as f:
        
        # collect all terms
        terms = f.read().split('\n')

        # ask for some input
        name = name.strip().lower()

        # get the first letter of the name
        first_letter = name[0]

        # find all terms that start with that letter
        matches = [term for term in terms if len(term) and term[0] == first_letter]

        # now, get a random match
        index = floor(uniform(0, len(matches)))
        match = matches[index]

        # output the random name
        return match

if __name__ == "__main__":
    name = input("Please enter a name: ")
    print("Your name: " + get_term(name) + " " + name)
