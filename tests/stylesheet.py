def split_by_partition(text, part):
    # base case
    if text.count(part) == 0:
        return [text, ]
    # recursive case
    else:
        text_tuple = text.partition(part)
        return [text_tuple[0], ] + split_by_partition(text_tuple[2], part)


nested_at_rules = (
    "@media",
    "@supports",
    "@document",
    "@page",
    "@font-face",
    "@keyframes",
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


class Stylesheet:
    def __init__(self, href, text, stylesheet_type="file"):
        self.__type = stylesheet_type
        self.__href = href
        self.text = text
        self.__nested_at_rules = []
        self.__rulesets = []
        self.comments = []
        self.minify()
        self.extract_comments()

    def minify(self):
        """ remove all whitespace, line returns, and tabs from text """
        self.text = minify_code(self.text)

    def extract_comments(self):
        comment_split_first_half = self.text.split("/*")
        comments = []

        for i in comment_split_first_half:
            if "*/" in i:
                comment = i.split("*/")
                comments.append("/*" + comment[0] + "*/")

        self.comments = comments


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


if __name__ == "__main__":
    import clerk

    # layout_css = clerk.file_to_string("tests/test_files/projects/large_project/css/layout.css")
    # layout_css = minify_code(layout_css)
    # rulesets = layout_css.split("}")
    # for rule in rulesets:
    #     rule = rule + ";"
    #     if "@" in rule:
    #         # remove any comments to left of @ rule
    #         at_rule = NestedAtRule(rule)

    # valid = "color: #336699;"
    # dec1 = Declaration(valid)
    # print(dec1.property)
    # print(dec1.value)
    # if dec1.is_valid:
    #     print("the declaration is valid")
    # else:
    #     print("The declaration is invalid")

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
    sheet = Stylesheet("tag", css_code)
    print(sheet.text)
