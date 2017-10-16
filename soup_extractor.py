# Beautiful Soup Extraction of Text
import json
import os
from bs4 import BeautifulSoup
from pprint import pprint
import sys, codecs, locale

if __name__ == '__main__':
    if (sys.stdout.encoding is None):
        print >> sys.stderr, "please set python env PYTHONIOENCODING=UTF-8, example: export PYTHONIOENCODING=UTF-8, when write to stdout."
        exit(1)

if __name__ == "__main__":
	dict1 = json.load(open('sample1.json', encoding='utf-8'))
	for data_dict in dict1:
		for key in ["p80", "http", "get", "body"]:
			print("key", key)
			print("data_dict", data_dict)
			soup1 = dict1[key]
			pprint(soup1)
			souped = BeautifulSoup(soup1, 'html.parser')
			print(souped.get_text())

#soup = BeautifulSoup(html_doc, 'html.parser')

#print(soup.get_text())