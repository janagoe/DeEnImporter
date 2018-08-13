from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from VocabularyImporter.content_handler.input_parser import InputParser
from VocabularyImporter.anki_inserter import AnkiInserter
from VocabularyImporter.input_dialog import InputDialog
from VocabularyImporter.get_model import get_model
from VocabularyImporter.content_handler.example_parser import SentencesParser
from VocabularyImporter.content_handler.translation_parser import TranslationParser
from VocabularyImporter.content_handler.media_loader import MediaLoader
from vocabimporter import deck_name

##############################################################################

def run():

    # getting user input
    data = InputDialog().run()
    if not data:
        return
    else:
        text, translations_nr, sentences_nr, images_nr, audios_nr,\
            from_lang, dest_lang, from_audio_wanted, dest_audio_wanted, image_side = data

    vocabs = InputParser().read_input(text)

    # setup anki collection for insertions
    #################################################

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

    # parsing downloads and inserting
    #################################################

    translation_parser = TranslationParser(from_lang, dest_lang, translations_nr)
    example_parser = SentencesParser(from_lang, dest_lang, sentences_nr)
    media_loader = MediaLoader(from_lang, dest_lang, from_audio_wanted, dest_audio_wanted, images_nr, audios_nr)
    inserter = AnkiInserter(mw.col, model, from_lang, dest_lang, image_side)

    for vocab in vocabs:
        translation = translation_parser.parse(vocab)
        if translation:
            sentences = example_parser.parse(vocab)
            images, from_audios, dest_audios = media_loader.load(vocab)

            inserter.insert(translation, sentences, images, from_audios, dest_audios)

    # saving and clearing everything up
    #################################################

    inserter.save()
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

