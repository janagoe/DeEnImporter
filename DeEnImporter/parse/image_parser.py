# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from DeEnImporter.download.image_loader import ImageLoader


class ImageParser:

    host_url = "https://glosbe.com"

    @classmethod
    def parse_html(cls, html, vocab, max_images):
        """
        Searching in the html data for the image sources, and letting the ImageLoader load the images.
        :param html: the html data
        :param vocab: the word from the input in the from language
        :param max_images: the maximal number of images the user wants
        :return: paths of the images
        """
        soup = BeautifulSoup(html)
        image_srcs = []

        try:
            div = soup.find('div', {'id': 'translation-images'})
            imgs = div.findAll('img')
            for img in imgs:
                html = str(img)
                src = cls._remove_html(html)
                image_srcs.append(ImageParser.host_url + src)
        except AttributeError:
            pass
        finally:
            image_file_names = ImageLoader.download_images(vocab, image_srcs, max_images)
            return image_file_names


    @classmethod
    def _remove_html(cls, html):
        s = html.split('src="')[1]
        s = s.split('"')[0]
        return s

