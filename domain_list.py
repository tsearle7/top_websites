# Data Analysis of Domains

import csv
import json
import sys
import re
from bs4 import BeautifulSoup

if __name__ == "__main__":

	input_file = open('sample1mil.json', encoding=('utf-8'))
	output_file = open('countries.txt', 'w')

	country_list= {}
	worked= 0
	error_count = 0

	for raw_line in input_file:
		try:
			line = raw_line
			data_dict = json.loads(line)
			domains = data_dict["domain"]
			splitdomain = domains.split('.')
			country = splitdomain[-1]
			#print(country)

			if country in country_list:
				country_list[country] += 1
			else:
				country_list[country] = 1
			worked += 1
		except Exception as error_desc:
			error_count += 1

	with open('country_list.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in country_list.items():
			writer.writerow([key,value])


	print(error_count)



