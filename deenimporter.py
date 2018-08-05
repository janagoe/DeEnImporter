from aqt import mw
from aqt.utils import showInfo, getText
from aqt.qt import *
from BeautifulSoup import BeautifulSoup
import os
from anki import Collection

import DeEnImporter.download
from DeEnImporter.download.downloader import Downloader
from DeEnImporter.parse.input_parser import InputParser
from DeEnImporter.parse.dict_parser import DictParser
from DeEnImporter.parse.image_parser import ImageParser
from DeEnImporter.parse.wiki_parser import WikiParser
from DeEnImporter.parse.audio_parser import AudioParser
from DeEnImporter.anki_inserter import AnkiInserter

# this is the file that gets started from anki
# and starts this addon


def run():

    data = getText("Input: ")
    vocabs = InputParser().read_input(data)

    for vocab in vocabs:
        Downloader.download(vocab)


    # the deck already has to exist
    deck_name = "tests"

    # select deck
    deck_id = mw.col.decks.id(deck_name)
    mw.col.decks.select(deck_id)
    deck = mw.col.decks.current()

    # select model
    model = mw.col.models.byName("Basic-Importer")
    model['did'] = deck_id

    deck['mid'] = model['id']
    mw.col.decks.save(deck)


    inserter = AnkiInserter(mw.col, model)

    max_images = 2
    max_audios = 1

    for vocab in vocabs:
        showInfo(str(vocab.__class__))
        translation = DictParser.parse_file(vocab)
        sentences = WikiParser.parse_file(vocab)
        images = ImageParser.parse_file(vocab, max_images)
        audios = AudioParser.parse_file(vocab, max_audios)

        showInfo(str(translation))

        inserter.insert(translation, sentences, images, audios)

    inserter.finish()

    Downloader.clear_temp_data()
    showInfo("DONE")


importAction = QAction("Import Input", mw)
importAction.triggered.connect(run)
mw.form.menuTools.addAction(importAction)

