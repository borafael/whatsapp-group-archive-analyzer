# coding=utf8

import sys
import datetime
import string
import re

def cleanWord(word):
	return word.translate(None, string.punctuation).strip().lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

def loadStopWords():
	stopWords = set()
	try:
		file = open('stopwords.txt', 'r')
		for line in file:
			stopWords.add(line[:-1])
	finally:
		file.close()
	return stopWords

def analyzeLine(line):
	try:
		parts = line.split(' - ', 1)
		date = parts[0]
		user = parts[1].split(':', 1)[0]
		message = parts[1].split(':', 1)[1][:-1]
		return (date, user, message if message.strip() != '<Multimedia omitido>' else None)
	except:
		return (None, None, None)

def analyze(path):
	words = dict()
	stopWords = loadStopWords()
	pattern = re.compile('(j|a)(j|a)*')
	try:
		file = open(path, 'r')
		for line in file:
			(date, user, message) = analyzeLine(line)
			if date != None and user != None and message != None:
				for word in message.split(' '):
					word = cleanWord(word)
					if word not in stopWords and len(word) > 2 and not pattern.match(word):
						if word not in words:
							words[word] = 0
						words[word] = words[word] + 1
				
	finally:
		file.close()

	ranking = words.keys()
	for word in sorted(ranking, key=lambda word: words[word], reverse=True):
		print(word + ';' + str(words[word]))

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("Usage: python analyzer.py <path>")
	else:
		analyze(sys.argv[1])

