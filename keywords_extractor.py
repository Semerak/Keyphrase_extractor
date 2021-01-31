from ling import extract_good_words, ngram


# def keywords(text):
#     key_list = text.split(" ")[:10]
#     return [{'word': word} for word in key_list]

def keywords(text):
    words = extract_good_words(text)
    pref_tree = ngram(words[0])
    return pref_tree.list(True)[:10]
