# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup


class AudioParser:

    host_url = "https://glosbe.com"

    @classmethod
    def parse_html(cls, html, from_audio_wanted, dest_audio_wanted):
        """
        Searching in the html data for the audio sources in the from and destination language,
        and letting the AudioLoader load the audios
        :param html: the html data
        :param vocab: the word from the input in the from language
        :param from_audio_wanted: boolean if the user wants to have audios in the from language
        :param dest_audio_wanted: boolean if the user wants to have audios in the destination language
        :param max_audios: the maximal number of audios the user wants to have for each language
        :return: paths for the files in the from and destination language
        """
        soup = BeautifulSoup(html)
        from_sources, dest_sources = [], []

        if from_audio_wanted:
            from_sources = cls._from_audio_srcs(soup)
        if dest_audio_wanted:
            dest_sources = cls._dest_audio_srcs(soup)

        return from_sources, dest_sources

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
