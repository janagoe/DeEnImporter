# -*- coding: utf-8 -*-
# from __future__ import unicode_literals


# TODO: process bar
# TODO: input form
# TODO: import model
# TODO: create deck if it doesnt exist


class AnkiInserter:

    def __init__(self, col, model):
        self.col = col
        self.deck = self.col.decks.current()
        self.model = model

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

        german_field = translation[0].decode('utf-8')

        english_field = ""
        for t in translation[1]:
            english_field = "{}<br>{}".format(english_field, t)

        example_sentences = u""
        if sentences:
            for s in sentences:
                example_sentences = u"{}<br>{}".\
                    format(example_sentences, s.decode('utf-8'))

        note.fields[0] = german_field
        note.fields[1] = english_field
        note.fields[2] = example_sentences
        note.fields[3] = media_field

        tags = "de-en-importer"
        note.tags = self.col.tags.canonify(self.col.tags.split(tags))
        note_model['tags'] = note.tags

        self.col.addNote(note)

    def finish(self):
        self.col.decks.save(self.deck)
        self.col.save()
