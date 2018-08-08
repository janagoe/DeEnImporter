import json
import urllib2
from aqt.utils import showInfo


class TranslationParser:

    def __init__(self, translations_nr):
        self.translations_nr = translations_nr
        self.german = ""
        self.english = []

    def parse(self, vocab):
        self.german = ""
        self.english = []
        v1, v2 = self.vocab_variations(vocab)

        j1 = self.get_json(v1)
        t1 = self.parse_json(j1)
        if len(t1) > 1:
            self.german = v1
            self.english = t1
        else:
            j2 = self.get_json(v2)
            t2 = self.parse_json(j2)
            self.german = v2
            self.english = t2

        return self.german, self.english

    def get_json(self, vocab):
        template = "https://glosbe.com/gapi_v0_1/translate?from=deu&dest=eng&format=json&phrase={}&pretty=true"
        url = template.format(vocab)
        response = urllib2.urlopen(url)
        return json.loads(response.read())

    def parse_json(self, json_object):
        tuc = json_object['tuc']
        translations = []
        for i in range(min(self.translations_nr, len(tuc))):
            translations.append(tuc[i]['phrase']['text'])
        return translations

    def vocab_variations(self, vocab):
        lower = vocab.lower()
        big = vocab.upper()[0] + lower[1:]
        return lower, big
