# -*- coding: utf-8 -*-
import re


class InputParser:

    @classmethod
    def read_input(cls, text, input_mode):
        """
        If input_mode == "words" splitting the words between punctuation characters and white spaces, in case the input
        is a real text.
        if input_mode == "phrases" splitting each line to be able to translate phrases
        :param text: The user input text
        :param input_mode: "words" or "phrases"
        :return: list of the words
        """

        words = set([])

        if input_mode == "words":
            regex = re.compile(ur'[^\wäüöß]', re.UNICODE)
        elif input_mode == "phrases":
            regex = re.compile(ur'\n', re.UNICODE)
        else:
            return []

        for word in regex.split(text):
            words.add(str(word.encode('utf-8')))

        words.discard('')
        return list(words)
