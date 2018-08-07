from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from DeEnImporter.download.downloader import Downloader
from DeEnImporter.parse.input_parser import InputParser
from DeEnImporter.parse.dict_parser import DictParser
from DeEnImporter.parse.image_parser import ImageParser
from DeEnImporter.parse.wiki_parser import WikiParser
from DeEnImporter.parse.audio_parser import AudioParser
from DeEnImporter.anki_inserter import AnkiInserter
from DeEnImporter.input_dialog import InputDialog
from DeEnImporter.progress_bar import ProgressBar

from DeEnImporter.get_model import get_model


##############################################################################

def run():
    data = InputDialog().run()
    if not data:
        return

    text, translations_nr, sentences_nr, images_nr, audios_nr = data
    vocabs = InputParser().read_input(text)

    progress_bar = ProgressBar(len(vocabs))
    # progress_bar.run()

    Downloader.download(vocabs, progress_bar)

    # setup anki collection for insertions
    #################################################

    deck_name = "DeEnImporter"

    # select deck
    deck_id = mw.col.decks.id(deck_name, create=True)
    mw.col.decks.select(deck_id)
    deck = mw.col.decks.current()

    # select model
    model = get_model(mw.col)
    model['did'] = deck_id

    deck['mid'] = model['id']
    mw.col.decks.save(deck)
    mw.col.models.save()

    #################################################

    # parsing downloads and inserting
    inserter = AnkiInserter(mw.col, model)
    for vocab in vocabs:
        translation = DictParser.parse_file(vocab, translations_nr)
        sentences = WikiParser.parse_file(vocab, sentences_nr)
        images = ImageParser.parse_file(vocab, images_nr)
        audios = AudioParser.parse_file(vocab, audios_nr)

        inserter.insert(translation, sentences, images, audios)
        progress_bar.finished_action()

    # saving and clearing everything up
    inserter.save()
    Downloader.clear_temp_data()
    finish_message(inserter.get_count())


def finish_message(count):
    if count == 1:
        showInfo("Successfully created one new card.")
    elif count > 1:
        showInfo("Successfully created %d new cards." % count)
    else:
        showInfo("No cards could be created.")


# setup anki gui
##############################################################################

importAction = QAction("Import Input", mw)
importAction.triggered.connect(run)
mw.form.menuTools.addAction(importAction)

