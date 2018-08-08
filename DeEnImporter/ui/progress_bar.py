from aqt.qt import *


# TODO: letting progress bar run in background
class ProgressBar(QDialog):

    def __init__(self, vocabs_nr):
        QDialog.__init__(self)

        self.vocabs_nr = vocabs_nr
        self.step = 0

        self.setWindowTitle("Progress")

        self.bar = QProgressBar(self)
        self.bar.setMaximum(100)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.bar)

        self.setLayout(self.layout)

    def finished_action(self):
        self.step += 50.0 / self.vocabs_nr
        self.bar.setValue(self.step)

        if self.step >= 100:
            self.close()

    def run(self):
        self.exec_()
