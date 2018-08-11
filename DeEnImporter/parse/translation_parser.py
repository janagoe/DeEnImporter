import json
import urllib2
from aqt.utils import showInfo


class TranslationParser:

    def __init__(self, from_lang, dest_lang, translations_nr):
        self.from_lang = from_lang
        self.dest_lang = dest_lang
        self.translations_nr = translations_nr
        self.from_lang_text = ""
        self.dest_lang_text = []

    def parse(self, vocab):
        self.from_lang_text = ""
        self.dest_lang_text = []
        v1, v2 = self.vocab_variations(vocab.decode('utf-8'))

        j1 = self.get_json(v1)
        t1 = self.parse_json(j1)

        j2 = self.get_json(v2)
        t2 = self.parse_json(j2)

        if len(t1) > len(t2):
            self.from_lang_text = v1
            self.dest_lang_text = t1
        else:

            self.from_lang_text = v2
            self.dest_lang_text = t2

        translation = [self.from_lang_text, self.dest_lang_text]
        if self.is_valid_translation(translation):
            return translation

    def get_json(self, vocab):
        template = "https://glosbe.com/gapi_v0_1/translate?from={}&dest={}&format=json&phrase={}&pretty=true"
        url = template.format(self.from_lang, self.dest_lang, urllib2.quote(vocab.encode('utf-8')))
        response = urllib2.urlopen(url)
        return json.loads(response.read())

    def parse_json(self, json_object):
        translations = []
        tuc = json_object[u'tuc']

        try:
            for i in range(min(self.translations_nr, len(tuc))):
                translations.append(tuc[i]['phrase']['text'])
        except KeyError:
            pass

        return translations

    @classmethod
    def vocab_variations(cls, vocab):
        if len(vocab) > 1:
            lower = vocab.lower()
            big = vocab.upper()[0] + lower[1:]
            return big, lower
        else:
            return vocab.upper(), vocab.lower()

    @classmethod
    def is_valid_translation(cls, translation):
        if translation[0] and translation[0] is not "":
            if translation[1] and len(translation[1]) > 0:
                return True
        return False
