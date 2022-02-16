""" STRUCTURE
replies = {
    reply_type: {
        messages (list): the messages it contains
        triggers (list): trigger words or phrases
        trigger_type (string): whether the text should include all the trigger words
        or just one of them, either 'all' or 'any'
        chance (int): chance to trigger between 0 and 100
        include_bot (bool): whether the word 'bot' should be included in the text or not
        exact (bool): whether the text should include the *exact* triggers or not
    },
    ...
}
"""

REPLIES = {
    "confused": {
        "messages": ["eh?"],
        "triggers": ["!pekofy", "!unpekofy"],
        "trigger_type": "all",
        "chance": 100,
        "exact": False,
        "include_bot": False,
    },
    "hey moona": {
        "messages": ["#Hey Moona!"],
        "chance": 25,
        "triggers": ["moona", "pekora"],
        "trigger_type": "all",
        "include_bot": False,
        "exact": False,
    },
    "pain peko": {
        "messages": ["[pain-peko.](https://preview.redd.it/dvk3bft2a9l51.jpg?auto=webp&s=d5e53605dc0e99ed55884fc00c9b965c7dd38e7c)"],
        "triggers": ["pain",  "pain.", "pain...", "pain peko"],
        "trigger_type": "any",
        "chance": 50,
        "exact": True,
        "include_bot": False,
    },
    "limit reached": {
        "messages": ["Sorry, but I can't pekofy it any further to prevent spam peko. Thank you for your understanding peko."],
        "triggers": [],  # will be evaluated run-time
        "trigger_type": "any",
        "chance": 100,
        "exact": False,
        "include_bot": False,
    },
    "bot score abuse": {
        "messages": ["Sorry, but I can't pekofy that due to potential bot score abuse peko."],
        "triggers": ["good bot", "good bot!", "good bot.", "bad bot", "bad bot!", "bad bot."],
        "trigger_type": "any",
        "exact": True,
        "chance": 100,
        "include_bot": False,
    },
    "no": {
        "messages": ["[no](https://www.youtube.com/watch?v=3FOe-KNUwb4)"],
        "triggers": [],  # will be evaluated run-time
        "trigger_type": "any",
        "chance": 100,
        "exact": False,
        "include_bot": False,
    },
    "thank": {
        "messages":
            ["Thank you peko", "Thank you peko!", "Thank you peko~", "Arigatou peko!", "Thank you peko!",
            "Thank you peko~", "Arigatou peko!", "Arigatou peko~", "ありがとうぺこ～", "ありがとうぺこ！",
            "Thank you peko!", "Thank you peko~", "Ehehe", "Ehehe",
            "Arigatou peko da ne! [peko~](https://www.youtube.com/watch?v=zOUPxaA6mBM)",
            "[Arigatou peko.](https://www.youtube.com/watch?v=swGNEJ56EFI)"],
        "triggers": ["good", "best", "amazing", "wonderful", "based"],
        "trigger_type": "any",
        "include_bot": True,
        "chance": 100,
        "exact": False,
    },
    "sorry": {
        "messages": ["Sorry peko ; ;", "Sorry peko...", "G-Gomen peko.", "ごめんぺこ・・・"],
        "triggers": ["bad", "worst", "awful", "terrible", "unbased"],
        "trigger_type": "any",
        "include_bot": True,
        "chance": 100,
        "exact": False,
    },
    "insult": {
        "messages":
            ["Bakatare ga!", "Bakatare ga!", "Bakatare ga!", "Bakatare ga!", "Anta wa baka nano?", "バカたれが！",
           "ばかたれが！", "あんたはバカなの？", "ぺっ", "Go peko yourself!",
           "[Disgusting.](https://streamable.com/6ntf2g)"],
        "triggers": ["insult me peko"],
        "trigger_type": "any",
        "chance": 100,
        "exact": False,
        "include_bot": False,
    },
    "love":{
        "messages":
            ["Thank you guys. Don't cheat on me, okay? [Peko~](https://streamable.com/8gagri)",
            "[Love you](https://streamable.com/dbzfxj) too peko!", "I love you too peko!", "Love you too peko~"],
        "triggers": ["love you","すき","好き", "love this bot"],
        "trigger_type": "any",
        "chance": 100,
        "exact": False,
        "include_bot": False,
    },
    "cute": {
        "messages":
            ["You're cute too peko!", "You're also cute peko!", "You're cute too peko~", "You're also cute peko~", "Ehehe", "あなたもかわいいぺこ！"],
        "triggers": ["cute","kawaii"],
        "trigger_type": "any",
        "include_bot": True,
        "chance": 100,
        "exact": False,
    },
    "nothing changed": {
        "messages":
            ["Sorry, I couldn\'t pekofy the comment for some reason peko. So here\'s a clip of Pekora saying [{}]({}) instead peko.".format(
            title, link) for title, link in {
                "naww": "https://www.youtube.com/watch?v=JNgCFHbPARg",
                "motherf*cker": "https://www.youtube.com/watch?v=1OjQVMiyUMg",
                "oh no jesus": "https://www.youtube.com/watch?v=MwCNEySMNWg",
                "yolo": "https://www.youtube.com/watch?v=MSUckSO-Dsw",
                "ogey rrat": "https://www.youtube.com/watch?v=JacN1MzyeKo",
                "rrat simulator rrrra": "https://www.youtube.com/watch?v=Xr_pKdyeIJo",
                "wao wao waoo!":"https://www.youtube.com/watch?v=O9s_HLql2YM",
                "pardun?":"https://www.youtube.com/watch?v=a3DpRlWdnDw",
                "holy sheet":"https://www.youtube.com/watch?v=yo0_m34o6Mg",
                "motherf*cker": "https://www.youtube.com/watch?v=4q1B06m4_Lk", # Korone roll
                "god bless you": "https://streamable.com/1w8pbx",
                "hi honey": "https://www.youtube.com/watch?v=n8psYwqS544"
            }.items()],
        "triggers": ["NOTHING_CHANGED", "NO_LETTER"],
        "trigger_type": "any",
        "exact": True,
        "chance": 100,
        "include_bot": False,
    },
    "pekofy": {
        "messages": [],  # will be evaluated run-time
        "triggers": ["!pekofy"],
        "trigger_type": "any",
        "chance": 100,
        "exact": False,
        "include_bot": False,
    },
    "unpekofy": {
        "messages": [],  # will be evaluated run-time
        "triggers": ["!unpekofy"],
        "trigger_type": "any",
        "chance": 100,
        "exact": False,
        "include_bot": False,
    },
    "merry christmas": {
        "messages": ["Merry christmas [peko!](https://www.youtube.com/watch?v=v4jHHWdPiCM)", "Merry christmas [peko~](https://www.youtube.com/watch?v=v4jHHWdPiCM)", "Merry christmas peko!", "Merry christmas peko~", "メリークリスマスぺこ～"],
        "triggers": ["merry christmas"],
        "trigger_type": "any",
        "chance": 100,
        "exact": False,
        "include_bot": False,
    },
    "marry": {
        "messages": ["Thank you, but I cant. I'm everyone's idol, peko~", 
                    "I bet you tell this to all bots, baka peko!",
                    "https://www.youtube.com/watch?v=3FOe-KNUwb4",
                    "HA↑HA↓HA↑HA↓HA↑HA↓HA↑HA↓HA↑HA↓HA↑HA↓HA↑HA↓HA↑HA↓"],
        "triggers": ["marry me", "marry me peko", "marry me!", "marry me peko!"],
        "trigger_type": "any",
        "chance": 100,
        "exact": False,
        "include_bot": False
    }
}
