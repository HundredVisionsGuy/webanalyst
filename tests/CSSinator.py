# CSSinator.py
# by Chris Winikka
# a set of tools to analyze CSS

import mechanicalsoup
from pathlib import Path
import bs4
import re
import cssutils

# TODO:
# 1. Move testing code
# 2. convert code to list of selectors
# 3. convert code to list of declarations
# add CSS checks (other than simply validation)
css_with_errors = """<body> {
    font-size: 1.2em;
    color: brown;
    background-color: aliceblue;
} 
"""
css_code = """
/* styles.css
    Apply general styles to the entire
    document
*/

/* TODO
 *  Use the adobe color mixer to select
    a color combination for the body
    Make sure it passes the Color Contrast tool with at least a AA rating
*/

body {
    background-color: #B3855D;
    color: #142326;
    font-family: 'Ubuntu', sans-serif;
    font-size: initial;
}
article#gallery {
    display: flex;
    flex-wrap: wrap;
    width: 96vw;
    margin: 0 auto;
}
figure {
    width: 200px;
    background-color: #7D8C45;
    padding: .7em;
    border: .3em solid #142326;
    margin: .5rem;
}
/* set image to  match width of the
    figure */
figure img {
    width: 100%;
    max-width: 100%;
}
"""


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


def get_comment_positions(code):
    positions = []
    try:
        positions.append(code.index("/*"))
        positions.append(code.index("*/"))
        return positions
    except:
        return


def separate_code(code):
    """ splits code into two lists: code & comments """
    code = code.strip()
    splitzky = {"code": [],
                "comments": []}

    new_code = []
    comments = []
    # Get positions of comments and place all code up to the comments
    # in code and comments in comments
    # do this till all code has been separated
    while code:
        positions = get_comment_positions(code)
        if positions and len(positions) == 2:
            start = positions[0]
            stop = positions[1]
            if code[:start]:
                new_code.append(code[:start])
            if code[start:stop+2]:
                comments.append(code[start:stop+2])
            code = code[stop + 2:]
            code = code.strip()
        else:
            if "/*" not in code and "*/" not in code:
                new_code.append(code)
                code = ""
            else:
                print("We have a problem with the code syntax.")
    splitzky["code"] = new_code
    splitzky["comments"] = comments
    return splitzky


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

    # Test out cssutils

    css = split_css(css_with_errors)
    big_css = split_css(css_code)
    try:
        sheet = cssutils.parseString(css_with_errors)
    except Exception as ex:
        print(ex)

    split = separate_code(css_code)
