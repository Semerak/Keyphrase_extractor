MainPath = "data/"
TextPath = "text/"
KeyPath = "key/"


def keypath() -> str:
    """Return path from root to folder with keywords."""
    return MainPath + KeyPath


def textpath() -> str:
    """Return path from root to folder with texts."""
    return MainPath + TextPath
