# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from DeEnImporter.download.audio_loader import AudioLoader
from aqt.utils import showInfo



class AudioParser:

    host_url = "https://glosbe.com"

    @classmethod
    def parse_html(cls, html, vocab, from_audio_wanted, dest_audio_wanted, max_audios):
        soup = BeautifulSoup(html)
        from_srcs, dest_srcs = [], []

        if from_audio_wanted:
            from_srcs = cls._from_audio_srcs(soup)
        if dest_audio_wanted:
            dest_srcs = cls._dest_audio_srcs(soup)

        from_file_names, dest_file_names = AudioLoader.download_audios(vocab, from_srcs, dest_srcs, max_audios)
        return from_file_names, dest_file_names

    @classmethod
    def _from_audio_srcs(cls, soup):

        h3s = soup.findAll('h3')
        for h3 in h3s:
            try:
                containers = h3.findAll('span', {'class': 'audioPlayer-container'})
                return cls._parse_containers(containers)
            except AttributeError:
                pass

    @classmethod
    def _dest_audio_srcs(cls, soup):

        uls = soup.findAll('ul')

        for ul in uls:
            try:
                li = ul.find('li', {'class': 'phraseMeaning show-user-name-listener'})
                div = li.find('div', {'class': 'text-info'})
                containers = div.findAll('span', {'class': 'audioPlayer-container'})
                return cls._parse_containers(containers)
            except AttributeError:
                pass

    @classmethod
    def _parse_containers(cls, containers):
        srcs = []

        for container in containers:
            audio_player = container.find('span', {'class': 'audioPlayer'})
            html = str(audio_player)

            url = "{}/{}".format(AudioParser.host_url, cls._remove_html(html))
            srcs.append(url)

        return srcs

    @classmethod
    def _remove_html(cls, html):
        s = html.split('data-url-mp3="')[1]
        s = s.split('"')[0]
        return s
