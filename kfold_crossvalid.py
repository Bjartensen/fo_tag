import corpus_prep
import fo_tag
import random

"""																|
Requires at least twice the memory of just loading the corpus
to a list.

https://en.wikipedia.org/wiki/Cross-validation_(statistics)#k-fold_cross-validation
"""

def cross_validation(k=10, iterations=5):
	corpus = corpus_prep.getSentences()
	random.shuffle(corpus)
	k_parts = split_list(corpus,k)
	k_minus_1_parts = []
	k_acc = []
	accuracy = 0


	for i in range(k):
		k_minus_1_parts = []
		for n, part in enumerate(k_parts):
			if n == i:
				pass
			else:
				k_minus_1_parts += part

		k_acc.append(evaluate(k_minus_1_parts, k_parts[i], iterations))

	print(k_acc)
	accuracy = sum(k_acc)/len(k_acc)
	print('Accuracy: ' + str(accuracy*100) + '%')

	with open(str(k)+'k_'+str(iterations)+'it.txt', 'w') as f:
		f.write(str(accuracy))

def evaluate(train_corpus, eval_corpus, iterations=5):

	correct = 0
	total = 0
	tagger = fo_tag.FaroeseTagger(False)
	tagger.train(train_corpus, iterations)

	for sent in eval_corpus:
		taggedSent = tagger.tagSent(' '.join([word[0] for word in sent]))

		total += len(sent)
		for i, word in enumerate(sent):
			if word == taggedSent[i]:
				correct += 1

	return correct/total

def split_list(l, n=1):
	length = len(l)
	return [l[i*length // n : (i+1)*length // n] for i in range(n)]
