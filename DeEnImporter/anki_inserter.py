from aqt.utils import showInfo


class AnkiInserter:

    def __init__(self, col, model, from_lang, dest_lang, image_side):
        self.col = col
        self.deck = self.col.decks.current()
        self.model = model
        self.from_lang = from_lang
        self.dest_lang = dest_lang
        self.image_side = image_side
        self._counter = 0

    def insert(self, translation, sentences, images, audios):
        if translation:
            images_field, from_audio_field, dest_audio_field = self._insert_media(images, audios)
            self._insert_note(translation, sentences, images_field, from_audio_field, dest_audio_field)

    def _insert_media(self, images, audios):
        image_links = []
        from_audio_links = []
        dest_audio_links = []

        if images:
            for image in images:
                if image:
                    link = self._path_to_link(image)
                    image_links.append(link)

        if audios:
            for from_audio in audios[0]:
                if from_audio:
                    link = self._path_to_link(from_audio)
                    from_audio_links.append(link)

            for dest_audio in audios[1]:
                if dest_audio:
                    link = self._path_to_link(dest_audio)
                    dest_audio_links.append(link)

        image_field = " ".join(image_links)
        from_audio_field = " ".join(from_audio_links)
        dest_audio_field = " ".join(dest_audio_links)

        return image_field, from_audio_field, dest_audio_field

    def _path_to_link(self, path):
        file_name = self.col.media.addFile(unicode(path, 'utf-8'))
        ext = file_name.split(".")[-1].lower()
        if ext == "jpg":
            return '<img src="%s">' % file_name
        else:
            return '[sound:%s]' % file_name

    def _insert_note(self, translation, sentences, images_field, from_audio_field, dest_audio_field):
        note = self.col.newNote()
        note_model = note.model()
        note_model['did'] = self.deck['id']
        note_model['id'] = self.model['id']

        if len(translation[0]) > 0 and len(translation[1]) > 0:
            from_text = translation[0]
            if self.is_no_dublicate(from_text):

                dest_text = translation[1][0]
                for i in range(1, len(translation[1])):
                    dest_text = u"{}<br>{}".format(dest_text, translation[1][i])

                from_examples = u""
                dest_examples = u""
                if sentences and len(sentences) > 0:
                    from_examples = u"{}".format(sentences[0][0])
                    dest_examples = u"{}".format(sentences[0][1])
                    for i in range(1, len(sentences)):
                        from_examples = u"{}<br>{}".format(from_examples, sentences[i][0])
                        dest_examples = u"{}<br>{}".format(dest_examples, sentences[i][1])

                note.fields[0] = from_text
                note.fields[1] = dest_text
                note.fields[2] = from_examples
                note.fields[3] = dest_examples
                note.fields[4] = from_audio_field
                note.fields[5] = dest_audio_field

                if self.image_side == "from":
                    note.fields[6] = images_field
                else:
                    note.fields[7] = images_field

                tags = u"{}-{}-import".format(self.from_lang, self.dest_lang)
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
