# TODO: process bar
# TODO: input form


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
            self._counter += 1

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

        return "<br/>".join(media_links)

    @classmethod
    def _path_to_link(cls, file_name):
        ext = file_name.split(".")[-1].lower()
        if ext == "jpg":
            return '<img src="%s">' % file_name
        else:
            return '[sound:%s]' % file_name

    def _insert_note(self, translation, sentences, media_field=""):
        # TODO: not inserting dublicates

        note = self.col.newNote()
        note_model = note.model()
        note_model['did'] = self.deck['id']
        note_model['id'] = self.model['id']

        german = translation[0].decode('utf-8')

        english = ""
        for t in translation[1]:
            english = "{}<br>{}".format(english, t)

        # example_sentences = u""
        # if sentences:
        #     for s in sentences:
        #         example_sentences = u"{}<br>{}".\
        #             format(example_sentences, s.decode('utf-8'))

        german_examples = ""
        english_examples = ""

        note.fields[0] = english
        note.fields[1] = german
        note.fields[2] = english_examples
        note.fields[3] = german_examples
        note.fields[4] = media_field

        tags = "de-en-importer"
        note.tags = self.col.tags.canonify(self.col.tags.split(tags))
        note_model['tags'] = note.tags

        self.col.addNote(note)

    def save(self):
        self.col.decks.save(self.deck)
        self.col.save()

    def get_count(self):
        return self._counter
