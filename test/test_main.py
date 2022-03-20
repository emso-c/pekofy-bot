### WIP ###

#NOTE: Signing in to a reddit account is necessary to run all tests (see auth.py)
import unittest
from unittest.case import skipIf
from main import (
    already_replied_to,
    is_anti,
    is_top_level,
    is_triggering,
    notify_author,
    passed_limit,
    reply_f,
    praw,
)
import main
from auth import REDDIT

class TestMain(unittest.TestCase):

    def setUp(self):
        main.logger.disabled = True
        main.BOT_NAME = "pekofy_bot"

    def tearDown(self):
        pass

    def test_reply_f(self):
        # pekofy

        # unpekofy

        # nothing changed

        # cute

        # love

        # insult

        # sorry

        # thank

        # no

        # bot score abuse

        # limit reached

        # pain peko

        # hey moona

        # confused

        pass

    def test_already_replied_to(self):
        # TODO reduce dependency
        # Right now it's vulnerable to reply changes, comment deletions and edits
        comment = praw.models.Comment
        
        ### pekofy ###
        # comment
        self.assertTrue(already_replied_to(comment(REDDIT, "hf8ump4"), "pekofy"))
        # comment (command and reply are both edited)
        self.assertFalse(already_replied_to(comment(REDDIT, "hb6x17z"), "pekofy"))
        # top level comment
        self.assertTrue(already_replied_to(comment(REDDIT, "hff0et8"), "pekofy"))
        # top level comment (command edited)
        self.assertTrue(already_replied_to(comment(REDDIT, "hfcb87u"), "pekofy"))

        ### unpekofy ###
        # there are no replies to unpekofy command

        ### nothing changed ###
        #TODO find an example of the new reply (it's not in production as I'm writing this test)
        #self.assertTrue(already_replied_to(comment(REDDIT, "TODO"), "nothing changed", False))
        

        ### cute ###
        self.assertTrue(already_replied_to(comment(REDDIT, "hb89b9c"), "cute"))

        ### love ###

        ### insult ###

        ### sorry ###

        ### thank ###

        ### no ###

        ### bot score abuse ###

        ### limit reached ###

        ### pain peko ###

        ### hey moona ###

        ### confused ###
    
    def test_is_triggering(self):
        # pekofy
        self.assertTrue(is_triggering("!pekofy","pekofy"))
        self.assertFalse(is_triggering("!Pekofy","pekofy"))

        # unpekofy
        self.assertTrue(is_triggering("!unpekofy","unpekofy"))
        self.assertFalse(is_triggering("!pekofy","unpekofy"))

        # nothing changed
        self.assertTrue(is_triggering("NOTHING_CHANGED","nothing changed"))
        self.assertTrue(is_triggering("NO_LETTER","nothing changed"))
        self.assertFalse(is_triggering("no letter","nothing changed"))
        self.assertFalse(is_triggering("NOTHING_CHANGED NO_LETTER","nothing changed"))

        # cute
        self.assertTrue(is_triggering("cute bot","cute"))
        self.assertFalse(is_triggering("cute","cute"))

        # love
        self.assertTrue(is_triggering("love you","love"))
        self.assertTrue(is_triggering("すき","love"))
        self.assertFalse(is_triggering("love","love"))

        # insult
        self.assertTrue(is_triggering("insult me peko","insult"))
        self.assertFalse(is_triggering("insult me","insult"))

        # sorry
        self.assertTrue(is_triggering("bad bot","sorry"))
        self.assertTrue(is_triggering("unbased bot","sorry"))
        self.assertFalse(is_triggering("bad","sorry"))

        # thank
        self.assertTrue(is_triggering("good bot","thank"))
        self.assertFalse(is_triggering("good","thank"))

        # no
        # no such implementation for "no", it's evaluated run-time

        # bot score abuse
        # no such implementation for "bot score abuse", it's evaluated run-time

        # limit reached
        # no such implementation for "limit reached", it's evaluated run-time

        # pain peko
        self.assertTrue(is_triggering("pain","pain peko"))
        self.assertFalse(is_triggering("pien","pain peko"))

        # hey moona
        self.assertTrue(is_triggering("moona and pekora","hey moona"))
        self.assertFalse(is_triggering("moona","hey moona"))
        self.assertFalse(is_triggering("pekora","hey moona"))

        # confused
        self.assertTrue(is_triggering("!pekofy !unpekofy","confused"))
        self.assertFalse(is_triggering("!pekofy","confused"))
        self.assertFalse(is_triggering("!unpekofy","confused"))

        # copypasta
        self.assertTrue(is_triggering(
            "So as a joke, I went to my friend's house wearing Pekora's wig and clothes. I could barely stop my laughter as he went as red as a tomato and looked at me from head to toe with a bit of drool in his mouth. The way he stared made me feel a bit funny too, but I decided to tease him more by taking off my clothes. He asked me, \"Are you serious?\" and I said \"Yep peko.\" He went silent for what seemed like forever, so I asked him, \"What's the matter peko?\" He said he's confused, but then his boner got really hard, which made me take off his clothes. I expected him to scream, \"Stop!\" as I kissed him and stroked his cock, but he instead shouted \"Oh God, Pekora!\" which made me get a boner myself. Before I knew it, I was blowing him for the first time till he came. His semen was so thick, it got stuck inside my throat no matter how hard I swallowed. He then said, \"I want to fuck you now!\" and seeing that we've already gone that far and we were both naked, I obliged. A few hours later, the jerk went all pale and said to me \"Why did we do that? Now I'm not fucking straight.\" But he still looked so cute all confused like that, so I took pity on him and reassured while wiping his cum off my face, \"Let's just pretend I'm still Pekora.\"",
            "pekora copypasta"
        ))
        self.assertFalse(is_triggering("So as a joke, I went to my friend's house wearing Pekora's wig and clothes.","pekora copypasta"))

    @skipIf(not "REDDIT" in globals(), "Not authorized")
    def test_passed_limit(self):
        self.assertTrue(passed_limit(praw.models.Comment(REDDIT, "hf8vugd"), limit=2))
        self.assertFalse(passed_limit(praw.models.Comment(REDDIT, "hf8ump4"), limit=2))

    @skipIf(not "REDDIT" in globals(), "Not authorized")
    def test_is_top_level(self):
        self.assertTrue(is_top_level(praw.models.Comment(REDDIT, "gbrxy6t")))
        self.assertFalse(is_anti(praw.models.Comment(REDDIT, "gbs48uz")))

    @skipIf(not "REDDIT" in globals(), "Not authorized")
    def test_is_anti(self):
        self.assertTrue(is_anti(praw.models.Comment(REDDIT, "gbsh3ng")))
        self.assertFalse(is_anti(praw.models.Comment(REDDIT, "gbs48uz")))


if __name__ == "__main__":  
    unittest.main()