import json
import urllib2


class ExampleParser:
    def __init__(self, sentences_nr):
        self.sentences_nr = sentences_nr

    def parse(self, vocab):
        json_object = self.get_json(vocab)
        examples = self.parse_json(json_object)
        return self.choose_examples(examples)

    def parse_json(self, json_object):
        ex = json_object['examples']
        examples = []
        # parsing more than necessary to a greater variety to choose from
        for i in range(min(self.sentences_nr*2, len(ex))):
            de = ex[i]['first']
            en = ex[i]['second']
            examples.append([de, en])
        return examples

    def choose_examples(self, examples):
        examples.sort(key=len)
        # choosing good sentences with a short length, easier for beginners
        return examples[:self.sentences_nr]

    def get_json(self, vocab):
        template = "https://glosbe.com/gapi_v0_1/tm?from=deu&dest=eng&format=json&phrase={}&pretty=true"
        url = template.format(urllib2.quote(vocab))
        response = urllib2.urlopen(url)
        return json.loads(response.read())
