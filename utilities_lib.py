import urllib2
from bs4 import BeautifulSoup

# Utility functions
def is_text(elem):
    text = str(elem)
    if '<' in text or '>' in text:
        return False
    return True

def rem_lead_end_spaces(text):
    ret = text
    if text[0] == ' ':
        ret = ret[1:]
    if text[-1] == ' ':
        ret = ret[:-1]
    return ret

def remove_leading_space(text):
    if text[0] == ' ':
        return text[1:]
    return text

def remove_leading_zeroes(text):
    i = 0
    while text[i] == '0':
        i += 1
    return text[i:]

def remove_brackets(text):
    return text[1:-1]

def purify_text(soup):
    pure_texts = []
    for verse_soup in soup:
        pure_text = ''
        # Go through the contents of this verse
        for cont in verse_soup.contents:
            # If text
            if not cont.name:
                pure_text += cont.encode('utf8')
            # If <a> tag or <u> tag
            elif cont.name == 'a' or cont.name == 'u' and cont.contents:
                pure_text += cont.contents[0].encode('utf8')
        pure_text = remove_leading_space(pure_text)
        pure_texts.append(pure_text)
    return pure_texts