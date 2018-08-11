# -*- coding: utf-8 -*-


class LanguageHandler:

    langs = [
        [u"eng", u"English", u"English"],
        [u"deu", u"German", u"Deutsch"],
        [u"fra", u"French", u"Français"],
        [u"spa", u"Spanish", u"Español"]
    ]

    @classmethod
    def langs_to_dict(cls):
        langs_dict = {}
        for lang in cls.langs:
            key = u"{} / {}".format(lang[1], lang[2])
            value = lang[0]
            langs_dict[key] = value
        return langs_dict



