from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from DeEnImporter.download.downloader import Downloader
from DeEnImporter.parse.input_parser import InputParser
from DeEnImporter.parse.image_parser import ImageParser
from DeEnImporter.parse.audio_parser import AudioParser
from DeEnImporter.anki_inserter import AnkiInserter
from DeEnImporter.ui.input_dialog import InputDialog
from DeEnImporter.ui.progress_bar import ProgressBar
from DeEnImporter.get_model import get_model
from DeEnImporter.parse.example_parser import ExampleParser
from DeEnImporter.parse.translation_parser import TranslationParser


##############################################################################

def run():
    data = InputDialog().run()
    if not data:
        return

    text, translations_nr, sentences_nr, images_nr, audios_nr = data
    vocabs = InputParser().read_input(text)
    showInfo(str(vocabs))

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
    translation_parser = TranslationParser(translations_nr)
    example_parser = ExampleParser(sentences_nr)
    inserter = AnkiInserter(mw.col, model)
    for vocab in vocabs:
        translation = translation_parser.parse(vocab)
        sentences = example_parser.parse(vocab)
        images = ImageParser.parse_file(vocab, images_nr)
        audios = AudioParser.parse_file(vocab, audios_nr)

        inserter.insert(translation, sentences, images, audios)
        progress_bar.finished_action()

    # saving and clearing everything up
    inserter.save()
    Downloader.clear_temp_data()
    finish_message(inserter.get_count())


def finish_message(count):
    count *= 2
    if count > 0:
        showInfo("Successfully created %d new cards." % count)
    else:
        showInfo("No cards could be created.")


# setup anki gui
##############################################################################

importAction = QAction("Import Input", mw)
importAction.triggered.connect(run)
mw.form.menuTools.addAction(importAction)

