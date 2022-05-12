# stylesheet_analyst.py
# by Chris Winikka

# Purpose:
# verify correct syntax using expanded syntax
# see [Use expanded syntax]
# (https://developer.mozilla.org/en-US/docs/MDN/Contribute/Guidelines/Code_guidelines/CSS#Use_expanded_syntax)
# to be used by report.py

import re

from . import CSSinator as cssinator
from . import clerk

styles = cssinator.Stylesheet
global_selectors = ("body", "html", "*")
descendant_re = r"([^/s,;]+\s){2}[{]"

# note multiple_selectors_re only works when looking at selectors
multiple_selectors_re = r"\S+,\s{1}"
direct_child_selector_re = r"(\S+\s?>\s?\S+){1}"
general_sibling_selector_re = r"(\S+\s?~\s?\S+){1}"
adjacent_sibling_selector_re = r"(\S+\s?\+\s?\S+){1}"
class_selector_re = r"(\.\S+){1}\s?\S?\s?"
id_selector_re = r"(\#\S+){1}\s?\S?\s?"

pseudoselectors = (
    ":active",
    ":any-link",
    ":autofill",
    ":blank",
    ":checked",
    ":current",
    ":default",
    ":defined",
    ":dir(",
    ":disabled",
    ":empty",
    ":enabled",
    ":first",
    ":first-child",
    ":first-of-type",
    ":fullscreen",
    ":future",
    ":focus",
    ":focus-visible",
    ":focus-within",
    ":has(",
    ":host",
    ":host(",
    ":host-context(",
    ":hover",
    ":indeterminate",
    ":in-range",
    ":invalid",
    ":is(",
    ":lang(",
    ":last-child",
    ":last-of-type",
    ":left",
    ":link",
    ":local-link",
    ":not(",
    ":nth-child(",
    ":nth-col(",
    ":nth-last-child(",
    ":nth-last-col(",
    ":nth-last-of-type(",
    ":nth-of-type(",
    ":only-child",
    ":only-of-type",
    ":optional",
    ":out-of-range",
    ":past",
    ":picture-in-picture",
    ":placeholder-shown",
    ":paused",
    ":playing",
    ":read-only",
    ":read-write",
    ":required",
    ":right",
    ":root",
    ":scope",
    ":state(",
    ":target",
    ":target-within",
    ":user-invalid",
    ":valid",
    ":visited",
    ":where(",
)

pseudoelements = (
    "::after",
    "::backdrop",
    "::before",
    "::cue",
    "::cue-region",
    "::first-letter",
    "::first-line",
    "::file-selector-button",
    "::grammar-error",
    "::marker",
    "::part(",
    "::placeholde",
    "::selection",
    "::slotted(",
    "::spelling-error",
    "::target-text",
)


def get_repeat_selectors(sheet):
    repeat_selectors = []
    sheet.sort_selectors()
    for selector in sheet.selectors:
        count = sheet.selectors.count(selector)
        if count > 1:
            if [selector, count] not in repeat_selectors:
                repeat_selectors.append([selector, count])
    return repeat_selectors


def has_type_selector(sheet):
    sheet.sort_selectors()
    type_selectors = get_type_selectors()
    for selector in type_selectors:
        if selector in sheet.selectors:
            return True
    return False


def get_type_selectors():
    type_selectors = [
        "body",
        "html",
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "ul",
        "ol",
        "li",
        "dt",
        "dd",
        "dl",
        "a",
        "br",
        "hr",
        "table",
        "tr",
        "td",
        "th",
        "thead",
        "tbody",
        "tfoot",
        "div",
        "span",
        "i",
        "b",
        "em",
        "strong",
        "kbd",
        "button",
        "input",
        "abbr",
        "address",
        "applet",
        "area",
        "article",
        "aside",
        "audio",
        "bdi",
        "bdo",
        "blockquote",
        "canvas",
        "caption",
        "cite",
        "code",
        "col",
        "colgroup",
        "data",
        "datalist",
        "details",
        "dfn",
        "dialog",
        "embed",
        "fieldset",
        "figurecaption",
        "figure",
        "footer",
        "form",
        "header",
        "iframe",
        "img",
        "ins",
        "label",
        "legend",
        "main",
        "map",
        "mark",
        "meter",
        "nav",
        "object",
        "optgroup",
        "option",
        "output",
        "param",
    ]
    type_selectors.sort()
    return type_selectors


def applies_global_colors(sheet):
    """checks to see if a stylesheet sets color and bg color globally"""
    results = False
    color_properties = []
    for rule in sheet.rulesets:
        if rule.selector not in global_selectors:
            continue
        for declaration in rule.declaration_block.declarations:
            if declaration.property not in (
                "color",
                "background-color",
                "background",
            ):
                continue
            color_properties.append((declaration.property, declaration.value))
    if len(color_properties) >= 2:
        if color_properties[0][0] == "color" or color_properties[1][0] == "color":
            if (
                color_properties[0][0] == "background-color"
                or color_properties[1][0] == "background-color"
            ):
                results = True
    return results


def applies_global_font(sheet):
    """checks to see if a stylesheet sets color and bg color globally"""
    font_properties = []
    for rule in sheet.rulesets:
        if rule.selector not in global_selectors:
            continue
        for declaration in rule.declaration_block.declarations:
            if declaration.property not in ("font", "font-family"):
                continue
            font_properties.append(declaration)

    return bool(font_properties)


def applies_selector(sheet, selector):
    """determines whether a stylesheet uses a particular selector or not"""


def has_descendant_selector(sheet):
    """return true if regex has a match with descendant selector pattern"""
    match = re.search(descendant_re, sheet.text)
    if match:
        return True
    return False


def has_multiple_selector(sheet):
    """returns True if separates selectors with commas (e.g. h1, h2, h3 {...})"""
    # We can only sift through selectors (not the entire text for this)
    return check_selectors_with_regex(sheet, multiple_selectors_re)


def has_direct_child_selector(sheet):
    """returns True if separates selectors with > (e.g. article > p {...})"""
    return check_selectors_with_regex(sheet, direct_child_selector_re)


def check_selectors_with_regex(sheet, regex):
    for selector in sheet.selectors:
        match = re.search(regex, selector)
        if match:
            return True
    for ruleset in sheet.nested_at_rules.values():
        for rule in ruleset:
            match = re.search(regex, rule.selector)
            if match:
                return True
    return False


def has_psuedoselector(sheet):
    """returns True if has a psuedoselector"""
    results = False
    for selector in sheet.selectors:
        if ":" in selector:
            for pseudoselector in pseudoselectors:
                if pseudoselector in selector:
                    return True
    return results


def get_psuedoselectors(sheet):
    """returns a list of all psuedoselectors from a stylesheet"""
    selectors = []
    return selectors


def has_repeat_selectors(sheet):
    selectors = sheet.selectors[:]
    selectors.sort()
    for selector in selectors:
        num_selector = selectors.count(selector)
        if num_selector > 1:
            return True
    return False


def has_class_selector(sheet):
    return check_selectors_with_regex(sheet, class_selector_re)


def has_id_selector(sheet):
    return check_selectors_with_regex(sheet, id_selector_re)


if __name__ == "__main__":
    # Test off of large project

    layout_css = clerk.file_to_string(
        "tests/test_files/projects/large_project/css/navigation.css"
    )
    test_sheet = cssinator.Stylesheet("local", layout_css, "file")

    repeat_selectors = get_repeat_selectors(test_sheet)
    print(repeat_selectors)
    has_type_selector(test_sheet)
    print(applies_global_colors(test_sheet))
    has_descendant_selector(test_sheet)
    has_multiple_selector(test_sheet)
    has_direct_child_selector(test_sheet)
    has_psuedoselector(test_sheet)
    has_repeat_selectors(test_sheet)
    has_class_selector(test_sheet)
