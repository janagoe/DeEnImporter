# -*- coding: utf-8 -*-

class LanguageHandler:

    langs = [
        [u"eng", u"english", u"english"],
        [u"deu", u"german", u"deutsch"],
        [u"fra", u"french", u"français"],
        [u"spa", u"spanish", u"español"],
        [u"jpn", u"japanese", u"日本の"],
        [u"rus", u"russian", u"русский"],
        [u"zh", u"chinese", u"中国"],
        [u"pol", u"polish", u"polski"],
        [u"ita", u"italian", u"italiano"],
        [u"ces", u"czech", u"český"],
        [u"aao", u"arabic", u"عربي"],
        [u"por", u"portuguese", u"português"],
    ]

    @classmethod
    def langs_to_dict(cls):
        langs_dict = {}
        for lang in cls.langs:
            key = u"{} | {}".format(lang[1], lang[2])
            value = lang[0]
            langs_dict[key] = value
        return langs_dict



