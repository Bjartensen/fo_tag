import fo_tag
import corpus_prep

tagger = fo_tag.FaroeseTagger(overWrite=True)

tagger.train(corpus_prep.getSentences(),2)
