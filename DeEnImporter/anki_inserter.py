
class AnkiInserter:

    def __init__(self, col, model):
        self.col = col
        self.deck = self.col.decks.current()
        self.model = model
        self._counter = 0

    def insert(self, translation, sentences, images, audios):
        if translation:
            media_field = self._insert_media(images, audios)
            self._insert_note(translation, sentences, media_field)

    def _insert_media(self, images, audios):
        media_links = []

        srcs = []
        if images:
            srcs += images
        if audios:
            srcs += audios

        for path in srcs:
            if path:
                file_name = self.col.media.addFile(unicode(path, 'utf-8'))
                link = self._path_to_link(file_name)
                media_links.append(link)

        return " ".join(media_links)

    @classmethod
    def _path_to_link(cls, file_name):
        ext = file_name.split(".")[-1].lower()
        if ext == "jpg":
            return '<img src="%s">' % file_name
        else:
            return '[sound:%s]' % file_name

    def _insert_note(self, translation, sentences, media_field=""):
        note = self.col.newNote()
        note_model = note.model()
        note_model['did'] = self.deck['id']
        note_model['id'] = self.model['id']

        if len(translation[0]) > 0 and len(translation[1]) > 0:

            german = translation[0]

            if self.is_no_dublicate(german):

                english = translation[1][0]
                for i in range(1, len(translation[1])):
                    english = u"{}<br>{}".format(english, translation[1][i])

                german_examples = u""
                english_examples = u""
                if sentences and len(sentences) > 0:
                    german_examples = u"{}".format(sentences[0][0])
                    english_examples = u"{}".format(sentences[0][1])
                    for i in range(1, len(sentences)):
                        german_examples = u"{}<br>{}".format(german_examples, sentences[i][0])
                        english_examples = u"{}<br>{}".format(english_examples, sentences[i][1])

                note.fields[0] = german
                note.fields[1] = english
                note.fields[2] = german_examples
                note.fields[3] = english_examples
                note.fields[4] = media_field

                tags = "de-en-importer"
                note.tags = self.col.tags.canonify(self.col.tags.split(tags))
                note_model['tags'] = note.tags

                self.col.addNote(note)
                self._counter += 1

    def save(self):
        self.col.decks.save(self.deck)
        self.col.save()

    def get_count(self):
        return self._counter

    def is_no_dublicate(self, front):
        cards = self.col.findCards(u"German:{}".format(front))
        return len(cards) < 1
