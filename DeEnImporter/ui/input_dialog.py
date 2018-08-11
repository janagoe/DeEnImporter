from aqt.qt import *
from aqt.utils import showInfo
from DeEnImporter.language_handler import LanguageHandler

class InputDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.input_values = None
        self._init_ui()
        self._set_layout()

    def _init_ui(self):
        self.setGeometry(20, 20, 540, 540)

        self._init_input()
        self._init_lang_preferences()
        self._init_spinboxes()
        self._init_buttons()

    def _init_input(self):
        self.input_label = QLabel("Insert new words here:")
        self.input_box = QPlainTextEdit(self)

    def _init_lang_preferences(self):
        self.from_box = QComboBox()
        self.dest_box = QComboBox()

        self.from_box_label = QLabel("Translate from...")
        self.dest_box_label = QLabel("to...")

        self._add_languages(self.from_box, self.dest_box)

        self.from_audio_checkbox = QCheckBox("with Audio Samples")
        self.dest_audio_checkbox = QCheckBox("with Audio Samples")

    def _init_spinboxes(self):
        self.translations_label = QLabel("Translations: ")
        self.translations_spinbox = QSpinBox()
        self.translations_spinbox.setMinimum(1)
        self.translations_spinbox.setMaximum(10)
        self.translations_spinbox.setValue(5)

        self.sentences_label = QLabel("Sentences: ")
        self.sentences_spinbox = QSpinBox()
        self.sentences_spinbox.setMinimum(0)
        self.sentences_spinbox.setMaximum(10)
        self.sentences_spinbox.setValue(2)

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

    def _init_buttons(self):
        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.on_import_click)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

    def _set_layout(self):
        self.layout = QVBoxLayout()

        self._set_input()
        self.layout.addWidget(QLabel("\n"))
        self._set_lang_preferences()
        self.layout.addWidget(QLabel("\n"))
        self._set_spinboxes()
        self.layout.addWidget(QLabel("\n"))
        self._set_buttons()

        self.setLayout(self.layout)

    def _set_input(self):
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_box)

    def _set_lang_preferences(self):
        self.from_lang_layout = QHBoxLayout()
        self.dest_lang_layout = QHBoxLayout()

        self.from_lang_layout.addWidget(self.from_box_label)
        self.from_lang_layout.addWidget(self.from_box)
        self.from_lang_layout.addWidget(self.from_audio_checkbox)

        self.dest_lang_layout.addWidget(self.dest_box_label)
        self.dest_lang_layout.addWidget(self.dest_box)
        self.dest_lang_layout.addWidget(self.dest_audio_checkbox)

        self.layout.addLayout(self.from_lang_layout)
        self.layout.addLayout(self.dest_lang_layout)

    def _set_spinboxes(self):
        self.spinbox_layout_1 = QHBoxLayout()
        self.spinbox_layout_2 = QHBoxLayout()

        self.spinbox_layout_1.addWidget(self.translations_label)
        self.spinbox_layout_1.addWidget(self.translations_spinbox)

        self.spinbox_layout_1.addWidget(self.sentences_label)
        self.spinbox_layout_1.addWidget(self.sentences_spinbox)

        self.spinbox_layout_2.addWidget(self.images_label)
        self.spinbox_layout_2.addWidget(self.images_spinbox)

        self.spinbox_layout_2.addWidget(self.audios_label)
        self.spinbox_layout_2.addWidget(self.audios_spinbox)

        self.layout.addLayout(self.spinbox_layout_1)
        self.layout.addLayout(self.spinbox_layout_2)

    def _set_buttons(self):
        self.button_layout = QHBoxLayout()

        self.button_layout.addWidget(self.import_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

    def _add_languages(self, box1, box2):
        self.langs = LanguageHandler.langs_to_dict()
        keys = self.langs.keys()
        box1.addItems(keys)
        box2.addItems(keys)

        # set default choices
        box1.setCurrentIndex(keys.index(u'German / Deutsch'))
        box2.setCurrentIndex(keys.index(u'English / English'))

    def _get_langs(self):

        from_key = self.from_box.currentText()
        dest_key = self.dest_box.currentText()

        from_value = self.langs[from_key]
        dest_value = self.langs[dest_key]

        return from_value, dest_value

    def _get_audio_langs(self):
        from_audio, dest_audio = False, False

        if self.from_audio_checkbox.isChecked():
            from_audio = True
        if self.dest_audio_checkbox.isChecked():
            dest_audio = True

        return from_audio, dest_audio

    def on_import_click(self):
        text = self.input_box.toPlainText()
        if len(text) > 0:

            images = self.images_spinbox.value()
            audios = self.audios_spinbox.value()
            translations = self.translations_spinbox.value()
            sentences = self.sentences_spinbox.value()

            from_lang, dest_lang = self._get_langs()
            from_audio, dest_audio = self._get_audio_langs()

            self.input_values = [text, translations, sentences, images, audios, from_lang, dest_lang, from_audio, dest_audio]
            self.close()

    def run(self):
        self.exec_()
        return self.input_values
