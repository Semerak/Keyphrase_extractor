def first_n_words(text, n=10):
    key_list = text.split(" ")[:n]
    return [{'word': word} for word in key_list]


def ngram_rank(text):
    from ling import extract_good_words, ngram
    words = extract_good_words(text)
    pref_tree = ngram(words[0])
    return pref_tree.list(True)[:10]


def keywords(text):
    try:
        return ngram_rank(text)

    except:
        return first_n_words(text)
