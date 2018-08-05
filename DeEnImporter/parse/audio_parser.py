# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from DeEnImporter.download.downloader import Downloader
from DeEnImporter.download.audio_loader import AudioLoader


class AudioParser:

    host_url = "https://glosbe.com"

    @classmethod
    def parse_file(cls, vocab, max_audios=5):
        with open(Downloader.glosbe_file_name(vocab), 'r') as file:
            response_body = file.read()

        soup = BeautifulSoup(response_body)

        h3 = soup.findAll('h3')
        audio_srcs = []

        for h in h3:
            try:
                audio_player_containers = h.findAll('span', {'class': 'audioPlayer-container'})
                for container in audio_player_containers:

                    audio_player = container.find('span', {'class': 'audioPlayer'})
                    html = str(audio_player)

                    url = "{0}/{1}".format(AudioParser.host_url, cls._remove_html(html))
                    audio_srcs.append(url)
            except AttributeError:
                pass

        audio_file_names = AudioLoader.download_audios(vocab, audio_srcs, max_audios)
        return audio_file_names

    @classmethod
    def _remove_html(cls, html):
        s = html.split('data-url-mp3="')[1]
        s = s.split('"')[0]
        return s
