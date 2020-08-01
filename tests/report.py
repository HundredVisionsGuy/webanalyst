import clerk
import re
import HTMLinator as html


class Report:
    def __init__(self, dir_path):
        self.__readme_path = dir_path + "README.md"
        self.__readme_text = clerk.file_to_string(self.__readme_path)
        self.__readme_list = re.split("[\n]", self.__readme_text)
        self.__general_report = None
        self.__html_report = None
        self.__css_report = None
        self.__dir_path = dir_path

    def get_readme_text(self):
        return self.__readme_text

    def get_readme_list(self):
        return self.__readme_list

    def generate_report(self):
        # pull readme text
        self.get_readme_text()

        # instantiate all reports
        self.__general_report = GeneralReport(self.__readme_list,
                                              self.__dir_path)
        self.__html_report = HTMLReport(self.__readme_list,
                                        self.__dir_path)
        self.__css_report = CSSReport(self.__readme_list,
                                      self.__dir_path)

        # run each report
        self.__general_report.generate_report()


class GeneralReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.title = ""
        self.description = ""
        self.__readme_list = readme_list
        self.report_details = {
            "writing_goals": {
                "average_SPP": [1, 5],
                "average_WPS": [14, 20],
            },
            "writing_goal_results": {
                "actual_SPP": 0,
                "meets_SPP": False,
                "actual_WPS": 0,
                "meets_WPS": False,
            }
        }

    def generate_report(self):
        self.set_title()
        self.set_description()
        self.get_word_count()

    def get_report_details(self):
        return self.report_details

    def set_title(self):
        # extract title from the readme text (str)
        for i in self.__readme_list:
            if "Project Name:" in i:
                self.title = i
                break
        row_list = re.split(":", self.title)
        self.title = row_list[1].strip()

    def get_title(self):
        return self.title

    def set_description(self):
        # extract description from the readme text
        for i in self.__readme_list:
            if "***GOAL***" in i:
                self.description = i
                break
        row_list = re.split(":", self.description)
        self.description = row_list[1].strip()

    def get_description(self):
        return self.description

    def get_word_count(self):
        html_files = clerk.get_all_files_of_type(self.__dir_path, "html")
        paragraphs = []
        for file in html_files:
            paragraphs.append(html.get_elements("p", file))


class HTMLReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.html_level = "0"
        self.__readme_list = readme_list
        self.report_details = {
            "html_level": "",
            "html_level_attained": "",
            "min_num_required_files": 0,
            "meets_requirements": False
        }

    def get_html_level(self):
        # extract HTML level from readme_list
        for i in self.__readme_list:
            if "### HTML Level" in i:
                self.report_details["html_level"] = i
        row_list = re.split("=", self.report_details["html_level"])
        self.report_details["html_level"] = row_list[1].strip()
        return self.report_details["html_level"]


class CSSReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.html_level = "0"
        self.__readme_list = readme_list
        self.report_details = {
            "css_level": "",
            "css_level_attained": None,
            "min_num_required_files": 0,
            "meets_requirements": False
        }


if __name__ == "__main__":
    about_me_readme_path = "tests/test_files/projects/about_me/"

    about_report = Report(about_me_readme_path)
    about_report.generate_report()
    about_report.get_readme_text()
