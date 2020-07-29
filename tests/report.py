import clerk
import re


class Report:
    def __init__(self, readme_path):
        self.__readme_text = clerk.file_to_string(readme_path)
        self.__readme_list = re.split("[\n]", self.__readme_text)
        self.title = ""
        self.author = ""
        self.description = ""
        self.report_details = {
            "html_level": "",
            "css_level": "",
            "num_files": {
                "html": 0,
                "css": 0,
            },
            "writing_goals": {
                "average_WPS": [14, 20],
                "actual_WPS": 0,
                "meets_WPS": False,
                "average_SPP": [1, 5],
                "actual_SPP": 0,
                "meets_SPP": False
            },
            "html_requirements": {},
            "css_requirements": {}
        }

    def get_readme_text(self):
        return self.__readme_text

    def set_title(self):
        # extract title from the readme text (str)
        for i in self.__readme_list:
            if "Project Name:" in i:
                self.title = i
        row_list = re.split(":", self.title)
        self.title = row_list[1].strip()

    def get_title(self):
        return self.title

    def set_description(self):
        # extract description from the readme text
        for i in self.__readme_list:
            if "***GOAL***" in i:
                self.description = i
        row_list = re.split(":", self.description)
        self.description = row_list[1].strip()

    def get_description(self):
        return self.description

    def get_html_level(self):
        # extract HTML level from readme_list
        for i in self.__readme_list:
            if "### HTML Level" in i:
                self.report_details["html_level"] = i
        row_list = re.split("=", self.report_details["html_level"])
        self.report_details["html_level"] = row_list[1].strip()
        return self.report_details["html_level"]
