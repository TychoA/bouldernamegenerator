#!/usr/bin/env python3
from bs4 import BeautifulSoup
from os import path
import re

def get_definitions():

    # collection of definitions per term
    definitions = {}

    # open the bouldering terms file
    with open("sources/terms.html") as f:

        # create a soup so we can parse it
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

        # expressions to find terms and definitions
        term_re = r'\<strong\>([\w\s]+)\<\/strong\>'
        dfn_re = r'\<\/strong\>([\w\s\.]+)\<br\>'
        both_re = r'\<strong\>([\w\s]+)\<\/strong\>([\w\s\.\/]+)\<'

        # write all definitions to the file
        matches = re.findall(both_re, contents, re.MULTILINE)

        # skip if we didn't find matches
        if matches == None:
            pass

        # iterate over the matches
        for (term, dfn) in matches:
            term = term.lower()
            if term not in definitions:
                definitions[term] = []

            # and add the definition to the term
            definitions[term].append(dfn)

    # open the wiki terms file
    with open("sources/wiki_terms.html") as f:

        # create a soup so we can parse it
        soup = BeautifulSoup(f.read(), 'html.parser')

        # the latest found term
        latest_dfn = ''

        # iterate over all the terms and definitions
        for tag in soup.find_all(['dfn', 'dd']):

            # add a new term
            if tag.name == 'dfn':
                latest_dfn = tag.get_text().lower().strip()
                definitions[latest_dfn] = []

            # add a definition to the term
            if tag.name == 'dd':
                definitions[latest_dfn].append(tag.get_text())

    # expose the definitions
    return definitions

if __name__ == "__main__":
    result = get_definitions()
    print(result)
