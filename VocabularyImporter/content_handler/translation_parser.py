import json
import urllib2


class TranslationParser:

    def __init__(self, from_lang, dest_lang, translations_nr):
        self.from_lang = from_lang
        self.dest_lang = dest_lang
        self.translations_nr = translations_nr
        self.from_lang_text = ""
        self.dest_lang_text = []

    def parse(self, vocab):
        """
        Searching for translations in the glosbe.com api while considering
        the case sensitivity of the api, and errors in the user input. Choosing the case
        which offers more translations.
        :param vocab: the word from the input in the from language
        :return: The translations from the one word in the from language into multiple words in the
        destination language, e.g. ["from", ["dest1", "dest2"]]; and None if the translation is not valid.
        """
        self.from_lang_text = ""
        self.dest_lang_text = []

        v0 = vocab.decode('utf-8')

        j0 = self._get_json(v0)
        t0 = self._parse_json(j0)

        if len(t0) > 0:
            self.from_lang_text = v0
            self.dest_lang_text = t0

        else:
            v1, v2 = self._vocab_variations(v0)

            j1 = self._get_json(v1)
            t1 = self._parse_json(j1)

            j2 = self._get_json(v2)
            t2 = self._parse_json(j2)

            if len(t1) > len(t2):
                self.from_lang_text = v1
                self.dest_lang_text = t1
            else:
                self.from_lang_text = v2
                self.dest_lang_text = t2

        translation = [self.from_lang_text, self.dest_lang_text]
        if self._is_valid_translation(translation):
            return translation

    def _get_json(self, vocab):
        template = "https://glosbe.com/gapi_v0_1/translate?from={}&dest={}&format=json&phrase={}&pretty=true"
        url = template.format(self.from_lang, self.dest_lang, urllib2.quote(vocab.encode('utf-8')))
        response = urllib2.urlopen(url)
        return json.loads(response.read())

    def _parse_json(self, json_object):
        """
        Parsing all translations from the json_object.
        :param json_object:
        :return: array of translations in the destination language
        """
        translations = []
        tuc = json_object[u'tuc']

        try:
            for i in range(min(self.translations_nr, len(tuc))):
                translations.append(tuc[i]['phrase']['text'])
        except KeyError:
            pass

        return translations

    @classmethod
    def _vocab_variations(cls, vocab):
        """
        The glosbe.com api might offer no valid translations if the capitalization of the input word
        is wrong. Therefore we once use both capital and small initial letters.
        :param vocab: the word from the input in the from language
        :return: the vocab with a capital initial letter, and the vocab with a small initial letter
        """
        if len(vocab) > 1:
            lower = vocab.lower()
            big = vocab.upper()[0] + lower[1:]
            return big, lower
        else:
            return vocab.upper(), vocab.lower()

    @classmethod
    def _is_valid_translation(cls, translation):
        """
        Looking if objects arent NoneType and if its not an empty string
        :param translation: array of the translation
        :return: True if the translation is valid, False if not
        """
        if translation[0] and translation[0] is not "":
            if translation[1] and len(translation[1]) > 0:
                return True
        return False
