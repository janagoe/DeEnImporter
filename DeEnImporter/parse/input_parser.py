# -*- coding: utf-8 -*-
import re


class InputParser:

    @classmethod
    def read_input(cls, text):
        """
        Splitting the words between punctuation characters and white spaces, in case the input
        is a real text.
        :param text: The user input text
        :return: list of the words
        """

        regex = re.compile(ur'[^\wäüöß]', re.UNICODE)

        words = set([])
        for word in regex.split(text):
            words.add(str(word.encode('utf-8')))

        words.discard('')
        return list(words)


