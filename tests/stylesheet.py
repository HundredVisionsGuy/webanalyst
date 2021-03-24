
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
        self.__selector = ""
        self.__declaration_block = ""
        self.__declarations = []
        self.__properties = []
        self.__values = []

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

    def get_property(self):
        return self.property

    def get_value(self):
        return self.value

if __name__ == "__main__":
    valid1 = "color: #336699;"
    dec1 = Declaration(valid1)
    print(dec1.property)
    print(dec1.value)
    if dec1.is_valid:
        print("the declaration is valid")
    else:
        print("The declaration is invalid")