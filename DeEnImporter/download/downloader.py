# -*- coding: utf-8 -*-
import subprocess
import os
import errno
import shutil


class Downloader:

    dict_url_template = "https://de-en.dict.cc/?s={0}"
    wiki_url_template = "https://de.wiktionary.org/wiki/{0}?printable=yes"
    glosbe_url_template = "https://glosbe.com/de/en/{0}"

    temp_data_directory = "temp_data"

    @classmethod
    def download(cls, vocabs, progress_bar):
        cls._make_directory()

        for vocab in vocabs:
            cls._download_dict(vocab)
            cls._download_wiki(vocab)
            cls._download_glosbe(vocab)

            progress_bar.finished_action()

    @classmethod
    def _download_dict(cls, vocab):
        url = cls._format_url(Downloader.dict_url_template, vocab)
        file_name = cls.dict_file_name(vocab)

        with open(file_name, 'w+') as output:
            subprocess.call(['curl', url], stdout=output)

    @classmethod
    def _download_wiki(cls, vocab):
        url = cls._format_url(Downloader.wiki_url_template, vocab)
        file_name = cls.wiki_file_name(vocab)

        with open(file_name, 'w+') as output:
            subprocess.call(['curl', url], stdout=output)

    @classmethod
    def _download_glosbe(cls, vocab):
        url = cls._format_url(Downloader.glosbe_url_template, vocab)
        file_name = cls.glosbe_file_name(vocab)

        with open(file_name, 'w+') as output:
            subprocess.call(['curl', url], stdout=output)

    @classmethod
    def _format_url(cls, template, vocab):
        v = vocab.replace(' ', '_')
        # TODO: format properly
        # v = urllib.parse.quote(v.encode("utf-8"))
        return template.format(v)

    @classmethod
    def dict_file_name(cls, vocab):
        return os.path.join(os.getcwd(),
                            Downloader.temp_data_directory,
                            'dict_%s.html' % vocab)

    @classmethod
    def wiki_file_name(cls, vocab):
        return os.path.join(os.getcwd(),
                            Downloader.temp_data_directory,
                            'wiki_%s.xml' % vocab)

    @classmethod
    def glosbe_file_name(cls, vocab):
        return os.path.join(os.getcwd(),
                            Downloader.temp_data_directory,
                            'glosbe_%s.html' % vocab)

    @classmethod
    def image_file_name(cls, vocab):
        return os.path.join(os.getcwd(), vocab)

    @classmethod
    def audio_file_name(cls, vocab):
        return os.path.join(os.getcwd(), str(vocab))

    @classmethod
    def _make_directory(cls):
        directory = os.path.join(os.getcwd(), Downloader.temp_data_directory)
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    @classmethod
    def clear_temp_data(cls):
        temp_data_path = os.path.join(os.getcwd(), Downloader.temp_data_directory)
        shutil.rmtree(temp_data_path)
