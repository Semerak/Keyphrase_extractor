import wikipedia


def summary(word) -> str:
    """Return information about word from wikipedia."""
    result = ""

    try:
        result = wikipedia.summary(word, chars=100, auto_suggest=False)

    except wikipedia.exceptions.DisambiguationError:
        result = "Disambiguation: " + " ,".join(wikipedia.search(word, results=4))

    except:
        result = "No page"

    return result


def list_summary(table) -> list:
    """Add to table of words information from wikipedia."""
    for line in table:
        line['wiki'] = summary(line['word'])
    return table

