import logging
import re

from bs4 import BeautifulSoup

from . import HTMLinator as html
from . import clerk
from . import report as rep
from . import validator as val

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S"
)
report_template_path = "webanalyst/report_template.html"
report_path = "report/report.html"


class HTMLReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.html_level = "0"
        self.__readme_list = readme_list
        self.html_requirements_list = []
        self.html_files = []
        self.linked_stylesheets = {}
        self.style_tags = []
        self.validator_errors = {"HTML": {}, "CSS": {}}
        self.validator_warnings = {"HTML": {}, "CSS": {}}
        self.report_details = {
            "html_level": "",
            "can_attain_level": False,
            "html_level_attained": None,
            "validator_goals": 0,
            "uses_inline_styles": False,
            "validator_results": {"CSS Errors": 0, "HTML Errors": 0},
            "num_html_files": 0,
            "required_elements": {
                "HTML5_essential_elements": {
                    "DOCTYPE": 1,
                    "HTML": 1,
                    "HEAD": 1,
                    "TITLE": 1,
                    "BODY": 1,
                },
            },
            "required_elements_found": {
                "HTML5_essential_elements_found": {},
            },
            "meets_required_elements": {
                "meets_HTML5_essential_elements": False,
                "meets_other_essential_elements": False,
            },
            "meets_requirements": False,
        }

    def generate_report(self):
        self.get_html_files_list()
        self.get_html_requirements_list()
        self.get_html_level()
        self.get_validator_goals()
        self.ammend_required_elements()
        self.set_linked_stylesheets()
        self.analyze_results()
        self.publish_results()

    def get_html_files_list(self):
        self.html_files = clerk.get_all_files_of_type(self.__dir_path, "html")
        return self.html_files

    def get_required_elements(self):
        # get a list of all required elements: the keys
        required_elements = []
        for element in enumerate(
            self.report_details["required_elements"].keys()
        ):
            if element[1] == "HTML5_essential_elements":
                for nested_el in enumerate(
                    self.report_details["required_elements"][
                        "HTML5_essential_elements"
                    ].keys()
                ):
                    required_elements.append(nested_el[1])
            else:
                required_elements.append(element[1])
        return required_elements

    def get_validator_goals(self):
        """gets number of validator errors allowed"""
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
            double_el = ""
            if "or" in el:
                # we have 2 elements and either may work
                # split the two elements and check each 1 at a time
                # if one meets, they both meet (or else they don't)
                actual_number = 0
                double_el = el
                my_elements = el.split("`")
                for i in my_elements:
                    if "or" in i:
                        continue
                    actual_number += html.get_num_elements_in_folder(
                        i, self.__dir_path
                    )
                el = my_elements[0] + "` or `" + my_elements[-1]
            else:
                actual_number = html.get_num_elements_in_folder(
                    el, self.__dir_path
                )

            # get how many of that element is required
            number_required = self.report_details["required_elements"][el]

            # do we have enough of that element to meet?
            el_meets = actual_number >= number_required

            # edit the el if it has two by removing the back tics `
            if double_el:
                el = el.replace("`", "")

            # modify the report details on required elements found
            self.report_details["required_elements_found"][el] = [
                number_required,
                actual_number,
                el_meets,
            ]

    def set_html5_required_elements_found(self):
        # Get HTML5_essential_elements
        html5_elements = self.report_details["required_elements"][
            "HTML5_essential_elements"
        ].copy()
        # get # of html files in folder - this is our multiplier
        for el in enumerate(html5_elements):
            element = el[1].lower()
            # how many were found
            number_found = html.get_num_elements_in_folder(
                element, self.__dir_path
            )
            number_required = self.report_details["required_elements"][
                "HTML5_essential_elements"
            ][element.upper()]
            # there must be 1 for each page
            number_required = len(self.html_files)
            element_meets = number_found == number_required

            self.report_details["required_elements_found"][
                "HTML5_essential_elements_found"
            ][element.upper()] = [number_required, number_found, element_meets]

    def meets_required_elements(self):
        all_elements_meet = True  # assume they meet until proved otherwise
        # Get all essential_elements
        html5_elements = self.report_details["required_elements"].copy()
        html5_elements.pop("HTML5_essential_elements", None)
        # remove essential HTML5 elements
        print(html5_elements)
        # check all other tags to see if they meet -
        # record whether each one meets individually
        for i in enumerate(html5_elements.items()):
            all_elements_meet = True
            key, min_value = i[1]
            actual_value = html.get_num_elements_in_folder(
                key, self.__dir_path
            )
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
                description = self.__readme_list[i + 1]
                break
        self.report_details["can_attain_level"] = "does meet" in description
        return "does meet" in description

    def ammend_required_elements(self):
        """adds remaining required HTML elements"""
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
            num_errors = len(errors_in_file)
            page_name = clerk.get_file_name(file_path)
            if num_errors > 0:
                self.process_errors(page_name, errors_in_file)

    def process_errors(self, page_name, errors):
        """receives errors and records warnings and errors"""
        errors_dict = {"HTML": {}, "CSS": {}}
        warnings_dict = {"HTML": {}, "CSS": {}}

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
                    except Exception as e:
                        errors_dict["CSS"][page_name] = [
                            item,
                        ]
                        print("We have an exception: " + str(e))
                else:
                    self.report_details["validator_results"][
                        "HTML Errors"
                    ] += 1
                    try:
                        errors_dict["HTML"][page_name].append(item)
                    except Exception as e:
                        errors_dict["HTML"][page_name] = [
                            item,
                        ]
                        print("We have an exception " + str(e))
            elif item["type"] == "info":
                if "CSS" in item["message"]:
                    try:
                        warnings_dict["CSS"][page_name].append(item)
                    except Exception as e:
                        warnings_dict["CSS"][page_name] = [
                            item,
                        ]
                        print("We have an exception " + str(e))
                else:
                    try:
                        warnings_dict["HTML"][page_name].append(item)
                    except Exception as e:
                        warnings_dict["HTML"][page_name] = [
                            item,
                        ]
                        print("We have an exception " + str(e))
            elif item["type"] == "alert":
                try:
                    warnings_dict["HTML"][page_name].append(item)
                except Exception as e:
                    warnings_dict["HTML"][page_name] = [
                        item,
                    ]
                    print("We have an exception " + str(e))

        self.augment_errors(
            errors_dict
        )  # we might need to change to a function
        self.add_warnings(warnings_dict)

    def augment_errors(self, new_dict):
        """appends any errors from a dict to validator errors"""
        for page, errors in new_dict["HTML"].items():
            self.validator_errors["HTML"][page] = errors

    def add_warnings(self, warnings):
        for page, warning in warnings["HTML"].items():
            self.validator_warnings["HTML"][page] = warning

    def add_errors(self, errors):
        for page, error in errors["HTML"].items():
            self.validator_errors[page] = error

    def analyze_results(self):
        self.can_attain_level()
        self.validate_html()
        self.set_html5_required_elements_found()
        self.set_required_elements_found()
        self.meets_required_elements()
        self.meets_html5_essential_requirements()
        self.check_for_inline_styles()

    def publish_results(self):
        # Get report
        report_content = html.get_html(report_path)

        # HTML Overview Table
        html_overview_tr = self.get_html_overview_row()
        report_content.find(id="html-overview").replace_with(html_overview_tr)

        # Validation Report
        # HTML Validation
        # get the results of the validation as a string
        validation_results_string = self.get_validation_results_string("HTML")

        # create our tbody contents
        tbody_contents = BeautifulSoup(
            validation_results_string, "html.parser"
        )
        tbody_id = "html-validation"
        report_content.find(id=tbody_id).replace_with(tbody_contents)

        # CSS Validation
        # get the results of the validation as a string
        validation_results_string = self.get_validation_results_string("CSS")

        # create our tbody contents
        tbody_contents = BeautifulSoup(
            validation_results_string, "html.parser"
        )
        tbody_id = "css-validation"
        report_content.find(id=tbody_id).replace_with(tbody_contents)

        # Generate Error report
        # For HTML Errors
        error_report_contents = self.get_validator_error_report()
        tbody_contents = BeautifulSoup(error_report_contents, "html.parser")
        tr_id = "html-validator-errors"
        report_content.find(id=tr_id).replace_with(tbody_contents)

        # For CSS Errors
        error_report_contents = self.get_validator_error_report("CSS")
        tbody_contents = BeautifulSoup(error_report_contents, "html.parser")
        tr_id = "css-validator-errors"
        report_content.find(id=tr_id).replace_with(tbody_contents)

        html_goals_results = list(
            self.report_details["required_elements_found"].items()
        )
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
            html_elements_results_string += (
                rep.Report.get_report_results_string(
                    "", element, goal, actual, results
                )
            )
        # add remaining elements
        for el in html_goals_results:
            # get element, goal, actual, and results
            element = el[0]
            goal = el[1][0]
            actual = el[1][1]
            results = el[1][2]
            html_elements_results_string += (
                rep.Report.get_report_results_string(
                    "", element, goal, actual, results
                )
            )
        ######
        ######
        # create our tbody contents
        tbody_contents = BeautifulSoup(
            html_elements_results_string, "html.parser"
        )
        report_content.find(id=tbody_id).replace_with(tbody_contents)

        # Save new HTML as report/report.html
        with open(report_path, "w") as f:
            f.write(str(report_content.contents[0]))

    def get_html_overview_row(self):
        # get a string version of can_attain_level
        can_attain = str(self.can_attain_level())
        html_overview_string = rep.Report.get_report_results_string(
            "html-overview", self.html_level, can_attain, "", ""
        )
        overview_row = BeautifulSoup(html_overview_string, "html.parser")
        return overview_row

    def get_validation_results_string(self, validation_type="HTML"):
        results = ""
        if not self.validator_errors.get("HTML"):
            return '<tr><td rowspan="4">Congratulations! No Errors Found</td></tr>'
        else:
            try:
                validation_report = self.validator_errors[
                    validation_type
                ].copy()
            except Exception as e:
                print("Whoah Nelly")
                print("We have an exception " + str(e))
            cumulative_errors = 0
            for page, errors in validation_report.items():
                num_errors = len(errors)
                error_str = str(num_errors) + " error"
                if num_errors != 1:
                    error_str += "s"
                cumulative_errors += num_errors
                cumulative_errors_string = (
                    str(cumulative_errors) + " total errors"
                )
                meets = str(
                    cumulative_errors <= self.report_details["validator_goals"]
                )
                results += rep.Report.get_report_results_string(
                    "", page, error_str, cumulative_errors_string, meets
                )
            return results

    def get_validator_error_report(self, validation_type="HTML"):
        results = ""
        if not self.validator_errors:
            # write 1 column entry indicating there are no errors
            congrats = "Congratulations, no errors were found."
            results = '<tr><td colspan="4">' + congrats + "</td></tr>"
            return results
        else:
            errors_dict = self.validator_errors[validation_type]
            tr_class = "html-validator-errors"

            for page, errors in errors_dict.items():
                for error in errors:
                    message = error["message"]

                    # clean message of smart quotes for HTML rendering
                    message = message.replace("“", '"').replace("”", '"')
                    last_line = error["lastLine"]
                    try:
                        first_line = error["firstLine"]
                    except Exception as e:
                        first_line = last_line
                        print("We have an exception " + str(e))
                    last_column = error["lastColumn"]
                    try:
                        first_column = error["firstColumn"]
                    except Exception as e:
                        first_column = last_column
                        print("We have an exception " + str(e))
                    # render any HTML code viewable on the screen
                    extract = (
                        error["extract"]
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    )

                    # place extract inside of a code tag
                    extract = "<code>" + extract + "</code>"

                    location = "From line {}, column {}; to line {}, column {}.".format(
                        first_line, first_column, last_line, last_column
                    )

                    new_row = rep.Report.get_report_results_string(
                        tr_class, page, message, location, extract
                    )
                    new_row = new_row.replace("Meets", extract)
                    results += new_row
        return results

    def extract_el_from_dict_key_tuple(self, the_dict):
        """converts all keys from a tuple to 2nd item in tuple"""
        new_dict = {}
        for t, i in the_dict.items():
            new_dict[t[1]] = i
        return new_dict

    def meets_html5_essential_requirements(self):
        required_elements = self.report_details["required_elements_found"][
            "HTML5_essential_elements_found"
        ]
        for element in required_elements.values():
            if not element[-1]:
                return False
        return True

    def set_linked_stylesheets(self):
        """will generate a list of HTML docs and the CSS they link to"""
        linked = {}
        # loop through html_files
        # in each file get the href of any link if that
        # href matches a file in the folder
        for file in self.html_files:
            contents = clerk.file_to_string(file)
            link_hrefs = clerk.get_linked_css(contents)
            filename = clerk.get_file_name(file)
            linked[filename] = link_hrefs
        self.linked_stylesheets = linked

    def check_for_inline_styles(self):
        files_with_inline_styles = []
        for file in self.html_files:
            markup = clerk.file_to_string(file)
            has_inline_styles = html.uses_inline_styles(markup)
            if has_inline_styles:
                filename = clerk.get_file_name(file)
                files_with_inline_styles.append(filename)

        self.report_details["uses_inline_styles"] = files_with_inline_styles
