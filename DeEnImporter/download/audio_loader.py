# -*- coding: utf-8 -*-
import urllib
from DeEnImporter.download.media_handler import MediaHandler


class AudioLoader:

    @classmethod
    def download_audios(cls, vocab, srcs, max_audios=5):
        audio_file_names = []
        for i in range(len(srcs)):
            if i >= max_audios:
                return audio_file_names
            id_str = '%03d' % (i+1)
            file_name = cls._load_audio(vocab, id_str, srcs[i])
            audio_file_names.append(file_name)
        return audio_file_names

    @classmethod
    def _load_audio(cls, vocab, id_str, url):
        original_file_name = url.split('/')[-1]
        file_suffix = original_file_name.split('.')[-1]
        if file_suffix in 'mp3':
            file_name = "{0}_{1}.{2}".format(MediaHandler.audio_file_name(vocab), id_str, file_suffix)
            with open(file_name, 'wb') as file:
                file.write(urllib.urlopen(url).read())
            return file_name
