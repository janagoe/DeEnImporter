

class AnkiInserter:

    def __init__(self, col, model, from_lang_code, dest_lang_code, image_side):
        self.col = col
        self.deck = self.col.decks.current()
        self.model = model
        self.from_lang_code = from_lang_code
        self.dest_lang_code = dest_lang_code
        self.image_side = image_side  # "from" or "dest"
        self._counter = 0

    def insert(self, translation, sentences, images, from_audios, dest_audios):
        """
        Inserts the content into an Anki node
        :param translation: translation[0] contains the word from the input in the from language,
         translation[1] contains an array of possible translations in the destination language
        :param sentences: array with arrays of one example sentence in the from language and the fitting
        translated sentence in the destination language
        :param from_audios: paths of the audios in the from language
        :param dest_audios: paths of the audios in the destination language
        """

        if translation:
            images_field, from_audio_field, dest_audio_field = self._insert_media(images, from_audios, dest_audios)
            self._insert_note(translation, sentences, images_field, from_audio_field, dest_audio_field)

    def _insert_media(self, images, from_audios, dest_audios):
        """
        Creating links from the file paths, which Anki uses to display the images and to play
        the audios
        :param images: paths of the images
        :param from_audios: paths of the audios in the from language
        :param dest_audios: paths of the audios in the destination language
        :return: strings which will get inserted into the node
        """

        image_links = []
        from_audio_links = []
        dest_audio_links = []

        if images:
            for image in images:
                if image:
                    link = self._path_to_link(image)
                    image_links.append(link)

        if from_audios:
            for from_audio in from_audios:
                if from_audio:
                    link = self._path_to_link(from_audio)
                    from_audio_links.append(link)

        if dest_audios:
            for dest_audio in dest_audios:
                if dest_audio:
                    link = self._path_to_link(dest_audio)
                    dest_audio_links.append(link)

        image_field = " ".join(image_links)
        from_audio_field = " ".join(from_audio_links)
        dest_audio_field = " ".join(dest_audio_links)

        return image_field, from_audio_field, dest_audio_field

    def _path_to_link(self, path):
        """
        Creating a string which Anki uses to display the image / play the audio
        :param path: absolute file path, where the media files are
        :return: link for Anki
        """
        file_name = self.col.media.addFile(unicode(path, 'utf-8'))
        ext = file_name.split(".")[-1].lower()
        if ext == "jpg":
            return '<img src="%s">' % file_name
        else:
            return '[sound:%s]' % file_name

    def _insert_note(self, translation, sentences, images_field, from_audio_field, dest_audio_field):
        """
        Inserting the node with the content into the Anki database, but no dublicates.
        :param translation: translation[0] contains the word from the input in the from language,
         translation[1] contains an array of possible translations in the destination language
        :param sentences: array with arrays of one example sentence in the from language and the fitting
        translated sentence in the destination language
        :param images_field: links for Anki with all images
        :param from_audio_field: links for Anki with the audios in the from language, if the user wants these
        :param dest_audio_field: links for Anki with the audios in the destination language, if the user wants these
        """

        if len(translation[0]) > 0 and len(translation[1]) > 0:

            note = self.col.newNote()
            note_model = note.model()
            note_model['did'] = self.deck['id']
            note_model['id'] = self.model['id']

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

                tags = u"{}-{}-import".format(self.from_lang_code, self.dest_lang_code)
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
        """
        Checking in the Anki database, if a card with the same front already exists.
        :param front: the content on the front of the card
        :return: True if the card is no dublicate, False if the card is a dublicate.
        """
        cards = self.col.findCards(u"FromLang:{}".format(front))
        return len(cards) < 1
