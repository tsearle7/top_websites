#Data Analysis of Average Length of Web Page

import csv
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

    input_file = open('sample1mil.json', encoding=('utf-8'))
    average_length = {}
    bell_graph = {}

    error_count = 0
    worked = 0
    for raw_line in input_file:

        line = raw_line
        line = repair(line, replace_with_quote, escape_and_quote)
        line = repair(line, replace_with_blank, multichar)
        line = repair(line, replace_with_blank, escape)
        line = repair(line, replace_with_blank, escape)
        line = stripTags(line)

        try:
            # Load JSON and specify branch
            data_dict = json.loads(line)
            html = data_dict["p80"]["http"]["get"]["body"]
            domain = data_dict["domain"]
            # Begin cleanup of HTML
            souped = BeautifulSoup(html, 'html.parser')
            htmltext = souped.get_text()
            # Output to text file
            words = htmltext.split(' ')
            length = len(words)
            bell_graph[domain] = length

            if length <= 10:
                if "tenwords" in average_length:
                    average_length["tenwords"] += 1
                else:
                    average_length["tenwords"] = 1

            if length <= 100 and length > 10:
                if "hundredwords" in average_length:
                    average_length["hundredwords"] += 1
                else:
                    average_length["hundredwords"] = 1

            if length <= 500 and length > 100:
                if "fivehundredwords" in average_length:
                    average_length["fivehundredwords"] += 1
                else:
                    average_length["fivehundredwords"] = 1

            if length <= 1000 and length > 500:     	
                if "thousandwords" in average_length:
                    average_length["thousandwords"] += 1
                else:
                    average_length["thousandwords"] = 1
            
            if length <= 10000 and length > 1000:
                if "tenthousand" in average_length:
                    average_length["tenthousand"] += 1
                else:
                    average_length["tenthousand"] = 1

            if length <= 1000000 and length > 10000:
                if "million" in average_length:
                    average_length["million"] += 1
                else:
                    average_length["million"] = 1

            worked += 1
        except Exception as error_desc:
            error_count += 1

    with open('average_length.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in average_length.items():
            writer.writerow([key,value])

    with open('bell_graph.csv', 'w') as csv_file:
    	writer = csv.writer(csv_file)
    	for key, value in bell_graph.items():
    		writer.writerow([key,value])

    print("Worked:", worked, "  Still broken:", error_count)
