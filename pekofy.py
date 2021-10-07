import regex

# IMPORTANT: This version of the better_profanity is the one I forked and
# the PR is not approved atm, so use the following line to install it 
# individually for the time being.
# pip install git+https://github.com/emso-c/better_profanity.git@issue-34
from better_profanity import profanity
profanity.load_censor_words_from_file('./profanity/custom_profanity_wordlist.txt')

ZERO_WIDTH_WHITESPACE = str("​")  # len(ZERO_WIDTH_WHITESPACE) is 1

def is_japanese(text):
    return regex.compile("[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf}]").search(text)

def pekofy(input_text):
    # Just to make the matching work if the text doesn't already include a newline at the end
    text = input_text + '\n'

    if not text.lower().islower() and not is_japanese(text):
        return "NO_LETTER"

    en_punctuation_list = ['.', '?', '!', '\]', '\n']
    jp_punctuation_list = ['。', '？', '！', '」', '・', '”', '】', '』', '；']
    punctuation_list = en_punctuation_list + jp_punctuation_list

    jp_keyword = 'ぺこ'
    en_keyword = ' peko'

    # pattern looks incomprehensible, but it just matches links, and any punctuation at the end (plus parenthesis)
    link_pattern = rf'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]*\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)([{"".join(punctuation_list)})])*'
    # pattern matches any punctuation, with the exception of those in spoiler tags
    incomp_pattern = rf'(?<!<|!>)([{"".join(punctuation_list)}]+)(?!>)'
    # pattern matches any punctuation not in a link
    punctuation_pattern = regex.compile(rf'(?<!({link_pattern})){incomp_pattern}')

    new_text = text
    # offset to account for adding keywords
    offset = 0

    for match in punctuation_pattern.finditer(new_text):
        i = match.start() + offset # match point
        last_word = regex.search(r'[^\W_]', new_text[i::-1]) # find the nearest alphanumeric behind match point
        try:
            j = i - last_word.start() + 1 # index to insert keyword

            if is_japanese(last_word.group()):
                keyword = jp_keyword
            elif last_word.group().isupper():
                keyword = en_keyword.upper()
            else:
                keyword = en_keyword
        except AttributeError: # If the entire string is just non-alphanumeric
            continue

        # Exceptions
        # General case for when there's already a peko and it's newly added
        already_keyword = (new_text[j - len(keyword):j] == keyword)
        if_newly_added = (text[j - offset - len(keyword):j - offset] == keyword)
        # nbsp-specific exception
        nbsp = new_text[j - len('&#x200B'):j] == '&#x200B'
        if (already_keyword and not if_newly_added) or nbsp:
            continue

        new_text = new_text[:j] + keyword + new_text[j:]
        offset += len(keyword)

    if new_text == text:
        return "NOTHING_CHANGED"

    # add zero-width-whitespace to disable mentioning usernames
    new_text = new_text[:-1].replace("u/",f"u{ZERO_WIDTH_WHITESPACE}/")

    # filter profanity
    new_text = profanity.censor(new_text, censor_char='\*', middle_only=True)
    
    return new_text
