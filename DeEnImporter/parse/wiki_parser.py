# -*- coding: utf-8 -*-
import re
from BeautifulSoup import BeautifulSoup
from DeEnImporter.download.downloader import Downloader


# TODO: fehler mit [..] bei Katze im satz


class WikiParser:

    @classmethod
    def parse_file(cls, vocab, number_of_sentences):
        with open(Downloader.wiki_file_name(vocab), 'r') as file:
            response_body = file.read()

        example_sentences = cls._parse_response(response_body)
        fitting_sentences = cls._parse_example_sentences(example_sentences, number_of_sentences)
        if fitting_sentences is not None:
            return fitting_sentences
        else:
            print('No fitting example sentences found for "%s"' % vocab)

    @classmethod
    def _parse_response(cls, response_body):
        response_body.replace('>\n<', '><')

        soup = BeautifulSoup(response_body)

        try:
            example = soup.find('span', {'id': 'Beispiele'})
            dl = example.findNext('dl')
            children = dl.findAll('dd')

            example_sentences = []
            for child in children:
                s = cls._remove_html(child)
                if s is not "" or s is not " ":
                    example_sentences.append(s)

            return example_sentences

        except AttributeError:
            pass

    @classmethod
    def _remove_html(cls, html):
        s = str(html).replace("<dd>", '').replace('</dd>', '').replace('<i>', '').replace('</i>', '')
        s = re.sub(r'<sup.*</sup>', '', s)
        s = re.sub(r'\[\d+[, \d+]*\][ ]*', '', s)
        return s

    @classmethod
    def _parse_example_sentences(cls, example_sentences, number_of_sentences):
        if example_sentences is not None:
            # only taking the shorter sentences
            # because they are easier for beginners to understand
            example_sentences.sort(key=len)
            return example_sentences[:number_of_sentences]

