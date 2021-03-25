
class Stylesheet:
    def __init__(self, href, text, stylesheet_type = "file"):
        self.__type = stylesheet_type
        self.__href = href
        self.__text = text
        self.__rulesets = []
        self.__at_rules = []
        self.__comments = []
        
        
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

    def get_property(self):
        return self.property

    def get_value(self):
        return self.value

    def validate_declaration(self):
        # Check to see if there's only 1 character in value
        # 0 is valid; anything else is invalid
        if len(self.value) == 1 and not self.value == "0":
            self.is_valid = False

        # Make sure there are no spaces in between property or value
        prop_list = self.property.split()
        if len(prop_list) > 1:
            self.is_valid = False

        val_list = self.value.split()
        if len(val_list) > 1:
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
        self.declarations = declarations
        


if __name__ == "__main__":
    invalid = "property:val; something"
    dec1 = Declaration(invalid)
    print(dec1.property)
    print(dec1.value)
    if dec1.is_valid:
        print("the declaration is valid")
    else:
        print("The declaration is invalid")

    declaration_block_with_selector = """
article#gallery {
    display: flex;
    flex-wrap: wrap;
    width: 96vw;
    margin: 0 auto;
}
"""
    block = DeclarationBlock(declaration_block_with_selector)
    print(block.declarations)
    invalid_css = """
body }
    background: #efefef;
    color: #101010;

"""
    ruleset = Ruleset(invalid_css)
    print(ruleset.is_valid)
    ruleset2 = Ruleset(declaration_block_with_selector)