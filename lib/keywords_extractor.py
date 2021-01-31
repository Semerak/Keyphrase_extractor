def first_n_words(text: str, n=10):
    """Return first n words."""
    key_list = text.split(" ")[:n]
    return [{'word': word} for word in key_list]


def ngram_rank(text: str) -> list:
    """Rank words by number of their appearance."""
    from lib.ling import extract_good_words, ngram

    words = extract_good_words(text)
    pref_tree = ngram(words[0])
    return pref_tree.list(True)[:10]


def keywords(text: str) -> list:
    """Extract keywords and return list of words with additional information [{'word': word, ...}...]"""
    try:
        return ngram_rank(text)

    except Exception as e:  # if problem with libraries, return simply first 10 words
        print(e)
        return first_n_words(text)
