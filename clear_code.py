import re
import os

# function to clear HTML tags
# https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def clear_tags(text):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', text)
    clean_text = os.linesep.join([s for s in clean_text.splitlines() if s])  # remove blank lines
    return clean_text


# function to remove code between <code> and </code>
def clear_code(text):
    length = 0
    if(isinstance(text,str)):
        length = len(text)
    clean_text = ""
    in_code = False

    for i in range(0, length):
        if (text[i] == "<" and text[i + 1] == "c" and text[i + 2] == "o" and text[i + 3] == "d" and
                text[i + 4] == "e" and text[i + 5] == ">"):
            # found <code>
            in_code = True

        if (text[i-1] == ">" and text[i - 2] == "e" and text[i - 3] == "d" and text[i - 4] == "o" and
                text[i - 5] == "c" and text[i - 6] == "/" and text[i - 7] == "<"):
            # found </code>
            in_code = False

        if (in_code == False):
            clean_text += text[i]  # record text

    return clean_text
