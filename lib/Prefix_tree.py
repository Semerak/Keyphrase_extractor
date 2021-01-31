import math
import json


class PrefixTree:
    """Prefix tree class with vectors methods and saving to file"""

    def __init__(self, init_dict={}, num=0, crop=0):
        """
        For empty prefix tree leave empty brackets.
        Can be initialized from saved file in dictionary representation.
        """
        if init_dict.get("num") is not None:
            self.num = init_dict.get("num")
            self.mod_val = init_dict.get("mod")
            self.mod_update = True
            self.crop = init_dict.get("crop")
            self.dictionary = self.SimpleDict(init_dict.get("dictionary"))
        else:
            self.dictionary = self.SimpleDict(init_dict)
            if num == 0:
                for word in self.list():
                    num += word["val"]
            self.num = num
            self.crop = crop
            self.mod_val = math.sqrt(sum(w["val"] ** 2 for w in self.list()))
            self.mod_update = True

    class SimpleDict:
        """
        Support class for PrefixTree.
        Simple node in prefix tree.
        """

        def __init__(self, init_dict: dict = {}):
            self.dictionary = {}
            for l in init_dict:
                if l == "":
                    self.dictionary[""] = init_dict[""]
                else:
                    self.dictionary[l] = PrefixTree.SimpleDict(init_dict[l])

        def keys(self):
            """Return all children nodes' letters"""
            return self.dictionary.keys()

        def get(self, letter: str):
            """Return SimpleDict for given letter, or None if no such SimpleDict."""

            return self.dictionary.get(letter)

        def get_add(self, letter: str):
            """Return SimpleDict for given letter, or create new if no such SimpleDict."""

            if letter == "":
                return self.dictionary.get("")

            if self.dictionary.get(letter) is None:
                self.dictionary[letter] = PrefixTree.SimpleDict()

            return self.dictionary.get(letter)

        def include(self, letter: str) -> bool:
            """Check if there is given letter."""

            return not (self.dictionary.get(letter) is None)

        def add(self, val: object):
            """Add given value in this node."""

            if self.dictionary.get("") is None:
                self.dictionary[""] = []

            self.dictionary[""].append(val)

        def inc(self, val: float = 1):
            """Increment value in this node by val, or by 1 if not specified."""
            if self.dictionary.get("") is None:
                self.dictionary[""] = val
            else:
                self.dictionary[""] += val

        def value(self, val: object):
            """Set value in this node"""
            self.dictionary[""] = val

        def clear(self, new_dic, word, val):
            """Add to new_dic word if value > val."""
            if not (self.dictionary.get("") is None):

                if self.dictionary.get("") > val:
                    new_dic.value(word, self.dictionary.get(""))

            for l in self.dictionary:
                if l != "":
                    self.dictionary[l].clear(new_dic, word + l, val)

        def list(self, word: str) -> list:
            """Generate list of words."""
            list_data = []
            val = self.dictionary.get("")

            if val is not None:
                list_data.append({"word": word, "val": val})

            for letter in self.dictionary:
                if letter != "":
                    list_data.extend(self.dictionary[letter].list(word + letter))

            return list_data

        def json(self) -> dict:
            """Generate dictionary representation."""
            json_dic = {}
            for l in self.dictionary:
                if l == "":
                    json_dic[""] = self.dictionary[""]
                else:
                    json_dic[l] = self.dictionary[l].json()
            return json_dic

    def inc(self, word: str, val: float = 1):
        """Increment value for given word"""
        dic = self.dictionary

        for letter in word:
            dic = dic.get_add(letter)
        dic.inc(val)

        self.num += val
        self.mod_update = False

    def mod(self, check=False) -> float:
        """Return module as if prefix tree is a vector"""
        if check:
            self.mod_val = math.sqrt(sum(w["val"] ** 2 for w in self.list()))
            self.mod_update = True
        else:
            if not self.mod_update:
                self.mod_val = math.sqrt(sum(w["val"] ** 2 for w in self.list()))
                self.mod_update = True

        return self.mod_val

    def value(self, word: str, val: object):
        """Add new value to given word"""
        dic = self.dictionary

        for letter in word:
            dic = dic.get_add(letter)

        dic.value(val)
        self.mod_update = False

    def get(self, word: str) -> object:
        """Return value by the word, or None if there is no such word"""
        dic = self.dictionary

        for letter in word:
            dic = dic.get(letter)

            if dic is None:
                return None

        return dic.get("")

    def clear(self, val: float) -> "PrefixTree":
        """Return new PrefixTree without elements, with values <= val."""
        new_dic = PrefixTree()
        self.dictionary.clear(new_dic, "", val)

        new_dic.num = self.num
        new_dic.crop = max(self.crop, val)
        return new_dic

    def list(self, sort=False) -> list:
        """Return list of all words in prefix tree [{"word" : word, "val" : val}, ...]."""
        list_data = []
        word = ""

        for letter in self.dictionary.keys():
            if letter == "":
                list_data.append({"word": word, "val": self.dictionary.get(letter)})
            else:
                list_data.extend(self.dictionary.get(letter).list(letter))

        if sort:
            return sorted(list_data, key=lambda word: word["val"], reverse=True)

        return list_data

    def json(self) -> dict:
        """Return dictionary representation of all information in this prefix tree"""
        data = {
            "num": self.num,
            "mod": self.mod(),
            "crop": self.crop,
            "dictionary": self.dictionary.json(),
        }
        return data

    def save(self, path: str):
        """Save this object as json file with given path"""
        f = open(path, "w")
        f.write(json.dumps(self.json()))
        f.close()

    def copy(self) -> "PrefixTree":
        """Create a copy."""
        return PrefixTree(self.json())

    def norm(self, new_vector=False) -> "PrefixTree":
        """Normalize values as if it is vector"""
        mod = self.mod()

        if new_vector:

            new_vector = PrefixTree()

            for word in self.list():
                new_vector.value(word["word"], word["val"] / mod)

            new_vector.num = self.num
            new_vector.crop = self.crop
            new_vector.mod_val = 1

            return new_vector

        else:

            for word in self.list():
                self.value(word["word"], word["val"] / mod)

            self.mod_val = 1

            return self
