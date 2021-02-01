from lib.prefix_tree import PrefixTree
import re
import nltk
from lib.stop_words import is_stop_word



def pre_proc_text(text: str) -> str:
    """Preprocess given text."""
    processed_article = text.lower()
    processed_article = re.sub("[^a-zA-Z]", " ", processed_article)
    processed_article = re.sub(r"\s+", " ", processed_article)
    return processed_article


def tokenizer(text: str) -> list:
    """Return list (sentences) of list (words)"""
    all_sentences = nltk.sent_tokenize(text)
    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]

    return all_words


def delete_stop_words(all_words: list) -> list:
    """From a list delete stop words."""
    good_words = []
    for word in all_words:
        if not(is_stop_word(word)):
            good_words.append(word)
    return good_words


def extract_good_words(text: str) -> list:
    """
    From a text return a list of meaningful words.
    Firstly do a preprocessing for text, then delete stop words.
    """
    proc_text = pre_proc_text(text)
    all_words = tokenizer(proc_text)[0]
    good_words = delete_stop_words(all_words)
    return good_words


def ngram(words: list, n: int = 1, ngram_dic : "PrefixTree" = PrefixTree()) -> "PrefixTree":
    """Generate a PrefixTree with ngrams with given n."""
    window = []
    for i in range(n - 1):
        window.insert(0, words[i])
    for word in words[n:]:
        window.insert(0, word)
        ngram_ = "_".join(window[::-1])
        ngram_dic.inc(ngram_)
        window.pop()
    return ngram_dic
