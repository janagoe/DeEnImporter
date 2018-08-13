# -*- coding: utf-8 -*-


class LanguageHandler:

    # 0: ISO 639-3 code of the language which glosbe.com uses
    # 1: english name of the language
    # 2: native name of the language
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
        """
        Creates a dictionary from LanguageHandler.langs.
        :return: the dictionary. The key is the name to display, like "german | deutsch"
        and the value is the language code.
        """
        langs_dict = {}
        for lang in cls.langs:
            key = u"{} | {}".format(lang[1], lang[2])
            value = lang[0]
            langs_dict[key] = value
        return langs_dict



