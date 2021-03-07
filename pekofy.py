import regex

def is_japanese(text):
    return regex.compile("[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf}]").search(text)

# Tbh, this one is bit of a mess and probably the most un-pythonic way to do this, but hey, it works! (kinda)
# If you know a better way to implement, please create a pull request.
def pekofy(text):
    if not text.lower().islower() and not is_japanese(text):
        return "NO_LETTER"

    en_punctuation_list = ['.', '?', '!', '\]', '\n']
    jp_punctuation_list = ['。', '？', '！', '」', '・']
    punctuation_list = en_punctuation_list + jp_punctuation_list

    jp_keyword = 'ぺこ'
    en_keyword = ' peko'

    # pattern looks incomprehensible, but it just matches links (with or without parentheses at the end)
    link_pattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]*\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)(\)?)'
    # a pattern that matches any punctuation not in a link
    punctuation_pattern = regex.compile(rf'(?<!({link_pattern}))([{"".join(punctuation_list)}])+')

    new_text = text
    # offset to account for adding keywords
    offset = 0
    for match in punctuation_pattern.finditer(text):
        i = match.start() + offset # match point
        last_word = regex.search(r'\w+', new_text[i::-1]) # find the nearest alphanumeric behind match point
        j = i - last_word.start() + 1 # index to insert keyword
        keyword = jp_keyword if is_japanese(last_word.group()) else en_keyword

        new_text = new_text[:j] + keyword + new_text[j:]
        offset += len(keyword)

    if new_text == text:
        return "NOTHING_CHANGED"

    return new_text
