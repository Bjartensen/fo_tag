import corpus_prep
import fo_tag
import random
import operator

"""																|
Requires at least twice the memory of just loading the corpus
to a list.

https://en.wikipedia.org/wiki/Cross-validation_(statistics)#k-fold_cross-validation
"""

class CrossValidation():
    'k-fold cross validation tool'
    version = '0.1'

    def __init__(self):
        self.sents = []
        self.k_parts = []
        self.k_acc = []
        self.accuracy = 0
        self.k = 0
        self.it = 0

        self.tagErrors = {}
        self.wordErrors = {}
        self.sentErrors = {}

    def load(self):
        self.sents = corpus_prep.getSentences()
        random.shuffle(self.sents)
        
    def cross_validate(self, k=10, it=5, log=False):
        self.k = k
        self.it = it
        self.k_parts = self._split(self.sents, self.k)
        
        for i in range(k):
            k_minus_1_parts = []
            for n, part in enumerate(self.k_parts):
                if n == i:
                    pass
                else:
                    k_minus_1_parts += part

            self.k_acc.append(self._evaluate(k_minus_1_parts, self.k_parts[i]))
            print(self.k_acc[i])
        
        
        sorted_tags = sorted(self.tagErrors.items(), key=operator.itemgetter(1))


        # simple logging of errors
        if log:
            with open('tags.txt', 'w') as tagF:
                for key, value in sorted(self.tagErrors.items(),
                        key = operator.itemgetter(1)):

                    tagF.write(str(value)+' -- '+key+'\n')


            with open('words.txt', 'w') as wordF:
                for key, value in sorted(self.wordErrors.items(),
                        key = operator.itemgetter(1)):

                    wordF.write(str(value)+' -- '+key+'\n')


            with open('sents.txt', 'w') as sentF:
                for key, value in sorted(self.sentErrors.items(),
                        key = operator.itemgetter(1)):
                    sentF.write(str(value)+' -- '+key+'\n')



    def _evaluate(self, train_corpus, eval_corpus):

        correct = 0
        total = 0
        tagger = fo_tag.FaroeseTagger(False)
        tagger.train(train_corpus, self.it)

        for sent in eval_corpus:
            taggedSent = tagger.tagSent(' '.join([word[0] for word in sent]))

            total += len(sent)
            for i, word in enumerate(sent):
                if word == taggedSent[i]:
                    correct += 1
                else:
                    self.tagErrors[word[1]] = self.tagErrors.get(word[1], 0) + 1

                    self.wordErrors[word[0]] = self.wordErrors.get(word[0], 0) + 1


                    errorSent = ''
                    errorSent += str(word[0])+'/'+str(word[1])+': '
                    for w,t in sent:
                        errorSent += w+'/'+t+' '
                    self.sentErrors[errorSent] = self.sentErrors.get(errorSent, 0) + 1


        return correct/total

    def _split(self, l, n=1):
        length = len(l)
        return [l[i*length // n : (i+1)*length // n] for i in range(n)]
