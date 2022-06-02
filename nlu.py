from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

import commands


class NLU:
    def __init__(self):
        self.__vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
        self.__classifier_probability = LogisticRegression()
        self.__classifier = LinearSVC()
        commands.prepare_corpus(self.__vectorizer, self.__classifier, self.__classifier_probability)

    @property
    def vectorizer(self):
        return self.__vectorizer

    @property
    def classifier(self):
        return self.__classifier

    @property
    def classifier_probability(self):
        return self.__classifier_probability
