# CSSinator.py
# by Chris Winikka
# a set of tools to analyze CSS

import mechanicalsoup
from pathlib import Path
import bs4
import re

# TODO:
# 1. Move testing code
# 2. convert code to list of selectors
#   3. convert code to list of declarations
# add CSS checks (other than simply validation)


def missing_end_semicolon(css_code):
    # remove all whitespace and line breaks
    # if there is no semicolon preceding closing curly bracket,
    # return True
    return True


def has_repeat_selector(css_code):
    return False


def split_css(css_code):
    """returns list of selectors & declarations (no { or })"""
    # remove newlines
    css_code = css_code.replace('\n', '')
    pattern = r'\{(.*?)\}'
    return re.split(pattern, css_code)


def get_selectors(css_list):
    selectors = []
    for i in range(0, len(css_list), 2):
        selectors.append(css_list[i].strip())
    selectors.remove('')
    return selectors


def get_declarations(css_list):
    declarations = []
    for i in range(1, len(css_list), 2):
        declarations.append(css_list[i].strip())
    if '' in declarations:
        declarations.remove('')
    return declarations


if __name__ == "__main__":
    print("hello, I'm CSSinator.")
    # resp = browser.open("https://jigsaw.w3.org/css-validator")
    # print(resp)
    # valid_css = "p { color: #336699; }"
    # invalid_css = "p { display: phred; } em { stoiky-lob"

    # # validate valid CSS
    # results = validate_css(valid_css)
    # print(results)
    # is_valid = is_css_valid(valid_css)
    # print("Are results valid? {}".format(is_valid))

    # # validate invalid CSS
    # results = validate_css(invalid_css)
    # print(results)
    # print("Results are of a {} type.".format(type(results)))
    # is_valid = is_css_valid(invalid_css)
    # print("Are results valid? {}".format(is_valid))

    # result_list = get_css_errors_list(results)
    # for i in result_list:
    #   print(i)
