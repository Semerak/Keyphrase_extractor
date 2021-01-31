import wikipedia


def summary(word):
    result = ""
    try:
        result = wikipedia.summary(word, chars=100, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError:
        result = "Disambiguation: " + " ,".join(wikipedia.search(word, results=4))
    except:
        result = "No page"
    return result


def list_summary(table):
    return [{'word': line['word'], 'wiki': summary(line['word'])} for line in table]

