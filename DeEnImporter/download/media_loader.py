import urllib2
from DeEnImporter.parse.audio_parser import AudioParser
from DeEnImporter.parse.image_parser import ImageParser


class MediaLoader:

    def __init__(self, images_nr, audios_nr):
        self.images_nr = images_nr
        self.audios_nr = audios_nr

    def load(self, vocab):
        html = self.get_html(vocab)

        images = ImageParser.parse_html(html, vocab, self.images_nr)
        audios = AudioParser.parse_html(html, vocab, self.audios_nr)

        return images, audios

    def get_html(self, vocab):
        template = "https://glosbe.com/de/en/{}"
        url = template.format(urllib2.quote(vocab))
        response = urllib2.urlopen(url)
        return response.read()
