# -*- coding: utf-8 -*-
import urllib
from DeEnImporter.download.media_handler import MediaHandler


class AudioLoader:

    @classmethod
    def download_audios(cls, vocab, from_srcs, dest_srcs, max_audios):
        from_file_names = []
        for i in range(len(from_srcs)):
            if i >= max_audios:
                break
            id_str = '%03d' % (i + 1)
            file_name = cls._load_audio('from_%s' % vocab, id_str, from_srcs[i])
            from_file_names.append(file_name)

        dest_file_names = []
        for i in range(len(dest_srcs)):
            if i >= max_audios:
                break
            id_str = '%03d' % (i + 1)
            file_name = cls._load_audio('dest_%s' % vocab, id_str, dest_srcs[i])
            dest_file_names.append(file_name)

        return from_file_names, dest_file_names

    @classmethod
    def _load_audio(cls, name, id_str, url):
        original_file_name = url.split('/')[-1]
        file_suffix = original_file_name.split('.')[-1]
        if file_suffix in 'mp3':
            file_name = "{0}_{1}.{2}".format(MediaHandler.audio_file_name(name), id_str, file_suffix)
            with open(file_name, 'wb') as file:
                file.write(urllib.urlopen(url).read())
            return file_name
