import json
from pprint import pprint
import sys
from bs4 import BeautifulSoup
import re

if __name__ == "__main__":

	invalid_escape = re.compile(r'\\[0-7]{1,3}')  # up to 3 digits for byte values up to FF

	invalid_escape2 = re.compile(r'\\[^tn]')

	def replace_with_byte(match):
		return chr(int(match.group(0)[1:], 8))

	def replace_with_letter(match):
		return "?"

	def repair(brokenjson):
		return invalid_escape.sub(replace_with_byte, brokenjson)

	def repair2(brokenjson):
		return invalid_escape2.sub(replace_with_letter, brokenjson)

	current = {}


	useful_keys = ["p80", "http", "get", "body"]

	f = open('sample1000.json', encoding=('utf-8'))

	languages = open('languages.txt', 'w')

	output = open('output1.txt', 'w')

	i = 0
	j = 0
	
	translation_table = dict.fromkeys(map(ord, '\n'), None)


	for line in f:
		try:
			data_dict = json.loads(repair2(repair(line)))
			#print(i+j)
			if "p80" in data_dict:

				current = data_dict["p80"]["http"]["get"]["body"]
				# print("current", current)
				souped = BeautifulSoup(current, 'html.parser')
				#print("souped", souped)
				# Kill all script and style elements
				for script in souped(["script", "style"]):
					script.decompose()
				# Format each line in preparation for HTML
				output.write("Domain: ")
				output.write(data_dict["domain"])
				output.write(" | ")
				# Get HTML text
				htmltext = souped.get_text()
				# Take out unnecessary whitespace
				lines = (line.strip() for line in htmltext.splitlines())
				# Remove returns in text
				results = '\n'.join(chunk for chunk in lines if lines)
				# Remove any further unnecessary line breaks
				results = results.translate(translation_table)
				# Output the formatted HTML
				output.write(results)
				#Detect Language and Output Data
				# lang_data = detect_language(results)
				# languages.write(lang_data)
				# languages.write("\n")
				# Skip line for next domain to be input
				output.write("\n")
				j += 1
				

		except (TypeError, KeyError):
				print("Error at", key)
				print(repr(data_dict))
				raise		

	print(i, "Lines Skipped")




				