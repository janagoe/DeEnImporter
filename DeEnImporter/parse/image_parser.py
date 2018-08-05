# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from DeEnImporter.download.downloader import Downloader
from DeEnImporter.download.image_loader import ImageLoader


class ImageParser:

    host_url = "https://glosbe.com"

    @classmethod
    def parse_file(cls, vocab, max_images=5):
        with open(Downloader.glosbe_file_name(vocab), 'r') as file:
            response_body = file.read()

        soup = BeautifulSoup(response_body)

        try:
            div = soup.find('div', {'id': 'translation-images'})
            imgs = div.findAll('img')

            image_srcs = []
            for img in imgs:
                html = str(img)
                src = cls._remove_html(html)
                image_srcs.append(ImageParser.host_url + src)

            image_file_names = ImageLoader.download_images(vocab, image_srcs, max_images)
            return image_file_names

        except AttributeError:
            pass

    @classmethod
    def _remove_html(cls, html):
        s = html.split('src="')[1]
        s = s.split('"')[0]
        return s

