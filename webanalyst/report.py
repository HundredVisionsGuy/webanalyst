import logging
import re

from bs4 import BeautifulSoup

from . import CSSReport
from . import HTMLinator as html
from . import HTMLReport, clerk

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S"
)
report_template_path = "webanalyst/report_template.html"
report_path = "report/report.html"


class Report:
    def __init__(self, dir_path):
        self.__readme_path = dir_path + "README.md"
        self.__readme_text = clerk.file_to_string(self.__readme_path)
        self.__readme_list = re.split("[\n]", self.__readme_text)
        self.general_report = None
        self.html_report = None
        self.css_report = None
        self.__dir_path = dir_path

    def get_readme_text(self):
        return self.__readme_text

    def get_readme_list(self):
        return self.__readme_list

    @staticmethod
    def get_report_results_string(
        tr_class, type_column, target, results, results_key
    ):
        results_key = str(results_key)
        if tr_class:
            results_string = '<tr class="' + tr_class + '">'
        else:
            results_string = "<tr>"
        results_string += "<td>" + type_column + "</td>"
        if target != "":
            results_string += "<td>" + str(target) + "</td>"
        if results != "":
            results_string += "<td>" + str(results) + "</td>"
        if results_key == "True":
            meets = "Meets"
        else:
            meets = "Does Not Meet"
        results_string += "<td>" + meets + "</td>"
        results_string += "</tr>"
        return results_string

    @staticmethod
    def get_header_details(header_string):
        header_list = header_string.split(":")
        title = header_list[0]
        title = title.strip()
        if "* " in title[:]:
            title = title[2:]
        description = header_list[1]
        return {
            "title": title,
            "details": {"description": description.strip()},
        }

    @staticmethod
    def foo():
        pass

    def generate_report(self):
        # pull readme text
        self.get_readme_text()

        # instantiate all reports
        self.general_report = GeneralReport(
            self.__readme_list, self.__dir_path
        )
        self.html_report = HTMLReport.HTMLReport(
            self.__readme_list, self.__dir_path
        )
        self.css_report = CSSReport.CSSReport(
            self.__readme_list, self.__dir_path
        )

        # run each report
        self.prep_report()
        self.general_report.generate_report()
        self.html_report.generate_report()

        # send linked stylesheets to css report
        self.css_report.linked_stylesheets = (
            self.html_report.linked_stylesheets
        )

        # Get CSS validation and send to css report
        try:
            css_validation_results = self.html_report.validator_errors["CSS"]
        except KeyError:
            css_validation_results = {}
        self.css_report.set_css_validation(css_validation_results)
        self.css_report.generate_report(self.html_report.html_files)

    def prep_report(self):
        # Create a report HTML file in the report folder
        report_template_content = clerk.file_to_string(report_template_path)
        with open("report/report.html", "w") as f:
            f.write(report_template_content)


class GeneralReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.title = ""
        self.description = ""
        self.paragraphs = []
        self.sentences = []
        self.word_count = 0
        self.__readme_list = readme_list
        self.num_html_files = 0
        self.num_css_files = 0
        self.words_per_sentence = 0.0
        self.sentences_per_paragraph = 0.0
        self.report_details = {
            "min_number_files": {
                "HTML": None, 
                "CSS": None},
            "num_files_results": {
                "Meets HTML": False, 
                "Meets CSS": False},
            "writing_goals": {
                "average_SPP": [1, 5],
                "average_WPS": [10, 20],
            },
            "writing_goal_results": {
                "actual_SPP": 0,
                "meets_SPP": False,
                "actual_WPS": 0,
                "meets_WPS": False,
            },
        }

    def generate_report(self):
        self.set_title()
        self.set_description()
        self.set_paragraphs()
        self.set_sentences()
        self.set_word_count()
        self.set_min_number_files()
        self.analyze_results()
        self.publish_results()

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

    def set_min_number_files(self):
        min_html_files = 0
        min_css_files = 0
        for row in self.__readme_list:
            if "* [HTML]" in row:
                num = re.search(r"[0-9]+", row)
                if num:
                    min_html_files = num.group(0)
            if "* [CSS]" in row:
                num = re.search(r"[0-9]+", row)
                if num:
                    min_css_files = num.group(0)

        self.report_details["min_number_files"]["HTML"] = int(min_html_files)
        self.report_details["min_number_files"]["CSS"] = int(min_css_files)

    def get_min_number_files(self, filetype):
        """receives filetype and returns minimum # of that file"""
        if filetype.lower() == "html":
            return self.report_details["min_number_files"]["HTML"]
        elif filetype.lower() == "css":
            return self.report_details["min_number_files"]["CSS"]
        else:
            return "NA"

    def set_paragraphs(self):
        html_files = clerk.get_all_files_of_type(self.__dir_path, "html")
        for file in html_files:
            if not self.paragraphs:
                self.paragraphs = list(html.get_elements("p", file))
            else:
                try:
                    # get list of any p elements
                    paragraphs = html.get_elements("p", file)
                    # then loop through and append each
                    for p in enumerate(paragraphs):
                        self.paragraphs.append(p[1])
                except Exception:
                    print("We have a problem")

    def get_paragraphs(self):
        return self.paragraphs

    def set_word_count(self):
        for p in self.paragraphs:
            self.word_count += self.get_num_words(p)

    def get_word_count(self):
        return self.word_count

    def get_num_words(self, element):
        # Get words from element
        words = html.get_element_content(element)

        # Get a word count
        word_list = words.split()
        return len(word_list)

    def set_sentences(self):
        sentence_list = self.paragraphs
        paragraphs = ""
        for i in enumerate(sentence_list):
            p = clerk.remove_tags(str(i[1]))
            p = p.strip()
            paragraphs += p
        self.sentences = clerk.split_into_sentences(paragraphs)

    def get_num_sentences(self):
        return len(self.sentences)

    def meets_num_html_files(self):
        # compare actual number of files to min
        # number of files.
        self.num_html_files = len(
            clerk.get_all_files_of_type(self.__dir_path, "html")
        )
        min_required = self.report_details["min_number_files"]["HTML"]
        self.report_details["num_files_results"]["Meets HTML"] = (
            self.num_html_files >= min_required
        )

    def meets_num_css_files(self):
        self.num_css_files = len(
            clerk.get_all_files_of_type(self.__dir_path, "css")
        )
        min_required = self.report_details["min_number_files"]["CSS"]
        self.report_details["num_files_results"]["Meets CSS"] = (
            self.num_css_files >= min_required
        )

    def analyze_results(self):
        # Does it meet min file requirements?
        self.meets_num_html_files()
        self.meets_num_css_files()

        # calculate WPS and SPP
        try:
            SPP = len(self.sentences) / len(self.paragraphs)
        except ZeroDivisionError:
            SPP = 0
        self.report_details["writing_goal_results"]["actual_SPP"] = SPP

        # Is SPP within range?
        minSPP, maxSPP = self.report_details["writing_goals"]["average_SPP"]
        self.report_details["writing_goal_results"]["meets_SPP"] = (
            SPP >= minSPP and SPP <= maxSPP
        )

        # calculate words per sentence WPS
        try:
            WPS = self.word_count / self.get_num_sentences()
        except ZeroDivisionError:
            WPS = 0
        self.report_details["writing_goal_results"]["actual_WPS"] = WPS

        # Is WPS within range?
        min_wps, max_wps = self.report_details["writing_goals"]["average_WPS"]
        self.report_details["writing_goal_results"]["meets_WPS"] = (
            WPS > min_wps and WPS < max_wps
        )

    def publish_results(self):
        # Get report
        report_content = html.get_html(report_path)

        goals_details = self.report_details["min_number_files"]
        goals_results = self.report_details["num_files_results"]
        writing_goals = self.report_details["writing_goals"]
        writing_results = self.report_details["writing_goal_results"]

        # Modify table in section#general

        # Append the following tds
        # Min HTML files & Actual HTML files
        html_results_string = Report.get_report_results_string(
            "general-html-files-results",
            "HTML",
            goals_details["HTML"],
            self.num_html_files,
            goals_results["Meets HTML"],
        )
        html_results_tag = BeautifulSoup(html_results_string, "html.parser")
        report_content.find(id="general-html-files-results").replace_with(
            html_results_tag
        )

        # Min CSS files & Actual CSS files
        css_results_string = Report.get_report_results_string(
            "general-css-files-results",
            "CSS",
            goals_details["CSS"],
            self.num_css_files,
            goals_results["Meets CSS"],
        )

        css_results_tag = BeautifulSoup(css_results_string, "html.parser")
        report_content.find(id="general-css-files-results").replace_with(
            css_results_tag
        )

        spp_results_string = Report.get_report_results_string(
            "general-spp-results",
            "Avg. Sentences / Paragraph",
            str(writing_goals["average_SPP"]),
            writing_results["actual_SPP"],
            writing_results["meets_SPP"],
        )

        spp_results_tag = BeautifulSoup(spp_results_string, "html.parser")
        report_content.find(id="general-spp-results").replace_with(
            spp_results_tag
        )

        wps_results_string = Report.get_report_results_string(
            "general-wps-results",
            "Avg. Words / Sentence",
            str(writing_goals["average_WPS"]),
            writing_results["actual_WPS"],
            writing_results["meets_WPS"],
        )
        wps_results_tag = BeautifulSoup(wps_results_string, "html.parser")
        report_content.find(id="general-wps-results").replace_with(
            wps_results_tag
        )

        # Save new HTML as report/general_report.html
        with open(report_path, "w") as f:
            f.write(str(report_content.contents[2]))


if __name__ == "__main__":
    # How to run a report:
    # 1. Set the path to the folder:    path = "path/to/project/folder"
    # 2. Create a report object:        project_name = Report(path)
    # 3. Generate a report:             project_name.generate_report()
    # 4. Go to report/report.html for results

    about_me_dnn_readme_path = (
        "tests/test_files/projects/about_me_does_not_meet/"
    )

    large_project_readme_path = "tests/test_files/projects/large_project/"
    single_page_path = "tests/test_files/projects/single_page/"

    # project path
    responsive_nav_path = "projects/responsive-navbar/"
    project_path = "projects/single-page/"
    project_page = Report(responsive_nav_path)
    project_page.generate_report()
    print(project_page.general_report)
