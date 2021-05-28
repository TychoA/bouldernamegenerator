#!/usr/bin/env python3
from bs4 import BeautifulSoup
import sys
from os import path
import re
import csv
from collections import defaultdict

def get_definitions():

    if getattr(sys, 'frozen', False):
        inputfile = path.join(sys._MEIPASS, 'definitions.tsv')
    else:
        inputfile = 'definitions.tsv'

    # check if the file exists
    if not path.isfile(inputfile):
        return {}

    # read the file and expose the collection
    with open(inputfile, 'r') as tsvfile:
        return {row['term']: row['definition'] for row in csv.DictReader(tsvfile, dialect='excel-tab')}

def _create_definitions():

    # collection of definitions per term
    definitions = defaultdict(list)

    # open the bouldering terms file
    with open("sources/terms.html") as f:

        # write all definitions to the file
        matches = re.findall(r'\<strong\>([\w\s]+)\<\/strong\>([\w\s\.\/\(\)\-\"\,\“\”]+)\<', f.read(), re.MULTILINE)

        # skip if we didn't find matches
        if matches == None:
            pass

        # iterate over the matches
        for (term, dfn) in matches:

            # and add the definition to the term
            definitions[term.lower().strip()].append(dfn)

    # open the wiki terms file
    with open("sources/wiki_terms.html") as f:

        # the latest found term
        latest_dfn = ''

        # iterate over all the terms and definitions
        for tag in BeautifulSoup(f.read(), 'html.parser').find_all(['dfn', 'dd']):

            # add a new term
            if tag.name == 'dfn':
                latest_dfn = tag.get_text().lower().strip()

            # add a definition to the term
            if tag.name == 'dd':
                definitions[latest_dfn].append(tag.get_text())

    # expose the definitions
    return definitions

if __name__ == "__main__":

    output_file = 'definitions.tsv'
    result = _create_definitions()

    # clear the file before writing to it
    if path.isfile(output_file):
        open(output_file, 'w').write('')

    # open the file for appending the definitions
    with open(output_file, 'a') as csv:

        # write the columns
        csv.write('term\tdefinition\n')

        # and all the data
        for key in result.keys():
            value = ''.join(result[key]).strip()
            csv.write(f'{key}\t{value}\n')
