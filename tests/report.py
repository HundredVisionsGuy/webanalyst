import clerk


class Report:
    def __init__(self):
        self.__readme_text = ""
        self.__title = ""
        self.__author = ""
        self.__description = ""
        self.__report_details = {}

    def set_readme_text(self, readme_path):
        # Pull readme contents and place into a string or list (not sure)
        self.__readme_text = clerk.file_to_string(readme_path)

    def get_readme_text(self):
        return self.__readme_text

    def set_title(self, readme):
        # extract title from the readme text (str)
        self.__title = "generic title"

    def get_title(self):
        return self.__title


if __name__ == "__main__":
    # create a Report object
    report = Report()
    print(f"A report is sitting in memory at {report}")
    report.set_title("hello")
    print(f"The title of the report is {report.get_title()}")
