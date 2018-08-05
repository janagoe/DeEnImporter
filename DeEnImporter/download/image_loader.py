# -*- coding: utf-8 -*-
import urllib
from DeEnImporter.download.downloader import Downloader


class ImageLoader:

    file_suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', ]

    @classmethod
    def download_images(cls, vocab, srcs, max_images=5):
        image_file_names = []
        for i in range(len(srcs)):
            if i >= max_images:
                return image_file_names
            id_str = '%03d' % (i+1)
            file_name = cls._load_image(vocab, id_str, srcs[i])
            image_file_names.append(file_name)

    @classmethod
    def _load_image(cls, vocab, id_str, url):
        original_file_name = url.split('/')[-1]
        file_suffix = original_file_name.split('.')[-1]
        if file_suffix in ImageLoader.file_suffix_list:
            file_name = "{0}_{1}.{2}".format(Downloader.image_file_name(vocab), id_str, file_suffix)
            with open(file_name, 'wb') as file:
                file.write(urllib.urlopen(url).read())
            return file_name
