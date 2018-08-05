from aqt import mw
from aqt.utils import showInfo, getText
from aqt.qt import *

from DeEnImporter.download.downloader import Downloader
from DeEnImporter.parse.input_parser import InputParser
from DeEnImporter.parse.dict_parser import DictParser
from DeEnImporter.parse.image_parser import ImageParser
from DeEnImporter.parse.wiki_parser import WikiParser
from DeEnImporter.parse.audio_parser import AudioParser
from DeEnImporter.anki_inserter import AnkiInserter


##############################################################################

def run():

    data = getText("Input: ")
    vocabs = InputParser().read_input(data)
    Downloader.download(vocabs)


    # setup anki collection for insertions
    #################################################

    deck_name = "ggggg"

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

    inserter = AnkiInserter(mw.col, model)
    max_images, max_audios = 2, 1

    # parsing downloads and inserting
    for vocab in vocabs:
        translation = DictParser.parse_file(vocab)
        sentences = WikiParser.parse_file(vocab)
        images = ImageParser.parse_file(vocab, max_images)
        audios = AudioParser.parse_file(vocab, max_audios)

        inserter.insert(translation, sentences, images, audios)

    # saving and clearing everything up
    inserter.save()
    Downloader.clear_temp_data()
    showInfo("DONE")


def get_model(col):  # mm = ModelManager
    mm = col.models

    m = mm.byName("Basic-Importer-Test")
    if m:
        mm.setCurrent(m)
        return m

    # creating model
    m = mm.new("Basic-Importer-Test")
    fm = mm.newField("English")
    mm.addField(m, fm)
    fm = mm.newField("German")
    mm.addField(m, fm)
    fm = mm.newField("Examples")
    mm.addField(m, fm)
    fm = mm.newField("Media")
    mm.addField(m, fm)

    # creating template
    t = mm.newTemplate("Card 1")
    t['qfmt'] = "{{English}}"
    t['afmt'] = """{{{FrontSide}}\n\n<hr id=answer>\n{{German}}\n\n<br/>\n{{Examples}}\n<br/>\n{{Media}}"""

    # adding template and model
    mm.addTemplate(m, t)
    mm.add(m)

    mm.setCurrent(m)
    mm.save()
    return m


# setup anki gui
##############################################################################

importAction = QAction("Import Input", mw)
importAction.triggered.connect(run)
mw.form.menuTools.addAction(importAction)

