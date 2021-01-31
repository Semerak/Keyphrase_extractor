from Prefix_tree import PrefixTree
import re
import nltk
from nltk.corpus import stopwords


def pre_proc_text(text):
    processed_article = text.lower()
    processed_article = re.sub('[^a-zA-Z]', ' ', processed_article)
    processed_article = re.sub(r'\s+', ' ', processed_article)
    return processed_article


def tokenizer(text):
    all_sentences = nltk.sent_tokenize(text)

    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
    return all_words


def delete_stop_words(all_words):
    bad_words = ["also", "th", "one", "two", "tree", "four", "five", "ten"]
    for i in range(len(all_words)):
        all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
        all_words[i] = [w for w in all_words[i] if w not in bad_words]
    return all_words


def extract_good_words(text):
    proc_text = pre_proc_text(text)
    all_words = tokenizer(proc_text)
    good_words = delete_stop_words(all_words)
    return good_words


def ngram(words, n=1):
    ngram_dic = PrefixTree()
    window = []
    for i in range(n - 1):
        window.insert(0, words[i])
    for word in words[n:]:
        window.insert(0, word)
        ngram_ = "_".join(window[::-1])
        ngram_dic.inc(ngram_)
        window.pop()
    return ngram_dic
