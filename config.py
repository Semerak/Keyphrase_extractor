import os
from typing import List


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    BAD_WORDS: List[str] = ["also", "th", "one", "two", "tree", "four", "five", "ten"]

    @property
    def DATA_PATH(self) -> str:
        return os.path.join(self.BASE_DIR, "data")

    @property
    def KEY_PATH(self) -> str:
        return os.path.join(self.DATA_PATH, "key")

    @property
    def TEXT_PATH(self) -> str:
        return os.path.join(self.DATA_PATH, "text")
