# CSSinator.py
# by Chris Winikka
# a set of tools to analyze CSS

import mechanicalsoup
from pathlib import Path
import bs4
import re
import cssutils
import webanalyst.clerk

class Stylesheet:
    def __init__(self, href, text, stylesheet_type="file"):
        self.type = stylesheet_type
        self.href = href
        self.text = text
        self.nested_at_rules = []
        self.rulesets = []
        self.comments = []
        self.minify()
        self.extract_comments()
        self.extract_nested_at_rules()
        self.extract_rulesets()
        self.selectors = []
        self.get_selectors()

    def minify(self):
        """ remove all whitespace, line returns, and tabs from text """
        self.text = minify_code(self.text)

    def extract_comments(self):
        # split all CSS text at opening comment
        text_comment_split = self.text.split("/*")
        comments = []
        code_without_comments = ""
        # loop through the list of code
        # in each iteration extract the comment

        for i in text_comment_split:
            # append comment to comments
            if "*/" in i:
                comment = i.split("*/")
                comments.append("/*" + comment[0] + "*/")
                # append code to code_without_comments
                code_without_comments += comment[1]
            else:
                # no comments, just get code
                code_without_comments += i
        # add comments
        self.comments = comments
        # replace code (comments extracted)
        self.text = code_without_comments

    def extract_nested_at_rules(self):
        # Search through nested at rules
        at_rules = []
        non_at_rules_css = []
        # split at the double }} (end of a nested at rule)
        css_split = self.text.split("}}")
        if len(css_split) == 1:
            return
        for code in css_split:
            # continue if empty
            if not code.strip():
                continue
            for rule in nested_at_rules:
                # check each
                if rule in code:
                    # we found a nested @rule
                    # split code from @rule
                    split_code = code.split(rule)
                    if len(split_code) == 2:
                        if split_code[0]:
                            # it began with an @rule (hence the split)
                            non_at_rules_css.append(split_code[0])
                            at_rules.append(rule + split_code[1] + "}}")
                        else:
                            at_rules.append(rule + split_code[1] + "}}")
                    else:
                        # it's only an @rule
                        at_rules.append(rule + split_code + "}}")

        self.text = ''.join(non_at_rules_css)
        self.nested_at_rules = at_rules

    def separate_nested_atrule_and_css(self, rule, text):
        if rule in text:
            start = len(rule)
            text = text[start:]
        at_rule_and_css = text.split("}}")
        if len(at_rule_and_css) > 1:
            if rule in at_rule_and_css[0]:
                nested_at_rule = at_rule_and_css[0]
            else:
                nested_at_rule = rule + at_rule_and_css[0]
            css = at_rule_and_css[1]
            return [nested_at_rule, css]
        else:
            return [None, css]

    def extract_rulesets(self):
        # split rulesets by closing of rulesets: }
        ruleset_list = self.text.split("}")
        for ruleset in ruleset_list:
            if ruleset:
                ruleset = Ruleset(ruleset + "}")
                self.rulesets.append(ruleset)

    def get_selectors(self):
        for rule in self.rulesets:
            self.selectors.append(rule.selector)

    def sort_selectors(self):
        self.selectors.sort()

        
class NestedAtRule:
    def __init__(self, text):
        is_valid = False
        for rule in nested_at_rules:
            if rule in text:
                is_valid = True
        if not is_valid:
            raise Exception("The CSS has no nested @rules.")
        self.__text = minify_code(text)
        self.rule = ""
        self.declaration_block = None
        self.set_at_rule()

    def set_at_rule(self):
        # remove anything before the @ sign
        rule_list = self.__text.split("@")
        rule_list = "@" + rule_list[1]
        
        # split at the first {
        pos = rule_list.find("{")
        self.rule = rule_list[:pos].strip()
        self.declaration_block = DeclarationBlock(rule_list[pos:])


class Ruleset:
    def __init__(self, text):
        self.__text = text
        self.selector = ""
        self.declaration_block = None
        self.is_valid = True
        self.validate()
        self.initialize()

    def initialize(self):
        if self.is_valid:
            contents = self.__text.split("{")
            self.selector = contents[0].replace("\n", "").strip()
            block = contents[1].replace("\n", "")
            self.declaration_block = DeclarationBlock(block)

    def validate(self):
        try:
            open_brace_pos = self.__text.index("{")
            close_brace_pos = self.__text.index("}")
            if open_brace_pos > close_brace_pos:
                # { needs to come before }
                self.is_valid = False
        except:
            self.is_valid = False

        if "{" not in self.__text or "}" not in self.__text:
            self.is_valid = False


class DeclarationBlock:
    def __init__(self, text):
        self.__text = text
        self.declarations = []
        self.__set_declarations()

    def __set_declarations(self):
        declarations = self.__text

        # remove selectors and braces if present
        if "{" in self.__text:
            declarations = declarations.split("{")
            declarations = declarations[1]
        if "}" in declarations:
            declarations = declarations.split("}")
            declarations = declarations[0]

        declarations = declarations.split(";")

        # remove all spaces and line returns
        for i in range(len(declarations)):
            declarations[i] = declarations[i].replace("\n", "")
            declarations[i] = declarations[i].strip()
            if not declarations[i]:
                declarations.pop(i)
            else:
                declarations[i] = Declaration(declarations[i])

        self.declarations = declarations


class Declaration:
    def __init__(self, text):
        self.__text = text
        self.property = ""
        self.value = ""
        self.is_valid = False
        self.set_declaration()

    def set_declaration(self):
        """ validate while trying to set declaration """
        # assume it's valid until proven otherwise
        self.is_valid = True
        # Make sure there's a colon for validity and separating
        if ":" not in self.__text:
            self.is_valid = False
        else:
            elements = self.__text.split(":")
            # make sure there are 2 values after the split
            if len(elements) > 2:
                self.is_valid = False
            else:
                self.property = elements[0].strip()
                self.value = elements[1].strip()
                self.validate_declaration()

    def validate_declaration(self):
        # Check to see if there's only 1 character in value
        # 0 is valid; anything else is invalid
        if len(self.value) == 1 and not self.value == "0":
            self.is_valid = False

        # Make sure there are no spaces in between property
        prop_list = self.property.split()
        if len(prop_list) > 1:
            self.is_valid = False

        # Make sure there's nothing after the semi-colon
        # but account for the empty string element after the split
        # as well as spaces (just in case)
        val_list = self.value.split(";")
        if len(val_list) > 1 and val_list[1].strip():
            self.is_valid = False

    def get_declaration(self):
        return self.property + ": " + self.value

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


def split_by_partition(text, part):
    # base case
    if text.count(part) == 0:
        return [text, ]
    # recursive case
    else:
        text_tuple = text.partition(part)
        return [text_tuple[0], ] + split_by_partition(text_tuple[2], part)


nested_at_rules = (
    "@supports",
    "@document",
    "@page",
    "@font-face",
    "@keyframes",
    "@media",
    "@viewport",
    "@counter-style",
    "@font-feature-values",
    "@property"
)


def minify_code(text):
    """ remove all new lines, tabs, and double spaces """
    text = text.replace("\n", "")
    text = text.replace("  ", "")
    text = text.replace("\t", "")
    return text


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

    # my_stylesheet = Stylesheet()

    # Test out cssutils

    # css = split_css(css_with_errors)
    # big_css = split_css(css_code)
    # try:
    #     sheet = cssutils.parseString(css_with_errors)
    # except Exception as ex:
    #     print(ex)

    # split = separate_code(css_code)

