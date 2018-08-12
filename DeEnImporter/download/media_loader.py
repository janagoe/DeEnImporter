import urllib2
from DeEnImporter.parse.audio_parser import AudioParser
from DeEnImporter.parse.image_parser import ImageParser


class MediaLoader:

    def __init__(self, from_lang_code, dest_lang_code, from_audio_wanted, dest_audio_wanted, images_nr, audios_nr):
        self.from_lang_code = from_lang_code
        self.dest_lang_code = dest_lang_code
        self.from_audio_wanted = from_audio_wanted
        self.dest_audio_wanted = dest_audio_wanted
        self.images_nr = images_nr
        self.audios_nr = audios_nr

    def load(self, vocab):
        html = self.get_html(vocab)
        images = ImageParser.parse_html(html, vocab, self.images_nr)
        audios = AudioParser.parse_html(html, vocab, self.from_audio_wanted, self.dest_audio_wanted, self.audios_nr)
        return images, audios

    def get_html(self, vocab):
        template = u"https://glosbe.com/{}/{}/{}"
        url = template.format(self.from_lang_code, self.dest_lang_code, urllib2.quote(vocab))
        response = urllib2.urlopen(url)
        return response.read()
