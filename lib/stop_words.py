from flask import current_app

from lib.prefix_tree import PrefixTree
from nltk.corpus import stopwords


class StopWordsSingleton(object):
    sw_list = PrefixTree()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(StopWordsSingleton, cls).__new__(cls)
            for word in stopwords.words("english"):
                cls.sw_list.value(word, True)
            for word in current_app.config["BAD_WORDS"]:
                cls.sw_list.value(word, True)
        return cls.instance


def is_stop_word(word: str) -> bool:
    """Return if a word is a stop word."""
    stop_words = StopWordsSingleton()
    return stop_words.sw_list.get(word) is True
