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


##############################################################################

def run():
    data = get_input()
    if not data:
        return

    text, translations_nr, sentences_nr, images_nr, audios_nr = data
    vocabs = InputParser().read_input(text)
    Downloader.download(vocabs)

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

    # saving and clearing everything up
    inserter.save()
    Downloader.clear_temp_data()

    insertions = inserter.get_count()
    if insertions > 0:
        showInfo("Successfully created %d new cards." % insertions)
    else:
        showInfo("No cards could be created.")


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
    t['qfmt'] = """<p id="english">{{English}}</p>"""
    t['afmt'] = """{{{FrontSide}}\n\n<hr id=answer>\n<p id="german">{{German}}</p>\n<br/>\n<p id="example">{{Examples}}</p>\n<br/>\n{{Media}}"""
    m['css'] = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}

#example {
 color: blue;
}
"""

    # adding template and model
    mm.addTemplate(m, t)
    mm.add(m)

    mm.setCurrent(m)
    mm.save()
    return m


def get_input():
    return InputDialog().run()


class InputDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.input_values = None

        self.setGeometry(20, 20, 540, 480)

        # big input box
        self.input_label = QLabel("Which German Vocabulary do you want to import?")
        self.input_box = QPlainTextEdit(self)

        # buttons
        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.on_import_click)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        # spinboxes
        self.translations_label = QLabel("Translations: ")
        self.translations_spinbox = QSpinBox()
        self.translations_spinbox.setMinimum(1)
        self.translations_spinbox.setMaximum(10)
        self.translations_spinbox.setValue(5)

        self.sentences_label = QLabel("Sentences: ")
        self.sentences_spinbox = QSpinBox()
        self.sentences_spinbox.setMinimum(0)
        self.sentences_spinbox.setMaximum(10)
        self.sentences_spinbox.setValue(3)

        self.images_label = QLabel("Images: ")
        self.images_spinbox = QSpinBox()
        self.images_spinbox.setMinimum(0)
        self.images_spinbox.setMaximum(5)
        self.images_spinbox.setValue(2)

        self.audios_label = QLabel("Audios: ")
        self.audios_spinbox = QSpinBox()
        self.audios_spinbox.setMinimum(0)
        self.audios_spinbox.setMaximum(3)
        self.audios_spinbox.setValue(1)

        # set layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_box)

        self.layout.addWidget(self.translations_label)
        self.layout.addWidget(self.translations_spinbox)

        self.layout.addWidget(self.sentences_label)
        self.layout.addWidget(self.sentences_spinbox)

        self.layout.addWidget(self.images_label)
        self.layout.addWidget(self.images_spinbox)

        self.layout.addWidget(self.audios_label)
        self.layout.addWidget(self.audios_spinbox)

        self.layout.addWidget(self.import_button)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

    def on_import_click(self):
        text = self.input_box.toPlainText()
        if len(text) > 0:

            images = self.images_spinbox.value()
            audios = self.audios_spinbox.value()
            translations = self.translations_spinbox.value()
            sentences = self.sentences_spinbox.value()

            self.input_values = [text, translations, sentences, images, audios]
            self.close()

    def run(self):
        self.exec_()
        return self.input_values


# setup anki gui
##############################################################################

importAction = QAction("Import Input", mw)
importAction.triggered.connect(run)
mw.form.menuTools.addAction(importAction)

