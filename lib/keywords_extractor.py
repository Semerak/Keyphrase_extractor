from lib.light_model import light_model
from lib.prefix_tree import PrefixTree


def first_n_words(text: str, n=10):
    """Return first n words."""
    key_list = text.split(" ")[:n]
    return [{"word": word} for word in key_list]


def ngram_rank(text: str, n: list = [1]) -> "PrefixTree":
    """Rank words by number of their appearance."""
    from lib.ling import extract_good_words, ngram

    words = extract_good_words(text)
    pref_tree = PrefixTree()
    for n_ in n:
        pref_tree = ngram(words, n_, pref_tree)
    return pref_tree


def evaluate_top(ranked: "PrefixTree", max_keys: int = 10, alpha: float = 0.5) -> list:
    max_val = ranked.list(True)[0]['val']
    return ranked.clear(max_val * alpha).list(True)[:max_keys]


def keywords(text: str, extractor_config: dict) -> list:
    """Extract keywords and return list of words with additional information [{'word': word, ...}...]"""
    try:
        ranked = ngram_rank(text, [1, 2])
        try:
            if extractor_config['light_flag']:
                ranked = light_model(ranked.clear(5))
        except Exception as e:
            print(e)
        return evaluate_top(ranked, extractor_config['max_keys'], extractor_config['alpha'])

    except Exception as e:  # if problem with libraries, return simply first 10 words
        print(e)
        return first_n_words(text)
