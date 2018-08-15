# -*- coding: utf-8 -*-


class LanguageHandler:

    # 0: ISO 639-3 code of the language which glosbe.com uses
    # 1: english name of the language
    langs = [
        [u"eng", u"english"],
        [u"deu", u"german"],
        [u"fra", u"french"],
        [u"spa", u"spanish"],
        [u"jpn", u"japanese"],
        [u"rus", u"russian"],
        [u"zh", u"chinese"],
        [u"pol", u"polish"],
        [u"ita", u"italian"],
        [u"ces", u"czech"],
        [u"aao", u"arabic"],
        [u"por", u"portuguese"],
        [u"swe", u"swedish"],
        [u"hrv", u"croatian"],
        [u"fin", u"finnish"],
        [u"hin", u"hindi"],
        [u"hun", u"hungarian"],
        [u"vie", u"vietnamese"],
        [u"tur", u"turkish"],
    ]

    @classmethod
    def langs_to_dict(cls):
        """
        Creates a dictionary from LanguageHandler.langs.
        :return: the dictionary. The key is the name to display,
        and the value is the language code.
        """
        langs_dict = {}
        for lang in cls.langs:
            key = lang[1]
            value = lang[0]
            langs_dict[key] = value
        return langs_dict



