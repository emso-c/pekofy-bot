""" STRUCTURE
replies = {
    message_type: {
        message/messages: the message it contains (string/list)
        triggers: trigger words (list)
        trigger_type: whether the text should include all the trigger words
        or just one of them, either 'all' or 'any' (string), defaults to any
        chance: chance to trigger (int), defaults to 100
        include_bot: whether the word 'bot' should be searched in the text too or not, defaults to False
        exact: whether the text should include the *exact* triggers or not, defaults to False
    },
    ...
}
"""

replies = {
    "confused": {
        "message": "eh?",
        "triggers": ["!pekofy","!unpekofy"],
        "trigger_type": "all"
    },
    "hey moona": {
        "message": "#Hey Moona!",
        "chance": 25,
        "triggers": ["moona", "pekora"],
        "trigger_type": "all"
    },
    "pain peko": {
        "message": "[pain-peko.](https://preview.redd.it/dvk3bft2a9l51.jpg?auto=webp&s=d5e53605dc0e99ed55884fc00c9b965c7dd38e7c)",
        "chance": 50,
        "triggers": ["pain", "pain.", "pain...", "pain peko"],
        "trigger_type": "any",
        "exact": True
    },
    "limit reached": {
        "message": "Sorry peko, but I can't pekofy it any further to prevent spam peko. Thank you for your understanding peko.",
    },
    "bot score abuse": {
        "message": "Sorry peko, can't pekofy that due to potential bot score abuse peko.",
        "triggers": ["good bot", "good bot!", "good bot.", "bad bot", "bad bot!", "bad bot."],
        "trigger_type": "any",
        "exact": True
    },
    "no": {
        "message": "[no](https://www.youtube.com/watch?v=3FOe-KNUwb4)",
    },
    "thank": {
        "messages":
            ["Thank you peko", "Thank you peko!", "Thank you peko~", "Arigatou peko!", "Thank you peko!",
            "Thank you peko~", "Arigatou peko!", "Arigatou peko~", "ありがとうぺこ～", "ありがとうぺこ！",
            "Thank you peko!", "Thank you peko~", "Ehehe", "Ehehe",
            "Arigatou peko da ne! [peko~](https://www.youtube.com/watch?v=zOUPxaA6mBM)",
            "[Arigatou peko.](https://www.youtube.com/watch?v=swGNEJ56EFI)"],
        "triggers": ["good", "best", "amazing", "based"],
        "trigger_type": "any",
        "include_bot": True
    },
    "sorry": {
        "messages": ["Sorry peko ; ;", "Sorry peko...", "G-Gomen peko.", "ごめんぺこ・・・"],
        "triggers": ["bad", "worst", "awful", "terrible"],
        "trigger_type": "any",
        "include_bot": True
    },
    "insult": {
        "messages":
            ["Bakatare ga!", "Bakatare ga!", "Bakatare ga!", "Bakatare ga!", "Anta wa baka nano?", "バカたれが！",
           "ばかたれが！", "あんたはバカなの？", "ぺっ", "Go peko yourself!",
           "[Disgusting.](https://streamable.com/6ntf2g)"],
        "triggers": ["insult me peko"],
        "trigger_type": "all",
    },
    "love":{
        "messages":
            ["Thank you guys. Don't cheat on me, okay? [Peko~](https://streamable.com/8gagri)",
            "[Love you](https://streamable.com/dbzfxj) too peko!", "I love you too peko!", "Love you too peko~"],
        "triggers": ["love you","すき","好き"],
        "trigger_type": "any"
    },
    "cute": {
        "messages":
            ["You're cute too peko!", "You're also cute peko!", "You're cute too peko~", "You're also cute peko~", "Ehehe", "あなたもかわいいぺこ！"],
        "triggers": ["cute"],
        "trigger_type": "all",
        "include_bot": True
    },
    "nothing changed": {
        "messages":
            ["Sorry, I couldn\'t pekofy the comment for some reason peko. So here\'s a video of Pekora saying [{}]({}) instead peko.".format(
            title, link) for title, link in {
                "naww": "https://www.youtube.com/watch?v=JNgCFHbPARg",
                "motherf*cker": "https://www.youtube.com/watch?v=1OjQVMiyUMg",
                "oh no jesus": "https://www.youtube.com/watch?v=MwCNEySMNWg",
                "yolo": "https://www.youtube.com/watch?v=MSUckSO-Dsw",
                "ogey rrat": "https://www.youtube.com/watch?v=JacN1MzyeKo",
                "rrat simulator rrrra": "https://www.youtube.com/watch?v=Xr_pKdyeIJo",
                "wao wao waoo!":"https://www.youtube.com/watch?v=O9s_HLql2YM",
                "pardun?":"https://www.youtube.com/watch?v=a3DpRlWdnDw"
            }.items()],
        "triggers": ["NOTHING_CHANGED", "NO_LETTER"],
        "trigger_type": "any",
        "exact": True
    },
    "pekofy": {
        "message": None,
        "triggers": ["!pekofy"],
        "trigger_type": "all"
    },
    "unpekofy": {
        "message": None,
        "triggers": ["!unpekofy"],
        "trigger_type": "all"
    },
}
