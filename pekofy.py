import re

def is_japanese(text):
    return re.compile("[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf}]").search(text)

# Tbh, this one is bit of a mess and probably the most un-pythonic way to do this, but hey, it works! (kinda)
# If you know a better way to implement, please create a pull request.
def pekofy(text):
    if not text.lower().islower() and not is_japanese(text):
        return "NO_LETTER"
    punctuation_list = ['.', '?', '!', '"', ')', ']', ':', '~', '~~', '\\[\*]?']  # asterisk has been hard coded into the regex_comp
    keyword = " peko"
    jp_punctuation_list = ['。', '？', '！', '」', '・', '～']
    jp_keyword = "ぺこ"
    punctuation_list.extend(jp_punctuation_list)
    regex = "(\\" + "|\\".join(punctuation_list) + "|[*]{1,3})"
    regex_comp = re.compile(regex)
    new_text = []

    text = re.split("\n", text)
    for line in text:
        line = re.split(regex, line)
        quote_counter = 0
        asterisk_counter = 0
        if len(line) > 2:
            if line[1] == '*' and (line.count('*') % 2 == 1):  # adjust for list
                asterisk_counter = 1
        asterisk_slashed_counter = 0
        tilde_counter = 0
        ignore_next_paranthesis = False
        for i in range(0, len(line)):
            if i != len(line) - 1:
                # QUOTE SOLUTION
                if line[i + 1] == "\"":
                    quote_counter += 1
                    if quote_counter == 1:
                        continue
                    elif quote_counter == 2:
                        quote_counter = 0
                # TILDE SOLUTION
                if line[i + 1] == "~~":
                    tilde_counter += 1
                    if tilde_counter == 1:
                        continue
                    elif tilde_counter == 2:
                        tilde_counter = 0

                # ASTERISK SOLUTION
                if line[i + 1] in ['*', '**', '***']:
                    asterisk_counter += 1
                    if (asterisk_counter % 2) == 1:
                        continue
                # BACKSLASH SOLUTION
                if line[i + 1] == '\\':
                    continue
                # ASTERISK WITH BACKSLASH SOLUTION
                if line[i + 1] == '\\*':
                    asterisk_slashed_counter += 1
                    if (asterisk_slashed_counter % 2) == 1:
                        continue

                # LINK SOLUTION
                if re.compile("^(\(http[s]?)").search(line[i]):
                    ignore_next_paranthesis = True
                    continue
                if line[i + 1] == '.' and line[i + 2] and not line[i + 2].startswith(' '):
                    continue
                if line[i + 1] == ':' and line[i + 2] == '//www':
                    continue

                # SLASH SOLUTION
                if i < len(line) - 3:
                    if line[i + 1] == '\\' and line[i + 3] and line[i + 3].startswith('*'):
                        continue

                # SPOILER SOLUTION
                if line[i + 1] == "!" and line[i].endswith('<'):
                    continue

                # :^)
                if line[i] == '^' and line[i + 1] == ')':
                    continue

                # EOL SOLUTION (TILDE, JP_TILDE, COLON)
                if line[i + 1] in [':', '~', '～'] and line[i + 2].strip():
                    if not line[i + 2] == '^':
                        continue
            if not regex_comp.search(line[i]) and line[i] and not line[i].isspace():
                if i != len(line) - 1:
                    if line[i + 1] == '?' and ignore_next_paranthesis:  # for \? in the links
                        continue
                    if line[i + 1] == ')':
                        if ignore_next_paranthesis:
                            ignore_next_paranthesis = False
                            continue
                    if line[i].endswith('>'):  # SPOILER SOLUTION
                        continue
                    if line[i + 1] and regex_comp.search(line[i + 1]):
                        if is_japanese(line[i][-1]):
                            line[i] = line[i] + jp_keyword
                            continue
                        line[i] = line[i] + (keyword if not line[i].isupper() else keyword.upper())
                else:
                    if line[i] == '&#x200B;':
                        continue
                    if is_japanese(line[i][-1]):
                        line[i] = line[i] + jp_keyword
                        continue
                    if not line[i].lower().islower():  # NON-WORD LINE SOLUTION
                        continue
                    if line[i].endswith('>'):  # SPOILER END SOLUTION
                        continue
                    line[i] = line[i] + (keyword if not line[i].isupper() else keyword.upper())
        new_text.append(''.join(line))
    if new_text == text:
        return "NOTHING_CHANGED"
    return '\n'.join(new_text).replace("u/","u​/")

