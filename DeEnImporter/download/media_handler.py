import os


class MediaHandler:

    @classmethod
    def image_file_name(cls, vocab):
        return os.path.join(os.getcwd(), vocab)

    @classmethod
    def audio_file_name(cls, vocab):
        return os.path.join(os.getcwd(), vocab)
