# web_reader.py a program to read Censys data.

import json
import sys
import re
from bs4 import BeautifulSoup

# Functions to replace text in very simple ways. The second is needed for cases
# where we want to preserve a quote (otherwise we risk breaking the json
# format).
def replace_with_blank(match):
    return " "

def replace_with_quote(match):
    return '\\"'

def stripTags(text):
    scripts = re.compile(r'<script.*?/script>')
    css = re.compile(r'<style.*?/style>')
    tags = re.compile(r'<.*?>')

    text = scripts.sub('', text)
    text = css.sub('', text)
    text = tags.sub('', text)

    return text



translation_table = dict.fromkeys(map(ord, '\n'), None)

# Regular expressions to match the problematic patterns in our text 
multichar = re.compile(r'\\u[0-9A-Za-z]{3,6}')
escape_and_quote = re.compile(r'\\h"')
escape = re.compile(r'\\[ h]')

# This function takes as input:
#   text - a string
#   replace_function - a function that will determine a suitable replacement
#   regular_expression - the pattern that will identify what is replaced
def repair(text, replace_function, regular_expression):
    return regular_expression.sub(replace_function, text)

if __name__ == "__main__":
    # A couple of values that control whether detailed error information is
    # logged
    LOG_ERRORS = False
    MAX_ERRORS_LOGGED = 1

    input_file = open('sample1000.json', encoding=('utf-8'))
    output_file = open('web_data.txt', 'w')
    training_categories = open('web_categories.txt', 'w')
    translation_table = dict.fromkeys(map(ord, '\n'), None)

    error_count = 0
    worked = 0
    for raw_line in input_file:

        line = raw_line
        # A series of modifications to the line, each making one type of
        # # change.
        line = repair(line, replace_with_quote, escape_and_quote)
        line = repair(line, replace_with_blank, multichar)
        line = repair(line, replace_with_blank, escape)
        line = repair(line, replace_with_blank, escape)
        line = stripTags(line)

        try:
            # Load JSON and specify branch
            data_dict = json.loads(line)
            html = data_dict["p80"]["http"]["get"]["body"]
            # Begin cleanup of HTML
            souped = BeautifulSoup(html, 'html.parser')
            htmltext = souped.get_text()
            lines = (line.strip() for line in htmltext.splitlines())
            results = '\n'.join(chunk for chunk in lines if lines)
            results = results.translate(translation_table)
            # Output to text file
            output_file.write("Domain: ")
            output_file.write(data_dict["domain"])
            output_file.write(" : ")
            output_file.write(results)
            output_file.write('\n')
            training_categories.write("Domain: "+ data_dict["domain"]+' | '+'\n')
            worked += 1
        except Exception as error_desc:
            error_count += 1

            if LOG_ERRORS:
                # Print the problematic line
                print(raw_line)
                print(line)

                # Print the details
                print(str(error_desc))

                # If it is an error that specifies a position, print 10 characters
                # either side of that position.
                error = str(error_desc)
                if "column" in error:
                    position = int(error.split('column')[1].strip().split()[0])
                    left = max(0, position - 50)
                    right = min(len(line), position + 50)
                    print(line[left:position])
                    print(line[position])
                    print(line[position+1:right])

                if error_count > MAX_ERRORS_LOGGED:
                    sys.exit(0)

    print("Worked:", worked, "  Still broken:", error_count)
