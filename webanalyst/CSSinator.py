# CSSinator.py
# by Chris Winikka
# a set of tools to analyze CSS

import re

from . import color_keywords as keyword
from . import colortools

# Regex Patterns
regex_patterns = {
    "vendor_prefix": r"\A-moz-|-webkit-|-ms-|-o-",
    "header_selector": r"h[1-6]",
    "id_selector": r"#\w+",
    "class_selector": r"\.\w+",
    "pseudoclass_selector": r":\w+",
    "attribute_selector": r"\[\w+=\w+]",
    "type_selector": r"([^#:\+.\[=a-zA-Z][a-zA-Z$][a-zA-Z1-6]*|^\w*)",
    "descendant_selector": r"\w+\s\w+",
    "child_combinator": r"\w+\s*>\s*\w+",
    "adjacent_sibling_combinator": r"\w+\s*\+\s*\w+",
    "general_sibling_combinator": r"\w+\s*~\s*\w+",
    "grouped_selector": r"\w+\s*,\s*\w+"
}

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
    "@property",
)


class Stylesheet:
    def __init__(self, href: str, text: str, stylesheet_type="file") -> None:
        """ href (filename or local if styletag) text (CSS code) """
        self.type = stylesheet_type
        self.href = href
        self.text = text
        self.original_text = text
        self.nested_at_rules = []
        self.rulesets = []
        self.comments = []
        self.color_rulesets = []
        self.minify()
        self.extract_comments()
        self.extract_nested_at_rules()
        self.extract_rulesets_from_at_rules()
        self.extract_rulesets()
        self.selectors = []
        self.get_selectors()

    def minify(self):
        """remove all whitespace, line returns, and tabs from text"""
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
        css_split = self.text.split("}}", 3)
        css_split = restore_braces(css_split)

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
                            # an @rule was NOT at the beginning or else,
                            # there would be an empty string
                            non_at_rules_css.append(split_code[0])
                            at_rules.append(rule + split_code[1])
                        else:
                            at_rules.append(rule + split_code[1])
                    else:
                        # it's only an @rule
                        print("skipping non-nested @rule.")

        self.text = "".join(non_at_rules_css)
        self.nested_at_rules = at_rules

    def extract_rulesets(self):
        # split rulesets by closing of rulesets: }
        ruleset_list = self.text.split("}")
        for ruleset in ruleset_list:
            if ruleset:
                ruleset = Ruleset(ruleset + "}")
                self.rulesets.append(ruleset)
                self.get_color_ruleset(ruleset)

    def extract_rulesets_from_at_rules(self):
        nested_at_rule_dict = {}
        nested_rules = self.nested_at_rules
        for nested_rule in nested_rules:
            nested_rule_split = nested_rule.split("{", 1)
            key = nested_rule_split.pop(0)
            rule_split = nested_rule_split[0].split("}")
            rulesets = []
            for rule in rule_split:
                if len(rule) > 1:
                    if rule[-1] != "}":
                        rule = rule + "}"
                    ruleset = Ruleset(rule)
                    rulesets.append(ruleset)
                    self.get_color_ruleset(ruleset)
            nested_at_rule_dict[key] = rulesets
        self.nested_at_rules = nested_at_rule_dict

    def get_color_ruleset(self, ruleset):
        color_rulesets = []
        if ruleset.declaration_block and "color:" in ruleset.declaration_block.text:
            selector = ruleset.selector
            for declaration in ruleset.declaration_block.declarations:
                if ("color" in declaration.property or
                        "background" in declaration.property):
                    property = declaration.property
                    value = declaration.value
                    # skip if has vendor prefix
                    if has_vendor_prefix(value):
                        continue
                    # skip if not valid color value
                    if not colortools.is_color_value(value):
                        continue
                    # make sure the value is a color (not other)
                    rule = {selector: {property: value}}
                    color_rulesets.append(rule)
        if color_rulesets:
            self.color_rulesets += color_rulesets

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
        except Exception:
            self.is_valid = False

        if "{" not in self.__text or "}" not in self.__text:
            self.is_valid = False


class DeclarationBlock:
    def __init__(self, text):
        self.text = text
        self.declarations = []
        self.__set_declarations()

    def __set_declarations(self):
        declarations = self.text

        # remove selectors and braces if present
        if "{" in self.text:
            declarations = declarations.split("{")
            declarations = declarations[1]
        if "}" in declarations:
            declarations = declarations.split("}")
            declarations = declarations[0]

        declarations = declarations.split(";")

        # remove all spaces and line returns
        for i in range(len(declarations)):
            # make sure i is not out of range (after popping i)
            if i > len(declarations) - 1:
                break
            declarations[i] = declarations[i].replace("\n", "")
            declarations[i] = declarations[i].strip()
            if not declarations[i]:
                declarations.pop(i)
        # create our declaration objects
        # we separated the cleaning from the separating due
        # to the potential of popping i resulting in index error
        # or missing a declaration (it happened)
        for i in range(len(declarations)):
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
        """validate while trying to set declaration"""
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


def get_nested_at_rule(code, rule):
    at_rule = []
    at_split = code.split(rule)
    if len(at_split) > 1:
        if at_split[0] == "":
            # rule was at the beginning
            at_rule.append(rule + " " + at_split[1])
        else:
            at_rule.append(rule + " " + at_split[0])
    return at_rule


def restore_braces(split):
    result = []
    if len(split) <= 1:
        return split
    for item in split:
        if len(item) > 0:
            item = item + "}}"
            result.append(item)
    return result


def split_by_partition(text, part):
    # base case
    if text.count(part) == 0:
        return [
            text,
        ]
    # recursive case
    else:
        text_tuple = text.partition(part)
        return [
            text_tuple[0],
        ] + split_by_partition(text_tuple[2], part)


def minify_code(text: str) -> str:
    """remove all new lines, tabs, and double spaces"""
    text = text.replace("\n", "")
    text = text.replace("  ", "")
    text = text.replace("\t", "")
    return text


def missing_end_semicolon(css_code: str) -> bool:
    # remove all whitespace and line breaks
    cleaned = css_code.replace(" ", "")
    cleaned = css_code.replace("\n", "")
    # if there is no semicolon preceding closing curly bracket,
    return ";}" in cleaned


def has_repeat_selector(styles: Stylesheet) -> bool:
    """ checks stylesheet to determine whether any selectors are repeated 
        or not. """
    # get & sort a list of all selectors
    selectors = styles.selectors

    # loop through and get a count of each
    for selector in selectors:
        count = selectors.count(selector)
        # are there more than 1 of the same kind?
        if count > 1:
            return True
    # otherwise
    return False


def get_nested_at_rule_selectors(sheet: Stylesheet) -> list:
    """ gets all selectors from nested @rules """
    selectors = []
    for at_rule in sheet.nested_at_rules.keys():
        type = at_rule.split()[0]
        if type not in ["@media", "@page", "@supports"]:
            continue
        for item in sheet.nested_at_rules[at_rule]:
            selectors.append(item.selector)
    return selectors


def split_css(css_code):
    """returns list of selectors & declarations (no { or })"""
    # remove newlines
    css_code = css_code.replace("\n", "")
    pattern = r"\{(.*?)\}"
    return re.split(pattern, css_code)


def get_selectors(css_list):
    selectors = []
    for i in range(0, len(css_list), 2):
        selectors.append(css_list[i].strip())
    selectors.remove("")
    return selectors


def get_declarations(css_list):
    declarations = []
    for i in range(1, len(css_list), 2):
        declarations.append(css_list[i].strip())
    if "" in declarations:
        declarations.remove("")
    return declarations


def get_comment_positions(code):
    positions = []
    try:
        positions.append(code.index("/*"))
        positions.append(code.index("*/"))
        return positions
    except Exception as ex:
        print(ex)
        return


def separate_code(code):
    """splits code into two lists: code & comments"""
    code = code.strip()
    splitzky = {"code": [], "comments": []}

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
            if code[start : stop + 2]:
                comments.append(code[start : stop + 2])
            code = code[stop + 2 :]
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


def get_color_rulesets(objects):
    color_rulesets = []
    if objects:
        for style_tag in objects:
            if style_tag.color_rulesets:
                for ruleset in style_tag.color_rulesets:
                    for declaration in ruleset.declaration_block.declarations:
                        if declaration.is_valid:
                            if "color" in declaration.property.lower():
                                if ruleset not in color_rulesets:
                                    color_rulesets.append(ruleset)
    return color_rulesets


def get_specificity(selector):
    id_selector = get_id_score(selector)
    class_selector = get_class_score(selector)
    type_selector = get_type_score(selector)
    return "{}{}{}".format(id_selector, class_selector, type_selector)


def get_id_score(selector):
    """receives a selector and returns # of id selectors"""
    pattern = regex_patterns["id_selector"]
    id_selectors = re.findall(pattern, selector)
    return len(id_selectors)


def get_class_score(selector):
    """receives a selector and returns # of class & psuedo-class selectors"""
    class_re = regex_patterns["class_selector"]
    selectors = re.findall(class_re, selector)
    pseudo_re = regex_patterns["pseudoclass_selector"]
    pseudo_selectors = re.findall(pseudo_re, selector)
    selectors += pseudo_selectors
    attribute_re = regex_patterns["attribute_selector"]
    attribute_selectors = re.findall(attribute_re, selector)
    selectors += attribute_selectors
    return len(selectors)


def get_type_score(selector):
    """receives a selector and returns # of type selectors"""
    pattern = regex_patterns["type_selector"]
    selectors = re.findall(pattern, selector)
    return len(selectors)


def get_header_color_details(rulesets):
    """receives rulesets and returns data on colors set by headers"""
    header_rulesets = []
    for ruleset in rulesets:
        selector = ruleset.selector
        # check selector for having a header
        heading_selectors = get_header_selectors(selector)
        if heading_selectors:
            # get color data
            background_color = ""
            color = ""
            for declaration in ruleset.declaration_block.declarations:
                if declaration.property == "background-color":
                    background_color = declaration.value
                elif declaration.property == "color":
                    color = declaration.value
                elif declaration.property == "background":
                    # check to see if the color value is present
                    print("it's time to figure out the background shorthand")
                if background_color and color:
                    break

            # then apply color data to all others
            if background_color or color:
                for h_selector in heading_selectors:
                    header_rulesets.append(
                        {
                            "selector": h_selector,
                            "background-color": background_color,
                            "color": color,
                        }
                    )

    return header_rulesets


def get_header_selectors(selector):
    """takes selector and returns any selector that selects an h1-h6"""
    # NOTE the following:
    # a selector is only selecting a header if it's the last item
    # example: header h1 {} does but h1 a {} does not
    header_selectors = []
    selectors = [sel.strip() for sel in selector.split(",")]
    if selectors[0]:
        for selector in selectors:
            items = selector.split()
            pattern = regex_patterns["header_selector"]
            h_match = re.search(pattern, items[-1])
            if h_match:
                header_selectors.append(selector)
    return header_selectors


def get_global_color_details(rulesets):
    """receives rulesets and returns data on global colors"""
    # Are color and background color set on global selectors?
    global_selectors = ("html", "body", ":root", "*")
    global_rulesets = []
    for ruleset in rulesets:
        if ruleset.selector in global_selectors:
            selector = ruleset.selector
            background_color = ""
            color = ""
            for declaration in ruleset.declaration_block.declarations:
                if declaration.property == "background-color":
                    background_color = declaration.value
                elif declaration.property == "color":
                    color = declaration.value
                    if is_gradient(color):
                        colors = process_gradient(color)
                        todo = input("We have colors: " + colors)
                        print(todo)
                elif declaration.property == "background":
                    background_color = declaration.value
                    if is_gradient(background_color):
                        bg_colors = process_gradient(background_color)
                        print("We have bg colors: " + str(bg_colors))

            if background_color or color:
                global_rulesets.append(
                    {
                        "selector": selector,
                        "background-color": background_color,
                        "color": color,
                    }
                )
    return global_rulesets


def has_vendor_prefix(property):
    vendor_prefixes = ("-webkit-", "-moz-", "-o-", "-ms-")
    for prefix in vendor_prefixes:
        if prefix in property:
            return True
    return False


def is_gradient(value):
    return "gradient" in value


def process_gradient(code: str) -> list:
    """returns list of all colors from gradient sorted light to dark"""
    colors = []
    data = code.split("),")

    # split the last datum in data into two
    last_item = data[-1].strip()
    last_split = last_item.split("\n")
    if len(last_split) == 2:
        data.append(last_split[1])

    # remove all vendor prefixes
    pattern = regex_patterns["vendor_prefix"]
    for datum in data:
        datum = datum.strip()
        if not re.match(pattern, datum):
            colors.append(datum)

    # capture only color codes and append to colors
    only_colors = []
    if colors:
        # grab only color codes (Nothing else)
        for gradient in colors:
            color_codes = get_colors_from_gradient(gradient)
            if color_codes:
                only_colors += color_codes
    only_colors = sort_color_codes(only_colors)
    return only_colors


def sort_color_codes(codes):
    """ sorts color codes from light to dark (luminance)"""
    # convert code to rgb then calculate luminance
    colors = []
    for c in codes:
        # get the color type and convert to hsl
        temp_c = c
        color_type = colortools.get_color_type(c)
        has_alpha = colortools.has_alpha_channel(c)
        is_hex = colortools.is_hex(temp_c)
        if has_alpha and not is_hex:
            temp_c = remove_alpha(c)
        if "hsl" not in color_type:
            if is_hex:
                rgb = colortools.hex_to_rgb(temp_c)
            else:
                rgb = temp_c
        else:
            rgb = colortools.hsl_to_rgb(c)
        if "<class 'str'>" == str(type(rgb)):
            r, g, b = colortools.extract_rgb_from_string(rgb)
            light = colortools.luminance((int(r), int(g), int(b)))
        else:
            light = colortools.luminance(rgb)
        colors.append([light, c])
    colors.sort()
    colors.reverse()
    sorted = []
    for i in colors:
        sorted.append(i[1])
    return sorted


def remove_alpha(color_code):
    """ removes the alpha channel from rgba or hsla """
    color_code = color_code.split(',')
    a = color_code[0].index('a')
    color_code[0] = color_code[0][:a] + color_code[0][a+1:]
    color_code.pop(-1)
    color_code = ",".join(color_code)
    color_code += ")"
    return color_code


def get_colors_from_gradient(gradient):
    """extract all color codes from gradient"""
    colors = []
    # use regex to pull all possible color codes first
    append_color_codes("hsl", gradient, colors)
    append_color_codes("rgb", gradient, colors)
    append_color_codes("hex", gradient, colors)
    append_color_codes("keywords", gradient, colors)

    return colors


def append_color_codes(type, code, color_list):
    if type == "hsl":
        colors = re.findall(colortools.hsl_all_forms_re, code)
    elif type == "rgb":
        colors = re.findall(colortools.rgb_all_forms_re, code)
    elif type == "hex":
        colors = re.findall(colortools.hex_regex, code)
    elif type == "keywords":
        words = re.findall(r"[+a-z+A-Z]*", code)
        colors = []
        for i in words:
            # regex captures non-strings, so we don't process if empty
            if i:
                i = i.strip().lower()
                is_keyword = keyword.is_a_keyword(i.strip(" "))
                if is_keyword:
                    colors.append(i)
    if colors:
        # strip each color code (if hex regex)
        colors = [i.strip(" ") for i in colors]
        color_list += colors


def is_required_selector(selector_type: str, selector: str) -> bool:
    """ checks selector to see if it's required type or not """
    pattern = regex_patterns[selector_type]
    return re.search(pattern, selector)


def get_number_required_selectors(selector_type: str, sheet: Stylesheet) -> int:
    """ returns # of a specific selector type in a stylesheet """
    count = 0
    pattern = regex_patterns[selector_type]
    for selector in sheet.selectors:
        matches = re.findall(pattern, selector)
        count += len(matches)
    # Loop through all nested @rules and count selectors
    for at_rule, rules in sheet.nested_at_rules.items():
        for rule in rules:
            matches = re.findall(pattern, rule.selector)
            count += len(matches)
    return count


def has_required_property(property: str, sheet: Stylesheet) -> bool:
    """ checks stylesheet for a particular property
        to see if it's there or not """
    has_property = False
    for rule in sheet.rulesets:
        for declaration in rule.declaration_block.declarations:
            if declaration.property == property:
                return True
    return has_property


if __name__ == "__main__":
    from . import clerk

    insane_gradient = """
    -moz-radial-gradient(0% 200%, ellipse cover,
    rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
    -webkit-radial-gradient(0% 200%, ellipse cover,
    rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
    -o-radial-gradient(0% 200%, ellipse cover,
    rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
    -ms-radial-gradient(0% 200%, ellipse cover,
    rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
    radial-gradient(0% 200%, ellipse cover, antiquewhite 10%,
    rgba(240, 205, 247,0) 40%),
    -moz-linear-gradient(top, rgba(169, 235, 206,.25) 0%,
    rgba(42,60,87,.4) 200%),
    -ms-linear-gradient(-45deg, #46ABA6 0%, #092756 200%),
    linear-gradient(-45deg, maroon 0%, #092756 200%)
    """

    insane_gradient = """
-moz-radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
-webkit-radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
-o-radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
-ms-radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
-moz-linear-gradient(top, rgba(169, 235, 206,.25) 0%,
rgba(42,60,87,.4) 200%),
-ms-linear-gradient(-45deg, #46ABA6 0%, #092756 200%)',
linear-gradient(-45deg, #46ABA6 0%, #092756 200%)'
"""
    results = process_gradient(insane_gradient)
    print(results)
    project_path = "projects/single-page/"
    css_path = project_path + "style.css"
    html_path = project_path + "index.html"
    css_code = clerk.file_to_string(css_path)
    html_code = clerk.file_to_string(html_path)

    styles = Stylesheet("style.css", css_code)
    color_rules = styles.color_rulesets
    for rule in color_rules:
        selector = rule.selector
        for declaration in rule.declaration_block.declarations:
            property = declaration.property
            value = declaration.value
