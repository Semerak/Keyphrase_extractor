from lib.prefix_tree import PrefixTree
import numpy as np


class GloVeSingleton(object):
    emb_dict = PrefixTree()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GloVeSingleton, cls).__new__(cls)
            with open("lib/GloVe/glove.6B.300d.txt", 'r', encoding="utf-8") as f:
                print("Downloading GloVe dictionary")
                i=0
                for line in f:
                    i += 1
                    if i % 10000 == 0:
                        print(i)
                    values = line.split()
                    word = values[0]
                    vector = np.asarray(values[1:], "float32")
                    cls.emb_dict.value(word, vector)
        return cls.instance


def get_embedding_vector(word: str):
    """Return embedding vector of word from GloVe."""
    glove = GloVeSingleton()
    return glove.emb_dict.get(word)


