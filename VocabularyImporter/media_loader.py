import urllib2
import urllib
import os
from VocabularyImporter.parse.audio_parser import AudioParser
from VocabularyImporter.parse.image_parser import ImageParser


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
        Loading the html data, getting the online sources, and downloading them.
        :param vocab: the word from the input in the from language
        :return: arrays of file paths with the medias
        """
        html = self.get_html(vocab)

        image_sources = ImageParser.parse_html(html)
        from_sources, dest_sources = AudioParser.parse_html(html, self.from_audio_wanted, self.dest_audio_wanted)

        image_paths = self._download_images(vocab, image_sources)
        from_audio_paths = self._download_audios('from_%s' % vocab, from_sources)
        dest_audio_paths = self._download_audios('dest_%s' % vocab, dest_sources)

        return image_paths, from_audio_paths, dest_audio_paths

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

    def _download_images(self, vocab, image_sources):
        image_paths = []
        for i in range(len(image_sources)):
            if i >= self.max_images:
                return image_paths
            id_str = '%03d' % (i + 1)
            file_name = self._load_image(vocab, id_str, image_sources[i])
            image_paths.append(file_name)
        return image_paths

    def _download_audios(self, name, sources):
        paths = []
        for i in range(len(sources)):
            if i >= self.max_audios:
                break
            id_str = '%03d' % (i + 1)
            file_name = self._load_audio(name, id_str, sources[i])
            paths.append(file_name)

        return paths

    @classmethod
    def _load_image(cls, name, id_str, url):
        """
        Downloading the image.
        :param name: name of the file
        :param id_str: used to make the file name unique
        :param url: online source to load the file from
        :return: the absolute path of the file, if the download was successful
        """

        original_file_name = url.split('/')[-1]
        file_suffix = original_file_name.split('.')[-1]

        if file_suffix in cls.image_file_suffix_list:
            file_name = "{0}_{1}.{2}".format(cls.image_file_name(name), id_str, file_suffix)
            with open(file_name, 'wb') as file:
                file.write(urllib.urlopen(url).read())
            return file_name

    @classmethod
    def _load_audio(cls, name, id_str, url):
        """
        Downloading the audio.
        :param name: name of the file
        :param id_str: used to make the file name unique
        :param url: online source to load the file from
        :return: the absolute path of the file, if the download was successful
        """

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