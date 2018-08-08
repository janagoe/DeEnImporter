# -*- coding: utf-8 -*-
import re
from aqt.utils import showInfo


class InputParser:

    def __init__(self):
        self.words = set([])
        self.word_count = {}
        self.sorted_words = []

    def read_input(self, text):

        regex = re.compile(ur'[^\wäüöß]', re.UNICODE)

        for word in regex.split(text):
            self.words.add(str(word.encode('utf-8')))

        self._count_words()
        return self.sorted_words

    def _count_words(self):
        for word in self.words:
            if word in self.word_count:
                self.word_count[word] += 1
            else:
                self.word_count[word] = 1

        for key, value in self.word_count.items():
            self.sorted_words.append(key)

        self.sorted_words = sorted(self.sorted_words,
                                   key=lambda x: self.word_count[x],
                                   reverse=True)

