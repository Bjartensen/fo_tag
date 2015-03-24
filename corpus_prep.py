# -*- coding: utf-8 -*-

"""																|
The file doesn't really prepare the default corpus properly.
The default corpus' delimiter -- '\n' -- doesn't delimit every
sentence. Some functionality to detect punctuation that
actually splits sentences should be added.
"""

def getSentences(corpus='..\\corpus.txt', enc='utf-8', sentDelim='\n', ignore='%'):
	sentences = []
	sent = []

	f = open(corpus, encoding=enc)

	for line in f:
		if ignore in line:
			pass
		elif line == sentDelim:
			if not sent == []:
				sentences.append(sent)
			sent = []
		else:
			sent.append(tuple(line.split()))

	return sentences

