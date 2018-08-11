import urllib2
from DeEnImporter.parse.audio_parser import AudioParser
from DeEnImporter.parse.image_parser import ImageParser


class MediaLoader:

    def __init__(self, from_lang, dest_lang, from_audio, dest_audio, images_nr, audios_nr):
        self.from_lang = from_lang
        self.dest_lang = dest_lang

        self.from_audio = from_audio
        self.dest_audio = dest_audio

        self.images_nr = images_nr
        self.audios_nr = audios_nr

    def load(self, vocab):
        html = self.get_html(vocab)

        images = ImageParser.parse_html(html, vocab, self.images_nr)
        audios = AudioParser.parse_html(html, vocab, self.from_audio, self.dest_audio, self.audios_nr)

        return images, audios

    def get_html(self, vocab):
        template = u"https://glosbe.com/{}/{}/{}"
        url = template.format(self.from_lang, self.dest_lang, urllib2.quote(vocab))
        response = urllib2.urlopen(url)
        return response.read()
