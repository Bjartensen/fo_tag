# -*- coding: iso-8859-1 -*-
import corpus_prep
import features_fo
from collections import defaultdict
import random
import pickle

"""
AveragedPerceptron to be used in a tagging scheme.

Taken from:
https://github.com/sloria/textblob-aptagger/blob/master/textblob_aptagger/_perceptron.py
and
http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/

Will probably have to make adjustments to make it better fit Faroese, but the general AveragePerceptron is probably good enough as is.
"""

class FaroeseTagger:

	def __init__(self, load=True):
		self.initialized = False

		self.weights = {}
		self._totals = defaultdict(int)
		self._tstamps = defaultdict(int)
		self.i = 0
		self.classes = set()
		self.tagdict = {}

		self.START = ['-START-', '-START2-']
		self.END = ['-END-', '-END-']

		if load:
			self.load('tagger')


	#Perceptron functions
	def predict(self, features):
		scores = defaultdict(float)
		for feat, value in features.items():
			if feat not in self.weights or value == 0:
				continue

			weights = self.weights[feat]
			for label, weight in weights.items():
				scores[label] += value*weight

		return max(self.classes, key=lambda label: (scores[label], label))

	def update(self, truth, guess, features):
		def upd_feat(c, f, w, v):
			param = (f, c)
			self._totals[param] += (self.i - self._tstamps[param])*w
			self._tstamps[param] = self.i
			self.weights[f][c] = w+v

		self.i += 1

		if truth == guess:
			return None

		for f in features:
			weights = self.weights.setdefault(f, {})
			upd_feat(truth, f, weights.get(truth, 0.0), 1.0)
			upd_feat(guess, f, weights.get(guess, 0.0), -1.0)


	def average_weights(self):
		for feat, weights in self.weights.items():
			new_feat_weights = {}
			for clas, weight in weights.items():
				param = (feat, clas)
				total = self._totals[param]
				total += (self.i - self._tstamps[param])*weight
				averaged = round(total / float(self.i), 3)
				if averaged:
					new_feat_weights[clas] = averaged

			self.weights[feat] = new_feat_weights


########################

	def tagSent(self, sent):
		tokens = sent.split()
		prev, prev2 = self.START

		context = self.START + [self._clean(w) for w in tokens] + self.END

		tagged = []
		for i, word in enumerate(tokens):
			tag = self.tagdict.get(word)
			if not tag:
				features = features_fo.features(i, word, context, prev, prev2)
				tag = self.predict(features)
			tagged.append((word, tag))
			prev2 = prev
			prev = tag

		return tagged

	
	def train(self, sentences, iterations=5):
		self._make_tagdict(sentences)

		prev, prev2 = self.START

		for it in range(iterations):
			c = 0
			n = 0

			for sents in sentences:
				words = [half[0] for half in sents]
				tags = [half[1] for half in sents]
				context = self.START + [self._clean(w) for w in words] + self.END 

				for i, word in enumerate(words):
					
					guess = self.tagdict.get(word)

					if not guess:
						feats = features_fo.features(i, word, context, prev, prev2)
						guess = self.predict(feats)
						self.update(tags[i], guess, feats)

					prev2 = prev
					prev = guess

					c += guess == tags[i]
					n += 1

			random.shuffle(sentences)
		self.average_weights()
					
		if self.initialized:
			pickle.dump((self.weights, self.tagdict, self.classes),
					open('tagger', 'wb'), -1)

	def load(self, path):
		try:
			w_td_c = pickle.load(open(path, 'rb'))
			self.initialized = True
		except IOError:
			print('no file')
			return

		self.weights, self.tagdict, self.classes = w_td_c

	def _clean(self, word):
		"""
		need something to like a dictionary to
		recognize abbreviations like t.d. and o.s.fr
		"""

		if '-' in word and word != '-':
			return '!HYPHEN'
		elif '/' in word and word != '/':
			return '!ABBREVIATION'
		elif word.isdigit() and len(word) == 4:
			return '!YEAR'
		elif word[0].isdigit():
			return '!DIGITS'

		else:
			#not sure about this
			return word.lower()

		return None

	def _make_tagdict(self, sentences):
		counts = defaultdict(lambda: defaultdict(int))

		for sents in sentences:
			for word, tag in sents:
				counts[word][tag] += 1
				self.classes.add(tag)

		# only add common and unambiguous words
		# they should probably be tuned to the corpus size
		freq_thresh = 20
		ambiguity_thresh = 0.97

		for word, tag_freqs in counts.items():
			tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
			n = sum(tag_freqs.values())

			if n >= freq_thresh and (float(mode) / n) >= ambiguity_thresh:
				self.tagdict[word] = tag
