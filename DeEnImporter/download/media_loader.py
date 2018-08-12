import urllib2
import urllib
import os
from DeEnImporter.parse.audio_parser import AudioParser
from DeEnImporter.parse.image_parser import ImageParser


class MediaLoader:

    image_file_suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', ]

    def __init__(self, from_lang_code, dest_lang_code, from_audio_wanted, dest_audio_wanted, max_images, max_audios):
        self.from_lang_code = from_lang_code
        self.dest_lang_code = dest_lang_code
        self.from_audio_wanted = from_audio_wanted
        self.dest_audio_wanted = dest_audio_wanted
        self.max_images = max_images
        self.max_audios = max_audios

    def load(self, vocab):
        """
        Loading the html data and parsing it.
        :param vocab: the word from the input in the from language
        :return: arrays of file paths with the medias
        """
        html = self.get_html(vocab)
        images = ImageParser.parse_html(html, vocab, self.max_images)
        audios = AudioParser.parse_html(html, vocab, self.from_audio_wanted, self.dest_audio_wanted, self.max_audios)
        return images, audios

    def get_html(self, vocab):
        """
        Loading the html data from glosbe.com
        :param vocab: the word from the input in the from language
        :return: unicode string of the html
        """
        template = u"https://glosbe.com/{}/{}/{}"
        url = template.format(self.from_lang_code, self.dest_lang_code, urllib2.quote(vocab))
        response = urllib2.urlopen(url)
        return response.read()

    def download_images(self, vocab, sources):
        image_file_names = []
        for i in range(len(sources)):
            if i >= self.max_images:
                return image_file_names
            id_str = '%03d' % (i + 1)
            file_name = self._load_image(vocab, id_str, sources[i])
            image_file_names.append(file_name)
        return image_file_names

    @classmethod
    def _load_image(cls, vocab, id_str, url):
        original_file_name = url.split('/')[-1]
        file_suffix = original_file_name.split('.')[-1]
        if file_suffix in cls.image_file_suffix_list:
            file_name = "{0}_{1}.{2}".format(cls.image_file_name(vocab), id_str, file_suffix)
            with open(file_name, 'wb') as file:
                file.write(urllib.urlopen(url).read())
            return file_name

    def download_audios(self, vocab, from_sources, dest_sources):
        from_file_names = []
        for i in range(len(from_sources)):
            if i >= self.max_audios:
                break
            id_str = '%03d' % (i + 1)
            file_name = self._load_audio('from_%s' % vocab, id_str, from_sources[i])
            from_file_names.append(file_name)

        dest_file_names = []
        for i in range(len(dest_sources)):
            if i >= self.max_audios:
                break
            id_str = '%03d' % (i + 1)
            file_name = self.._load_audio('dest_%s' % vocab, id_str, dest_sources[i])
            dest_file_names.append(file_name)

        return from_file_names, dest_file_names

    @classmethod
    def _load_audio(cls, name, id_str, url):
        original_file_name = url.split('/')[-1]
        file_suffix = original_file_name.split('.')[-1]
        if file_suffix in 'mp3':
            file_name = "{0}_{1}.{2}".format(cls.audio_file_name(name), id_str, file_suffix)
            with open(file_name, 'wb') as file:
                file.write(urllib.urlopen(url).read())
            return file_name

    @classmethod
    def image_file_name(cls, vocab):
        """
        :param vocab: the word from the input in the from language
        :return: absolute path from the image file
        """
        return os.path.join(os.getcwd(), vocab)

    @classmethod
    def audio_file_name(cls, vocab):
        """
        :param vocab: the word from the input in the from language
        :return: absolute path from the audio file
        """
        return os.path.join(os.getcwd(), vocab)