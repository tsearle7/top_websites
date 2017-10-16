import json
from pprint import pprint
import sys

if __name__ == "__main__":
	#for line in open('sample10.json'):
	#	print(line)

	with open('sample101.json') as sample10_file:
		data = json.load(sample10_file)
	pprint(data["p80"]["http"]["get"]["body"])


	# file = open('sample101.json', 'r')

	# for dict in file:
	# 	for key, value in file.items():
	# 		pprint(data["p80"]["http"]["get"]["body"])

	# file.close()


	# pprint(data["p80"]["http"]["get"]["body"])


