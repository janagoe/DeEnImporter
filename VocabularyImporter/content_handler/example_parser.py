import json
import urllib2


class SentencesParser:
    def __init__(self, from_lang_code, dest_lang_code, sentences_nr):
        self.from_lang_code = from_lang_code
        self.dest_lang_code = dest_lang_code
        self.sentences_nr = sentences_nr

    def parse(self, vocab):
        json_object = self._get_json(vocab)
        sentences = self._parse_json(json_object)
        return self._choose_sentences(sentences)

    def _parse_json(self, json_object):
        ex = json_object['examples']
        sentences = []

        # parsing more than necessary to have a greater variety to choose from
        for i in range(min(self.sentences_nr*2, len(ex))):
            from_text = ex[i]['first']
            dest_text = ex[i]['second']
            sentences.append([from_text, dest_text])
        return sentences

    def _choose_sentences(self, sentences):
        """
        Choosing the shortest sentences, because some sentences
        on glosbe.com are very long and complicated
        :param sentences: array of all the parsed sentences
        :return: array of the shortest sentences
        """
        sentences.sort(key=len)
        return sentences[:self.sentences_nr]

    def _get_json(self, vocab):
        template = u"https://glosbe.com/gapi_v0_1/tm?from={}&dest={}&format=json&phrase={}&pretty=true"
        url = template.format(self.from_lang_code, self.dest_lang_code, urllib2.quote(vocab))
        response = urllib2.urlopen(url)
        return json.loads(response.read())
