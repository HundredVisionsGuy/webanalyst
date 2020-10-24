import clerk
import re
import HTMLinator as html
from bs4 import BeautifulSoup
import logging

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
report_template_path = "tests/report_template.html"
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

    def generate_report(self):
        # pull readme text
        self.get_readme_text()

        # instantiate all reports
        self.general_report = GeneralReport(self.__readme_list,
                                            self.__dir_path)
        self.html_report = HTMLReport(self.__readme_list,
                                      self.__dir_path)
        self.css_report = CSSReport(self.__readme_list,
                                    self.__dir_path)

        # run each report
        self.general_report.generate_report()


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
                "CSS": None
            },
            "num_files_results": {
                "Meets HTML": False,
                "Meets CSS": False
            },
            "writing_goals": {
                "average_SPP": [1, 5],
                "average_WPS": [10, 20],
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
                num = re.search(r'[0-9]+', row)
                if num:
                    min_html_files = num.group(0)
            if "* [CSS]" in row:
                num = re.search(r'[0-9]+', row)
                if num:
                    min_css_files = num.group(0)

        self.report_details["min_number_files"]["HTML"] = int(min_html_files)
        self.report_details["min_number_files"]["CSS"] = int(min_css_files)

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
                except:
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
            clerk.get_all_files_of_type(self.__dir_path, "html"))
        min_required = self.report_details["min_number_files"]["HTML"]
        self.report_details["num_files_results"]["Meets HTML"] = self.num_html_files >= min_required

    def meets_num_css_files(self):
        self.num_css_files = len(
            clerk.get_all_files_of_type(self.__dir_path, "css"))
        min_required = self.report_details["min_number_files"]["CSS"]
        self.report_details["num_files_results"]["Meets CSS"] = self.num_css_files >= min_required

    def analyze_results(self):
        # Does it meet min file requirements?
        self.meets_num_html_files()
        self.meets_num_css_files()

        # calculate WPS and SPP
        SPP = len(self.sentences) / len(self.paragraphs)
        self.report_details["writing_goal_results"]["actual_SPP"] = SPP

        # Is SPP within range?
        minSPP, maxSPP = self.report_details["writing_goals"]["average_SPP"]
        self.report_details["writing_goal_results"]["meets_SPP"] = SPP > minSPP and SPP < maxSPP

        # calculate words per sentence WPS
        WPS = self.word_count / self.get_num_sentences()
        self.report_details["writing_goal_results"]["actual_WPS"] = WPS

        # Is WPS within range?
        min_wps, max_wps = self.report_details["writing_goals"]["average_WPS"]
        self.report_details["writing_goal_results"]["meets_WPS"] = WPS > min_wps and WPS < max_wps

    def publish_results(self):
        # Get report_template
        report_template = html.get_html(report_template_path)
        report_content = report_template

        goals_details = self.report_details["min_number_files"]
        goals_results = self.report_details["num_files_results"]
        writing_goals = self.report_details["writing_goals"]
        writing_results = self.report_details["writing_goal_results"]

        # Modify table in section#general
        
        # Append the following tds
        # Min HTML files & Actual HTML files
        html_results_string = self.get_report_results_string("general-html-files-results", "HTML", goals_details['HTML'], self.num_html_files, goals_results['Meets HTML'])
        html_results_tag = BeautifulSoup(html_results_string,features="lxml")
        report_content.find(id="general-html-files-results").replace_with(html_results_tag)
        
        # Min CSS files & Actual CSS files
        css_results_string = self.get_report_results_string("general-css-files-results", "CSS",  goals_details['CSS'], self.num_css_files, goals_results['Meets CSS'])
        
        css_results_tag = BeautifulSoup(css_results_string, features="lxml")
        report_content.find(id="general-css-files-results").replace_with(css_results_tag)
        
        spp_results_string = self.get_report_results_string("general-spp-results", "Avg. Sentences / Paragraph", str(writing_goals["average_SPP"]), writing_results["actual_SPP"], writing_results["meets_SPP"])
        spp_results_tag = BeautifulSoup(spp_results_string, features="lxml")
        report_content.find(id="general-spp-results").replace_with(spp_results_tag)

        wps_results_string = self.get_report_results_string("general-wps-results", "Avg. Words / Sentence", str(writing_goals["average_WPS"]), writing_results["actual_WPS"], writing_results["meets_WPS"])
        wps_results_tag = BeautifulSoup(wps_results_string, features="lxml")
        report_content.find(id="general-wps-results").replace_with(wps_results_tag)

        # Save new HTML as report/report.html
        with open('report/report.html', 'w') as f:
            f.write(str(report_content.contents[2]))
        
    def get_report_results_string(self, tr_id, type_column, target, results, results_key):
        results_string = '<tr id="'+ tr_id + '">'
        results_string += '<td>' + type_column + '</td>'
        results_string += '<td>' + str(target) + '</td>'
        results_string += "<td>" + str(results) + "</td>"
        meets = "Does Not Meet"
        if results_key:
            meets = "Meets"
        else:
            meets = "Does Not Meet"
        results_string += "<td>" + meets + "</td></tr>"
        return results_string

class HTMLReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.html_level = "0"
        self.__readme_list = readme_list
        self.html_requirements_list = []
        self.html_files = []
        self.report_details = {
            "html_level": "",
            "can_attain_level": False,
            "html_level_attained": None,
            "min_num_required_files": 0,
            "num_html_files": 0,
            "required_elements": {
                "HTML5_essential_elements": {
                    "DOCTYPE": 1,
                    "HTML": 1,
                    "HEAD": 1,
                    "TITLE": 1,
                    "BODY": 1
                },
            },
            "required_elements_found": {
                "HTML5_essential_elements_found": {},
            },
            "meets_required_elements": {
                "meets_HTML5_essential_elements": False,
                "meets_other_essential_elements": False},
            "meets_requirements": False
        }

    def generate_report(self):
        self.get_html_files_list()
        self.get_html_requirements_list()
        self.get_html_level()
        self.ammend_required_elements()
        self.analyze_results()
        self.publish_results()

    def get_html_files_list(self):
        self.html_files = clerk.get_all_files_of_type(self.__dir_path, "html")
        return self.html_files

    def get_required_elements(self):
        # get a list of all required elements: the keys
        required_elements = []
        for element in enumerate(self.report_details["required_elements"].keys()):
            if element[1] == "HTML5_essential_elements":
                for nested_el in enumerate(self.report_details["required_elements"]["HTML5_essential_elements"].keys()):
                    required_elements.append(nested_el[1])
            else:
                required_elements.append(element[1])
        return required_elements

    def set_required_elements_found(self):
        # get a copy of the required elements
        required_elements = self.get_required_elements().copy()

        # remove the HTML5_essential_elements 
        # that was already covered
        html_essential_elements = ["DOCTYPE", "HTML", "HEAD", "TITLE", "BODY"]
        for i in html_essential_elements:
            required_elements.remove(i)
        # iterate through each element and get the total number
        for el in enumerate(required_elements):
            num = html.get_num_elements_in_folder(el[1], self.__dir_path)
            # add the element and its number to required_elements_found
            self.report_details["required_elements_found"][el] = num
        

    def set_html5_required_elements_found(self):
        # Get HTML5_essential_elements
        html5_elements = self.report_details["required_elements"]["HTML5_essential_elements"].copy(
        )
        # get # of html files in folder - this is our multiplier
        for el in enumerate(html5_elements):
            key = el[1].lower()
            # val is how many were found
            val = html.get_num_elements_in_folder(key, self.__dir_path)
            self.report_details["required_elements_found"]["HTML5_essential_elements_found"][key.upper(
            )] = val

    def meets_html5_essential_requirements(self):
        # Get HTML5_essential_elements
        html5_elements = self.report_details["required_elements"]["HTML5_essential_elements"].copy(
        )
        # get # of html files in folder - this is our multiplier
        num_files = len(self.get_html_files_list())
        for el in enumerate(html5_elements):
            key = el[1]
            val = html.get_num_elements_in_folder(key, self.__dir_path)
            # if each element has exactly the number of required elements, it passes
            if val != num_files:
                return False
        # all must pass or no pass
        # any failures and return False
        # otherwise, return True
        return True

    def meets_required_elements(self):
        # Get all essential_elements
        html5_elements = self.report_details["required_elements"].copy(
        )
        html5_elements.pop('HTML5_essential_elements', None)
        # remove essential HTML5 elements
        print(html5_elements)
        # check all other tags to see if they meet
        for i in enumerate(html5_elements.items()):
            key, min_value = i[1]
            print("Key = {} Val = {}".format(key, min_value))
            val = html.get_num_elements_in_folder(key, self.__dir_path)
            if val < min_value:
                return False
        return True

    def check_element_for_required_number(self, file_path, element, min_num):
        num_elements = html.get_num_elements_in_file(element, file_path)
        return num_elements >= min_num

    def get_html_requirements_list(self):
        h_req_list = []
        # create a flag to switch On when in the HTML section and off
        # when that section is over (### CSS)
        correct_section = False
        for row in enumerate(self.__readme_list):
            # 1st row in the section should be ### HTML
            if row[1] == "### HTML":
                # it's the beginning of the correct section
                correct_section = True
            if row[1] == "### CSS":
                break
            if correct_section:
                h_req_list.append(row[1])

        self.html_requirements_list = h_req_list
        return self.html_requirements_list

    def get_html_level(self):
        # extract HTML level from readme_list
        for i in self.__readme_list:
            if "### HTML Level" in i:
                self.report_details["html_level"] = i
                break
        row_list = re.split("=", self.report_details["html_level"])
        self.report_details["html_level"] = row_list[1].strip()
        return self.report_details["html_level"]

    def get_num_html_files(self):
        html_files = clerk.get_all_files_of_type(self.__dir_path, "html")
        return len(html_files)

    def can_attain_level(self):
        # Determine whether or not this project is enough
        # to qualify to meet the level
        description = ""
        for i in range(len(self.__readme_list)):
            row = self.__readme_list[i]
            if "### HTML Level" in row:
                # set description to next row (after the header)
                description = self.__readme_list[i+1]
                break
        self.report_details["can_attain_level"] = "does meet" in description
        return "does meet" in description

    def ammend_required_elements(self):
        """ adds remaining required HTML elements """
        # extract all elements and their minimum #
        # using a regex to capture the pattern: `EL` : ##
        ptrn = r"((`(.*)`\s*):(\s*\d*))"
        for i in self.html_requirements_list:
            if "`DOCTYPE`" in i:
                # skip the row with required HTML 5 elements
                continue
            match = re.search(ptrn, i)
            if match:
                key, val = match.group(2, 4)
                key = key.strip()[1:-1]
                # add key and value to required elements
                self.report_details["required_elements"][key] = int(val)
        

    def get_report_details(self):
        return self.report_details
        
    def analyze_results(self):
        self.can_attain_level()
        self.set_html5_required_elements_found()
        self.set_required_elements_found()
        self.meets_required_elements()

    def publish_results(self):
        pass

    def get_report_results_string(self):
        return ""

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

    def get_num_css_files(self):
        css_files = clerk.get_all_files_of_type(self.__dir_path, 'css')
        return len(css_files)

    def get_num_style_tags(self):
        # get HTML files
        html_files = clerk.get_all_files_of_type(self.__dir_path, 'html')
        count = 0
        for file in html_files:
            style_tags = html.get_elements("style", file)
            count += len(style_tags)
        return count


if __name__ == "__main__":
    about_me_readme_path = "tests/test_files/projects/about_me/"
    large_project_readme_path = "tests/test_files/projects/large_project/"
    # large_project = Report(large_project_readme_path)
    # large_project.generate_report()
    # large_project.get_readme_text()

    # Create about_me report
    about_me_report = Report(about_me_readme_path)
    about_me_report.generate_report()
    about_me_report.html_report.generate_report()
    about_me_report.html_report.get_required_elements()
    about_me_report.html_report.meets_html5_essential_requirements()
    print(about_me_report.html_report.get_report_details())
    # # about_me_report.html_report.generate_report()
    # num_sentences = about_me_report.general_report.get_num_sentences()
    # about_me_report.html_report.get_html_requirements_list()
    # about_me_report.html_report.ammend_required_elements()
    # print(num_sentences)
    # # get required elements
    # about_me_report.html_report.set_required_elements_found()
    # about_me_report.html_report.generate_report()
    # about_me_report.html_report.meets_html5_essential_requirements()
    # # test clerk
    # paragraph = "Hello, you! How are you? i am fine Mr. selenium.\nsee ya later."
    # list_of_ps = clerk.split_into_sentences(paragraph)
    # for i in list_of_ps:
    #     print(i)

    # can_attain = about_me_report.html_report.can_attain_level()
    # print(f"It is {can_attain} that this project can attain the level.")

    # html_list = about_me_report.html_report.get_html_requirements_list()
