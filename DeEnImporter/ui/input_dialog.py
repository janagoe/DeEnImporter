from aqt.qt import *

class InputDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.input_values = None
        self.initUI()

    def initUI(self):
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
