import clerk
import re
import HTMLinator as html
from bs4 import BeautifulSoup
import logging
import validator as val

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

    @staticmethod
    def get_report_results_string(tr_class, type_column, target, results, results_key):
        results_key = str(results_key)
        if tr_class:
            results_string = '<tr class="' + tr_class + '">'
        else:
            results_string = '<tr>'
        results_string += '<td>' + type_column + '</td>'
        if target != "":
            results_string += '<td>' + str(target) + '</td>'
        if results != "":
            results_string += "<td>" + str(results) + "</td>"
        if results_key == "True":
            meets = "Meets"
        else:
            meets = "Does Not Meet"
        results_string += "<td>" + meets + "</td>"
        results_string += "</tr>"
        return results_string

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
        self.prep_report()
        self.general_report.generate_report()
        self.html_report.generate_report()
        # Get CSS validation and send to css report
        css_validation_results = self.html_report.validator_errors["CSS"]
        self.css_report.set_css_validation(css_validation_results)
        self.css_report.generate_report()

    def prep_report(self):
        # Create a report HTML file in the report folder
        report_template_content = clerk.file_to_string(report_template_path)
        with open('report/report.html', 'w') as f:
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

    def get_min_number_files(self, filetype):
        """ receives filetype and returns minimum # of that file"""
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
        try:
            SPP = len(self.sentences) / len(self.paragraphs)
        except ZeroDivisionError:
            SPP = 0
        self.report_details["writing_goal_results"]["actual_SPP"] = SPP

        # Is SPP within range?
        minSPP, maxSPP = self.report_details["writing_goals"]["average_SPP"]
        self.report_details["writing_goal_results"]["meets_SPP"] = SPP > minSPP and SPP < maxSPP

        # calculate words per sentence WPS
        try:
            WPS = self.word_count / self.get_num_sentences()
        except ZeroDivisionError:
            WPS = 0
        self.report_details["writing_goal_results"]["actual_WPS"] = WPS

        # Is WPS within range?
        min_wps, max_wps = self.report_details["writing_goals"]["average_WPS"]
        self.report_details["writing_goal_results"]["meets_WPS"] = WPS > min_wps and WPS < max_wps

    def publish_results(self):
        # Get report
        report_content = html.get_html(report_path)
        # report_content = report_template

        goals_details = self.report_details["min_number_files"]
        goals_results = self.report_details["num_files_results"]
        writing_goals = self.report_details["writing_goals"]
        writing_results = self.report_details["writing_goal_results"]

        # Modify table in section#general

        # Append the following tds
        # Min HTML files & Actual HTML files
        # Report.get_report_results_string()
        html_results_string = Report.get_report_results_string(
            "general-html-files-results", "HTML", goals_details['HTML'], self.num_html_files, goals_results['Meets HTML'])
        html_results_tag = BeautifulSoup(html_results_string, "html.parser")
        report_content.find(
            id="general-html-files-results").replace_with(html_results_tag)

        # Min CSS files & Actual CSS files
        css_results_string = Report.get_report_results_string(
            "general-css-files-results", "CSS",  goals_details['CSS'], self.num_css_files, goals_results['Meets CSS'])

        css_results_tag = BeautifulSoup(css_results_string, "html.parser")
        report_content.find(
            id="general-css-files-results").replace_with(css_results_tag)

        spp_results_string = Report.get_report_results_string("general-spp-results", "Avg. Sentences / Paragraph", str(
            writing_goals["average_SPP"]), writing_results["actual_SPP"], writing_results["meets_SPP"])
        spp_results_tag = BeautifulSoup(spp_results_string, "html.parser")
        report_content.find(
            id="general-spp-results").replace_with(spp_results_tag)

        wps_results_string = Report.get_report_results_string("general-wps-results", "Avg. Words / Sentence", str(
            writing_goals["average_WPS"]), writing_results["actual_WPS"], writing_results["meets_WPS"])
        wps_results_tag = BeautifulSoup(wps_results_string, "html.parser")
        report_content.find(
            id="general-wps-results").replace_with(wps_results_tag)

        # Save new HTML as report/general_report.html
        with open(report_path, 'w') as f:
            f.write(str(report_content.contents[2]))


class HTMLReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.html_level = "0"
        self.__readme_list = readme_list
        self.html_requirements_list = []
        self.html_files = []
        self.validator_errors = {}
        self.validator_warnings = {}
        self.report_details = {
            "html_level": "",
            "can_attain_level": False,
            "html_level_attained": None,
            "validator_goals": 0,
            "validator_results": {
                "CSS Errors": 0,
                "HTML Errors": 0
            },
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
        self.get_validator_goals()
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

    def get_validator_goals(self):
        """ gets number of validator errors allowed """
        readme_list = self.html_requirements_list[:]
        # Looking for Allowable Errors
        for line in readme_list:
            if "* Allowable Errors" in line:
                allowable_errors = re.search("[0-9]", line).group()
                self.report_details["validator_goals"] = int(allowable_errors)
                return int(allowable_errors)
            else:
                continue
        return 0

    def set_required_elements_found(self):
        # get a copy of the required elements
        required_elements = self.get_required_elements().copy()

        # remove the HTML5_essential_elements
        # that was already covered
        html_essential_elements = ["DOCTYPE", "HTML", "HEAD", "TITLE", "BODY"]
        for i in html_essential_elements:
            required_elements.remove(i)

        # iterate through each element and get the total number
        # then compare to required number
        for el in required_elements:
            actual_number = html.get_num_elements_in_folder(
                el, self.__dir_path)

            # get how many of that element is required
            number_required = self.report_details['required_elements'][el]

            # do we have enough of that element to meet?
            el_meets = actual_number >= number_required

            # modify the report details on required elements found
            self.report_details["required_elements_found"][el] = [
                number_required, actual_number, el_meets]

    def set_html5_required_elements_found(self):
        # Get HTML5_essential_elements
        html5_elements = self.report_details["required_elements"]["HTML5_essential_elements"].copy(
        )
        # get # of html files in folder - this is our multiplier
        for el in enumerate(html5_elements):
            element = el[1].lower()
            # how many were found
            number_found = html.get_num_elements_in_folder(
                element, self.__dir_path)
            number_required = self.report_details['required_elements']['HTML5_essential_elements'][element.upper(
            )]
            element_meets = number_found >= number_required

            self.report_details["required_elements_found"]["HTML5_essential_elements_found"][element.upper(
            )] = [number_required, number_found, element_meets]

    def meets_required_elements(self):
        all_elements_meet = True  # assume they meet until proved otherwise
        # Get all essential_elements
        html5_elements = self.report_details["required_elements"].copy(
        )
        html5_elements.pop('HTML5_essential_elements', None)
        # remove essential HTML5 elements
        print(html5_elements)
        # check all other tags to see if they meet - record whether each one meets individually
        for i in enumerate(html5_elements.items()):
            all_elements_meet = True
            key, min_value = i[1]
            actual_value = html.get_num_elements_in_folder(
                key, self.__dir_path)
            element_meets = actual_value >= min_value
            if not element_meets:
                all_elements_meet = False  # it just takes one not meeting
        return all_elements_meet

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
        self.html_level = self.report_details["html_level"]
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

    def validate_html(self):
        # create a dictionary with doc titles for keys
        # and num of errors for value

        # get titles and run them through validator
        for file_path in self.html_files:
            # Get error objects
            errors_in_file = val.get_markup_validity(file_path)
            # Get number of errors
            errors = len(errors_in_file)
            page_name = clerk.get_file_name(file_path)
            if errors > 0:
                self.process_errors(page_name, errors_in_file)

    def process_errors(self, page_name, errors):
        """ receives errors and records warnings and errors """
        errors_dict = {"HTML": {},
                       "CSS": {}}
        warnings_dict = {"HTML": {},
                         "CSS": {}}

        # Loop through all the errors and separate
        # error from warning and CSS from HTML
        # Must use try/except whenever adding an item
        # because it will crash if we try and append it
        # to a non-existant list
        for item in errors:
            if item["type"] == "error":
                if "CSS" in item["message"]:
                    self.report_details["validator_results"]["CSS Errors"] += 1
                    try:
                        errors_dict["CSS"][page_name].append(item)
                    except:
                        errors_dict["CSS"][page_name] = [item, ]
                else:
                    self.report_details["validator_results"]["HTML Errors"] += 1
                    try:
                        errors_dict["HTML"][page_name].append(item)
                    except:
                        errors_dict["HTML"][page_name] = [item, ]
            elif item["type"] == "info":
                if "CSS" in item["message"]:
                    try:
                        warnings_dict["CSS"][page_name].append(item)
                    except:
                        warnings_dict["CSS"][page_name] = [item, ]
                else:
                    try:
                        warnings_dict["HTML"][page_name].append(item)
                    except:
                        warnings_dict["HTML"][page_name] = [item, ]

        self.validator_errors = errors_dict
        self.validator_warnings = warnings_dict

    def analyze_results(self):
        self.can_attain_level()
        self.validate_html()
        self.set_html5_required_elements_found()
        self.set_required_elements_found()
        self.meets_required_elements()

    def publish_results(self):
        # Get report
        report_content = html.get_html(report_path)

        # HTML Overview Table
        html_overview_tr = self.get_html_overview_row()
        report_content.find(id="html-overview").replace_with(html_overview_tr)

        # Validation Report
        # HTML Validation
        # get the results of the validation as a string
        validation_results_string = self.get_validation_results_string('HTML')

        # create our tbody contents
        tbody_contents = BeautifulSoup(
            validation_results_string, "html.parser")
        tbody_id = 'html-validation'
        report_content.find(id=tbody_id).replace_with(tbody_contents)

        # CSS Validation
        # get the results of the validation as a string
        validation_results_string = self.get_validation_results_string('CSS')

        # create our tbody contents
        tbody_contents = BeautifulSoup(
            validation_results_string, "html.parser")
        tbody_id = 'css-validation'
        report_content.find(id=tbody_id).replace_with(tbody_contents)

        # Generate Error report
        # For HTML Errors
        error_report_contents = self.get_validator_error_report()
        tbody_contents = BeautifulSoup(error_report_contents, "html.parser")
        tr_id = "html-validator-errors"
        report_content.find(id=tr_id).replace_with(tbody_contents)

        # For CSS Errors
        error_report_contents = self.get_validator_error_report('CSS')
        tbody_contents = BeautifulSoup(error_report_contents, "html.parser")
        tr_id = "css-validator-errors"
        report_content.find(id=tr_id).replace_with(tbody_contents)

        html_goals_results = list(
            self.report_details["required_elements_found"].items())
        html5_goals_results = list(html_goals_results.pop(0)[1].items())

        html_elements_results_string = ""
        # we have to modify an entire tbody (not just a tr)
        tbody_id = "html-elements-results"
        for el in html5_goals_results:
            # get element, goal, actual, and results
            element = el[0]
            goal = el[1][0]
            actual = el[1][1]
            results = str(el[1][2])
            html_elements_results_string += Report.get_report_results_string(
                "", element, goal, actual, results)
        # add remaining elements
        for el in html_goals_results:
            # get element, goal, actual, and results
            element = el[0]
            goal = el[1][0]
            actual = el[1][1]
            results = el[1][2]
            html_elements_results_string += Report.get_report_results_string(
                "", element, goal, actual, results)
        ######
        ######
        # create our tbody contents
        tbody_contents = BeautifulSoup(
            html_elements_results_string, "html.parser")
        report_content.find(id=tbody_id).replace_with(tbody_contents)

        # Save new HTML as report/report.html
        with open(report_path, 'w') as f:
            f.write(str(report_content.contents[0]))

    def get_html_overview_row(self):
        # get a string version of can_attain_level
        can_attain = str(self.can_attain_level())
        html_overview_string = Report.get_report_results_string(
            "html-overview", self.html_level, can_attain, "", "")
        overview_row = BeautifulSoup(html_overview_string, "html.parser")
        return overview_row

    def get_validation_results_string(self, validation_type="HTML"):
        results = ""
        if not self.validator_errors:
            return '<tr><td rowspan="4">Congratulations! No Errors Found</td></tr>'
        else:
            validation_report = self.validator_errors[validation_type].copy()

            cumulative_errors = 0
            for page, errors in validation_report.items():
                num_errors = len(errors)
                error_str = str(num_errors) + " error"
                if num_errors != 1:
                    error_str += 's'
                cumulative_errors += num_errors
                cumulative_errors_string = str(
                    cumulative_errors) + " total errors"
                meets = str(cumulative_errors <=
                            self.report_details["validator_goals"])
                results += Report.get_report_results_string(
                    "", page, error_str, cumulative_errors_string, meets)
            return results

    def get_validator_error_report(self, validation_type="HTML"):
        results = ""
        if not self.validator_errors:
            # write 1 column entry indicating there are no errors
            congrats = "Congratulations, no errors were found."
            results = '<tr><td colspan="4">' + congrats + '</td></tr>'
            return results
        else:
            errors_dict = self.validator_errors[validation_type]
            tr_class = "html-validator-errors"

            for page, errors in errors_dict.items():
                for error in errors:
                    message = error['message']

                    # clean message of smart quotes for HTML rendering
                    message = message.replace('“', '"').replace('”', '"')
                    last_line = error['lastLine']
                    try:
                        first_line = error['firstLine']
                    except:
                        first_line = last_line
                    last_column = error['lastColumn']
                    first_column = error['firstColumn']

                    # render any HTML code viewable on the screen
                    extract = error['extract'].replace(
                        "<", "&lt;").replace(">", "&gt;")

                    # place extract inside of a code tag
                    extract = "<code>" + extract + "</code>"

                    location = 'From line {}, column {}; to line {}, column {}.'.format(first_line,
                                                                                        first_column, last_line, last_column)

                    new_row = Report.get_report_results_string(
                        tr_class, page, message, location, extract)
                    new_row = new_row.replace("Meets", extract)
                    results += new_row
        return results

    def extract_el_from_dict_key_tuple(self, the_dict):
        """ converts all keys from a tuple to 2nd item in tuple """
        new_dict = {}
        for t, i in the_dict.items():
            new_dict[t[1]] = i
        return new_dict


class CSSReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.html_level = "0"
        self.__readme_list = readme_list
        self.font_families_used = []
        self.min_num_css_files = 0
        self.max_num_css_files = 0
        self.css_errors = {}
        self.css_files = []
        self.style_tag_contents = []
        self.report_details = {
            "css_level": "",
            "css_level_attained": False,
            "css_validator_goals": 0,
            "css_validator_results": {},
            "num_css_files": 0,
            "num_style_tags": 0,
            "repeat_selectors": 0,
            "repeat_declaration_blocks": 0,
            "general_css_styles": {
                "font_families": {
                    "min": 0,
                    "max": 0,
                    "actual": 0,
                },
                "color_goals": {
                    "entire_page": False,
                    "headers": False,
                    "color_contrast": False
                },
                "color_settings": {
                    "page_background_set": False,
                    "page_color_set": False,
                    "headers_background_set": False,
                    "headers_color_set": False,
                    "page_contrast_rating": "Fail",
                    "headers_contrast_rating": "Fail"
                }
            },
            "project_specific_goals": {},
            "project_specific_results": {},
            "meets_requirements": False
        }

    def set_css_validation(self, css_validation_results):
        self.report_details['css_validator_results'] = css_validation_results
        self.report_details['css_validator_errors'] = len(
            css_validation_results)

    def generate_report(self):
        self.get_num_css_files()
        self.get_num_style_tags()
        self.get_css_code()
        self.validate_css()

    def get_num_css_files(self):
        css_files = clerk.get_all_files_of_type(self.__dir_path, 'css')
        num_css_files = len(css_files)
        self.report_details["num_css_files"] = num_css_files
        return num_css_files

    def get_num_style_tags(self):
        # get HTML files
        html_files = clerk.get_all_files_of_type(self.__dir_path, 'html')
        count = 0
        for file in html_files:
            style_tags = html.get_elements("style", file)
            count += len(style_tags)
        self.report_details["num_style_tags"] = count
        return count

    def get_css_code(self):
        # extract content from all CSS files
        self.css_files = clerk.get_all_files_of_type(self.__dir_path, "css")
        for file in self.css_files:
            try:
                self.style_tag_contents.append(
                    clerk.get_css_from_stylesheet(file))
            except:
                print("Something went wrong witht the stylesheet code")

        # extract CSS from all style tags
        html_files = clerk.get_all_files_of_type(self.__dir_path, "html")
        for file in html_files:
            try:
                self.style_tag_contents.append(
                    clerk.get_css_from_style_tag(file))
            except:
                print("No style tag in this file")

    def validate_css(self):
        # Get CSS validation on CSS files
        errors = 0
        for file_path in self.css_files:
            # Get code (just run it all)
            css_code = clerk.file_to_string(file_path)
            # Get error objects
            errors_in_file = val.validate_css(css_code)
            # Get number of errors
            errors += len(errors_in_file)
            page_name = clerk.get_file_name(file_path)
        # Validate style tag contents
        self.validate_style_tag_contents(self.style_tag_contents)
        if errors > 0:
            self.process_errors(page_name, errors_in_file)

    def validate_style_tag_contents(self, contents):
        for item in contents:
            css_errors = val.validate_css(item)
            print(css_errors)

    def process_errors(self, page_name, errors):
        """ receives errors and records warnings and errors """
        errors_dict = {}
        warnings_dict = {}

        # Loop through all the errors and separate
        # error from warning
        # Must use try/except whenever adding an item
        # because it will crash if we try and append it
        # to a non-existant list
        for item in errors:
            if item["type"] == "error":
                self.report_details["css_validator_errors"] += 1
                try:
                    errors_dict[page_name].append(item)
                except:
                    errors_dict[page_name] = [item, ]
            elif item["type"] == "info":
                try:
                    warnings_dict[page_name].append(item)
                except:
                    warnings_dict[page_name] = [item, ]

        self.report_details["css_validator_results"][page_name] = errors_dict[page_name]
        self.report_details["css_validator_results"][page_name] += warnings_dict[page_name]


if __name__ == "__main__":
    # How to run a report:
    # 1. Set the path to the folder:    path = "path/to/project/folder"
    # 2. Create a report object:        project_name = Report(path)
    # 3. Generate a report:             project_name.generate_report()
    # 4. Go to report/report.html for results

    # about_me_dnn_readme_path = "tests/test_files/projects/about_me_does_not_meet/"
    # project = Report(about_me_dnn_readme_path)
    # project.generate_report()

    # large_project_readme_path = "tests/test_files/projects/large_project/"
    # # large_project = Report(large_project_readme_path)
    # # large_project.generate_report()

    readme_path = "project/"
    project = Report(readme_path)
    project.generate_report()
