# -*- coding: iso-8859-1 -*-

"""
Should be tuned to the Faroese language.

Thoughts:
	suffix should be [-2:]
"""

def features(i, word, context, prev, prev2):
	def add(name, *args):
		features[' '.join((name,) + tuple(args))] += 1
	
	i += len(self.START)
	features = defaultdict(int)

	add('bias')
	add('i suffix', word[-2:])
	add('i pref1', word[0])
	add('i-1 tag', prev)
	add('i-2 tag', prev2)

	# doesn't matchup, but not sure which part
	add('i tag+i-2 tag', prev, prev2)

	add('i word', context[i])
	add('i-1 tag+i word', prev, context[i])
	add('i-1 word', context[i-1])
	add('i-1 suffix', context[i-1][-3:])
	add('i-2 word', context[i-2])
	add('i+1 word', context[i+1])
	add('i+1 suffix', context[i+1][-3:])
	add('i+2 word', context[i+2])

	return features

