# stylesheet_analyst.py
# by Chris Winikka

# Purpose:
# verify correct syntax using expanded syntax
# see [Use expanded syntax](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Guidelines/Code_guidelines/CSS#Use_expanded_syntax)
# to be used by report.py

from webanalyst import CSSinator as cssinator
styles = cssinator.Stylesheet
from webanalyst import clerk
from webanalyst import colortools
import re

global_selectors = ('body','html','*')
descendant_re = r'([^/s,;]+\s){2}[{]'

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
    type_selectors = ["body", "html", "p", "h1", "h2",
    "h3", "h4", "h5", "h6", "ul", "ol", "li",
    "dt", "dd", "dl", "a", "br", "hr", "table",
    "tr", "td", "th", "thead", "tbody", "tfoot",
    "div", "span", "i", "b", "em", "strong",
    "kbd", "button", "input", "abbr", "address", "applet",
    "area", "article", "aside", "audio", "bdi", "bdo", "blockquote",
    "canvas", "caption", "cite", "code", "col", "colgroup",
    "data", "datalist", "details", "dfn", "dialog",
    "embed", "fieldset", "figurecaption", "figure",
    "footer", "form", "header", "iframe", "img",
    "ins", "label", "legend", "main", "map", "mark",
    "meter", "nav", "object", "optgroup", "option",
    "output", "param", ""]
    type_selectors.sort()
    return type_selectors

def applies_global_colors(sheet):
    """ checks to see if a stylesheet sets color and bg color globally """
    results = False
    color_properties = []
    for rule in sheet.rulesets:
        if rule.selector not in global_selectors:
            continue
        for declaration in rule.declaration_block.declarations:
            if declaration.property not in ('color', 'background-color', 'background'):
                continue
            color_properties.append((declaration.property, declaration.value))
    if len(color_properties) >= 2:
        if color_properties[0][0] == 'color' or color_properties[1][0] == 'color':
            if color_properties[0][0] == 'background-color' or color_properties[1][0] == 'background-color':
                results = True
    return results
    
def applies_global_font(sheet):
    """ checks to see if a stylesheet sets color and bg color globally """
    font_properties = []
    for rule in sheet.rulesets:
        if rule.selector not in global_selectors:
            continue
        for declaration in rule.declaration_block.declarations:
            if declaration.property not in ('font', 'font-family'):
                continue
            font_properties.append(declaration)
        
    return bool(font_properties)

def applies_selector(sheet, selector):
    """ determines whether a stylesheet uses a particular selector or not """
    pass

def is_descendant_selector(sheet):
    """ return true if regex has a match with descendant selector pattern """
    match = re.search(descendant_re, sheet.text)
    if match:
        return True
    return False

if __name__ == "__main__":
    # Test off of large project
    layout_css = clerk.file_to_string(
        "tests/test_files/projects/large_project/css/general.css")
    
    test_sheet = cssinator.Stylesheet("local", layout_css, "file")
    repeat_selectors = get_repeat_selectors(test_sheet)
    print(repeat_selectors)
    has_type_selector(test_sheet)
    print(applies_global_colors(test_sheet))
    is_descendant_selector(test_sheet)