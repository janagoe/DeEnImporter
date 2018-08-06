from BeautifulSoup import BeautifulSoup
import re
from DeEnImporter.download.downloader import Downloader


# TODO: parse html fehler bei "Pink", giraffe zum beispiel

# parts taken and modified from
# https://pypi.org/project/dict.cc.py/#description

class DictParser(object):

    @classmethod
    def parse_file(cls, vocab, number_of_wanted_translations):
        with open(Downloader.dict_file_name(vocab), 'r') as file:
            response_body = file.read()

        translation_tuples = cls._parse_response(response_body)
        if translation_tuples is not None:
            return cls._parse_translation(vocab, translation_tuples, number_of_wanted_translations)
        else:
            print('No translations found for "%s"' % vocab)

    @classmethod
    def _parse_response(cls, response_body):
        en_list = []
        de_list = []

        soup = BeautifulSoup(response_body)

        max_vocabs_per_page = 50
        for i in range(1, max_vocabs_per_page+1):

            try:
                tr = soup.find('tr', {'id': "tr%d" % i})
                children = tr.findAll('td')

                left_td = children[1]
                right_td = children[2]

                left_links = left_td.findAll('a')
                right_links = right_td.findAll('a')

                left = cls._extract_vocab_from_links(left_links)
                right = cls._extract_vocab_from_links(right_links)

                en_list.append(str(left))
                de_list.append(str(right))

            except AttributeError:
                pass

        return zip(de_list, en_list)

    @classmethod
    def _extract_vocab_from_links(cls, links_list):
        content = []
        for link in links_list:
            word = cls._remove_link_html(str(link))
            if '[' not in word and '<' not in word:
                content.append(word)

        # putting content together into a string
        return " ".join(content)

    @classmethod
    def _remove_link_html(cls, s):
        s = re.sub(r'</a>$', '', s)
        s = re.sub(r'^(.*">)', '', s)
        s = re.sub(r'</*b>', '', s)
        return s

    @classmethod
    def _parse_translation(cls, vocab, translation_tuples, number_of_wanted_translations):
        equals_list = []
        different_capitalization_list = []

        for translation in list(translation_tuples):
            if str(translation[0]) == str(vocab):
                equals_list.append(translation)
            elif str(translation[0]).lower() == str(vocab).lower():
                different_capitalization_list.append(translation)

        good_translations = equals_list + different_capitalization_list
        good_translations = good_translations[:number_of_wanted_translations]

        if any(good_translations):
            front = good_translations[0][0]
            back = []
            for translation in good_translations:
                back.append(translation[1])
            return front, back
        else:
            print('No fitting translations found for "%s"' % vocab)
