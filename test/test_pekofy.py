from typing import Tuple
import unittest
from pekofy import pekofy
from enum import Enum

def test_for(test_cases:list[Tuple]) -> Tuple[str, str]:
    for tt in test_cases:
        text, expected = tt
        result = pekofy(text)
        yield result, expected

class TestPekofy(unittest.TestCase):
    def setUp(self):
        class TestCases(Enum):
            BASIC = [
                (
                    "kon",
                    "kon peko"
                ),(
                    "war crimes",
                    "war crimes peko"
                )
            ]
            PUNCTUATION = [
                (
                    "violence.",
                    "violence peko."
                ),(
                    "hello...",
                    "hello peko..."
                ),(
                    "dope, based, superlit",
                    "dope, based, superlit peko",
                ),(
                    "hello~!?!?",
                    "hello peko~!?!?"
                ),(
                    "hello! world~",
                    "hello peko! world peko~"
                ),(
                    "...",
                    "NO_LETTER"
                ),(
                    "version 1.1",
                    "version 1.1 peko"
                )
            ]
            LINE_BREAK = [
                (
                    "hello\nhello",
                    "hello peko\nhello peko"
                ),(
                    "hello...\nhello...\n",
                    "hello peko...\nhello peko...\n",
                ),(
                    "hello...\n\n\n\nhello...",
                    "hello peko...\n\n\n\nhello peko...",
                ),
                (
                    "\n",
                    "NO_LETTER"
                )
            ]
            URL = [
                (
                    "[nice video](https://www.youtube.com/watch?v=4q1B06m4_Lk)",
                    "[nice video peko](https://www.youtube.com/watch?v=4q1B06m4_Lk)",
                ),(
                    "[nice. video.](https://www.youtube.com/watch?v=4q1B06m4_Lk)",
                    "[nice peko. video peko.](https://www.youtube.com/watch?v=4q1B06m4_Lk)",
                ),(
                    "text [nice video](https://www.youtube.com/watch?v=4q1B06m4_Lk) text",
                    "text [nice video peko](https://www.youtube.com/watch?v=4q1B06m4_Lk) text peko",
                    #"text [nice video](https://www.youtube.com/watch?v=4q1B06m4_Lk) text peko", # TODO convert to this
                )
            ]
            EMOJI = [
                (
                    "I forgor 💀",
                    "I forgor peko 💀"
                ),(
                    "peko 🥕 peko",
                    "peko 🥕 peko peko"
                ),(
                    "🥕",
                    "NO_LETTER"
                )
            ]
            EMPTY = [
                (
                    "",
                    "NO_LETTER"
                ),(
                    " ",
                    "NO_LETTER"
                ),(
                    "​", #U+200B
                    "NO_LETTER"
                )
            ]
            REDDIT_MARKDOWN = [
                (
                    ">!spoilers!<",
                    ">!spoilers peko!<",
                ),(
                    "_italic_ or *italic*",
                    "_italic_ or *italic peko*"
                ),(
                    "__bold__ or **bold**",
                    "__bold__ or **bold peko**",
                ),(
                    "___bold-italic___ or ***bold-italic***",
                    "___bold-italic___ or ***bold-italic peko***",
                ),(
                    "~~strikethrough~~",
                    "~~strikethrough peko~~",
                ),(
                    "^superscript or ^(superscript)",
                    "^superscript or ^(superscript peko)",
                ),(
                    "`code`",
                    "`code peko`",
                )
            ]
            JP_BASIC = [
                (
                    "草",
                    "草ぺこ"
                ),(
                    "にんじん",
                    "にんじんぺこ"
                )
            ]
            JP_PUNCTUATION = [
                (
                    "おめでとう～！",
                    "おめでとうぺこ～！",
                ),(
                    "！",
                    "NOTHING_CHANGED"
                )
            ]
        self.test_cases = TestCases

    def test_basic(self):
        for res, exp in test_for(self.test_cases.BASIC.value):
            self.assertEqual(res, exp)

    def test_punctuation(self):
        for res, exp in test_for(self.test_cases.PUNCTUATION.value):
            self.assertEqual(res, exp)

    def test_line_break(self):
        for res, exp in test_for(self.test_cases.LINE_BREAK.value):
            self.assertEqual(res, exp)

    def test_url(self):
        for res, exp in test_for(self.test_cases.URL.value):
            self.assertEqual(res, exp)
    
    def test_emoji(self):
        for res, exp in test_for(self.test_cases.EMOJI.value):
            self.assertEqual(res, exp)

    def test_empty(self):
        for res, exp in test_for(self.test_cases.EMPTY.value):
            self.assertEqual(res, exp)

    def test_reddit_markdown(self):
        for res, exp in test_for(self.test_cases.REDDIT_MARKDOWN.value):
            self.assertEqual(res, exp)

    def test_jp_basic(self):
        for res, exp in test_for(self.test_cases.JP_BASIC.value):
            self.assertEqual(res, exp)

    def test_jp_punctuation(self):
        for res, exp in test_for(self.test_cases.JP_PUNCTUATION.value):
            self.assertEqual(res, exp)


if __name__ == "__main__":  
    unittest.main()