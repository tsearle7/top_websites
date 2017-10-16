# Checking the language of HTML text

import json
import sys
import re
import unicodedata
from bs4 import BeautifulSoup
from collections import Counter

translation_table = dict.fromkeys(map(ord, '[]()123456789'), None)

if __name__ == "__main__":

    input_file = open('sample1000.json', encoding=('utf-8'))
    error_count = 0
    worked = 0
    language_dict = []
    mode_list = []

    for raw_line in input_file:

        line = raw_line

        try:
            # Load JSON and specify branch
            data_dict = json.loads(line)
            html = data_dict["p80"]["http"]["get"]["body"]
            # Begin cleanup of HTML
            souped = BeautifulSoup(html, 'html.parser')
            htmltext = souped.get_text()
            #print(htmltext)
            characters = list(htmltext)
            #print(characters)
            for character in characters:
                try:
                    data = unicodedata.name(character)
                except:
                    continue
                data_split = data.split()
                language = data_split[0]
                language_dict.append(language)

            mode_finder = Counter(language_dict)
            mode = mode_finder.most_common(1)
            mode = mode.translate(translation_table)
            mode_list.append(mode)
            language_dict = []


        except Exception as error_desc:
            error_count += 1
    with open('language_data.csv', 'w') as file_handler:
        for item in mode_list:
            file_handler.write("{}\n".format(item))
    print(len(mode_list))

    print(error_count)