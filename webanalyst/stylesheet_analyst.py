# stylesheet_analyst.py
# by Chris Winikka

# Purpose:
# verify correct syntax using expanded syntax
# see [Use expanded syntax](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Guidelines/Code_guidelines/CSS#Use_expanded_syntax)
# to be used by report.py

from webanalyst.CSSinator import Stylesheet as styles


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

if __name__ == "__main__":
    import clerk
    
    # Test off of large project
    layout_css = clerk.file_to_string(
        "tests/test_files/projects/large_project/css/layout.css")
    
    test_sheet = styles.Stylesheet("local", layout_css, "file")
    repeat_selectors = get_repeat_selectors(test_sheet)
    print(repeat_selectors)
    has_type_selector(test_sheet)