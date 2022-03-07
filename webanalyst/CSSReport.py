from fileinput import filename
import keyword
from webanalyst import CSSinator
from webanalyst import clerk
import re
from webanalyst import HTMLinator as html
from bs4 import BeautifulSoup
import logging
from webanalyst import validator as val
import os
from webanalyst.CSSinator import Stylesheet as stylesheet
from webanalyst import stylesheet_analyst as css_analyst
import webanalyst.report as rep
import webanalyst.colortools as colors
import webanalyst.color_keywords as keywords

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
report_template_path = "webanalyst/report_template.html"
report_path = "report/report.html"


class CSSReport:
    def __init__(self, readme_list, dir_path):
        self.__dir_path = dir_path
        self.html_level = "0"
        self.readme_list = readme_list
        self.html_files = []
        self.project_css_by_html_file = {}
        self.font_families_used = []
        self.min_num_css_files = 0
        self.max_num_css_files = 0
        self.css_errors = {}
        self.css_files = []
        self.style_tag_contents = []
        self.num_style_tags = 0
        self.linked_stylesheets = {}
        self.order_of_css_by_file = {}
        self.pages_contain_same_css_files = False
        self.repeat_selectors = {}
        self.repeat_declarations_blocks = {}
        self.set_readme_list()
        self.stylesheet_objects = []
        self.report_details = {
            "css_level": "",
            "css_level_attained": False,
            "css_validator_goals": 0,
            "css_validator_results": {},
            "num_css_files": 0,
            "style_tags": [],
            "repeat_selectors": 0,
            "repeat_declaration_blocks": 0,
            "general_styles_goals": {},
            "standard_requirements_goals": {},
            "standard_requirements_results": {},
            "project_specific_goals": {},
            "project_specific_results": {},
            "meets_requirements": False
        }

    def set_css_validation(self, css_validation_results):
        self.report_details['css_validator_results'] = css_validation_results
        self.css_errors.update(css_validation_results)
        self.report_details['css_validator_errors'] = len(
            css_validation_results)

    def generate_report(self, html_files):
        self.html_files = html_files
        self.get_project_css_by_file(html_files)
        self.get_order_of_css_by_file(html_files)
        self.get_num_css_files()
        self.get_style_tags()
        self.get_num_style_tags()
        self.get_css_code()
        self.check_pages_for_same_css_files()
        self.set_repeat_selectors()
        self.validate_css()
        self.set_repeat_declaration_blocks()
        self.get_standard_requirements()
        self.get_standard_requirements_results()
        self.get_general_styles_goals()
        self.get_general_styles_results()
        self.publish_results()

    def get_general_styles_goals(self):
        try:
            start = self.readme_list.index("* General Styles:") + 1
        except ValueError:
            # There's no general styles goals
            warning = "There's no General Styles Goals in README."
            warning += "Look into it."
            logging.warn(warning)
            return
        if "* Project-specific Requirements:" in self.readme_list:
            stop = self.readme_list.index("* Project-specific Requirements:")
        else:
            stop = len(self.readme_list)

        # take a slice in between for reqs
        requirements = self.readme_list[start:stop]
        details = {}
        for req in requirements:
            if '    * Font Families' in req:
                response = rep.Report.get_header_details(req)
                details = response
            elif '+ minimum' in req.lower() or '+ min' in req.lower():
                min = req.split(":")[1].strip()
                details["details"]["minimum"] = min
            elif '+ maximum' in req.lower() or '+ max' in req.lower():
                max = req.split(":")[1].strip()
                details["details"]["maximum"] = max
            elif '* color settings' in req.lower():
                # If we had already gathered requirements,
                # Let's add them before clearing them out for the next round
                if details:
                    # add details to report_details
                    item = details.pop("title")
                    self.report_details["general_styles_goals"][item] = details

                    # reset details
                    details = {"Color Settings": {}}

            elif '+ entire page colors set' in req.lower():
                description, title = self.get_title_and_description(req)
                details['Color Settings']['details'] = {
                    'description': req.strip()
                    }
                (self.report_details["general_styles_goals"]
                    ['Color Settings']) = details['Color Settings']
            elif '+ headers' in req.lower():
                description, title = self.get_title_and_description(req)
                details["Color Settings"][title] = description
            elif '+ color contrast' in req.lower():
                description, title = self.get_title_and_description(req)
                details["Color Settings"][title] = {"description": description}
            elif '- normal' in req.lower():
                description, title = self.get_title_and_description(req)
                details["Color Settings"]['Color Contrast (readability)'][title] = description
            elif '- large' in req.lower():
                description, title = self.get_title_and_description(req)
                (details["Color Settings"]
                    ['Color Contrast (readability)'][title]) = description
        self.report_details["general_styles_goals"]["Color Settings"] = details["Color Settings"]

    def get_title_and_description(self, req):
        full_details = req.split(": ")
        title = full_details[0].strip()[2:]
        description = full_details[1].strip()
        return description, title

    def get_general_styles_results(self):
        goals = list(self.report_details['general_styles_goals'].items())
        all_styles_in_order = self.get_all_styles_in_order()

        for goal, details in goals:
            if goal == "Font Families":
                # get actual # of font families and compare to range (min max)
                font_families = self.get_font_families()
                font_count = self.get_font_count(font_families)
                min = int(details['details']['minimum'])
                max = int(details['details']['maximum'])
                meets = font_count >= min and font_count <= max
                self.report_details['general_styles_goals']['Font Families']['details']['actual'] = str(font_count)
                self.report_details['general_styles_goals']['Font Families']['details']['meets'] = meets
            elif goal == "Color Settings":
                color_settings_results = ""

                # Check for global colors 
                needs_global_colors = self.needs_global_colors_set()
                global_colors = []
                if needs_global_colors:
                    # We have all styles in order let's check for global
                    # are they set?
                    global_colors = self.get_final_global_colors(all_styles_in_order)
                    global_colors_results = self.get_global_colors_results(global_colors)
                    color_settings_results += global_colors_results

                # check for headers
                print("Refactoring stopped here. ")

                # check for color contrast
                color_rulesets = self.get_color_data()
                passes_page_colors = self.meets_page_colors(details)
                if not color_rulesets:
                    actual = "We still need this piece of functionality"
                else:
                    actual = str(color_rulesets)
                self.report_details['general_styles_goals']['Color Settings']['details']['actual'] = actual
                self.report_details['general_styles_goals']['Color Settings']['details']['meets'] = passes_page_colors
                print(passes_page_colors)

    def get_global_colors_results(self, global_colors):
        """ Are global colors set for each HTML file? """
        results = ""
        num_files = len(self.html_files)
        num_global_set = len(global_colors)
        global_filenames = []
        for i in global_colors:
            global_filenames.append(i.get('file'))
        
        # Check to see if all HTML files have global colors set
        if num_global_set < num_files:
            results += "Fail: not all files have global colors applied.\n"
            for file in self.html_files:
                filename = file.split("\\")[-1]
                if filename not in global_filenames:
                    results += "File: " + filename + " has no global colors set.\n"

        # Were any global styles missing a declaration (color or bg-color):
        for setting in global_colors:
            color_set = setting.get('color')
            if not color_set:
                results += "Fail: in " + setting.get('file') 
                results += " the color property was not set.\n"
            bg_color_set = setting.get('bg-color')
            if not bg_color_set:
                results += "Fail: in " + setting.get('file') 
                results += " the background-color property was not set.\n"

        # If no results, there were no problems
        if not results:
            results = "Global Colors Set: " 
            results += "Success! All files had global colors set.\n"
            return results
        else:
            results = "Global Colors Set: " + results
            return results

    def needs_global_colors_set(self):
        """ returns whether global colors should be set """
        general_styles_goals = self.report_details.get('general_styles_goals')
        if general_styles_goals:
            color_settings = general_styles_goals.get('Color Settings')
            if color_settings:
                description = color_settings.get('details')
                if "Entire Page" in description.get('description'):
                    return True

        return False

    def get_color_data(self):
        """ Initialize background & foreground to white & black
            Get background & foreground colors for:
            * global styles
            * headers
            * anchors (default is blue and purple for hover)
            * any other selectors
            If any declarations leave out color or background-color, use the global setting
            NOTE: we will NOT worry about the context (like applying inheritance of an li from ul). That's beyond my paygrade
        """
        color_data = self.set_color_data_defaults()

        # TODO:
        # Check all stylesheet objects for color_rulesets
        color_rulesets = []
        all_styles = self.get_all_styles_in_order()

        # Override any stylesheet rulesets with matching styletag rulesets
        # we may also have to check specificity
        global_color_errors = ""
        global_colors = self.get_final_global_colors(all_styles)
        num_html_files = len(self.html_files)
        num_files_colors_set = len(global_colors)
        if num_files_colors_set < num_html_files:
            global_color_errors += "Global colors not set on all pages\n"
        global_color_contrast = self.get_global_color_contrast(global_colors)
        
    def get_global_color_contrast(self, global_colors):
        results = ""
        for file in global_colors:
            color = file.get('color')
            color = self.get_color_hex(color)
            if "warning" in color.lower():
                results += "WARNING for " + file['file'] + ": "
                results += color 
                continue
            bg_color = file.get('bg-color')
            bg_color = self.get_color_hex(bg_color)
            if "warning" in bg_color.lower():
                results += "WARNING for " + file['file'] + ": "
                results += color
                continue
            # Test for contrast
            contrast_report = colors.get_color_contrast_report(color, bg_color)
            results += "Results for " + file['file'] + ": "
            
            contrast_goal = self.get_color_contrast_goals("global", "")
            results += self.process_contrast_report(contrast_report)

        return results
    
    def get_color_contrast_goals(self, type="global"):
        # TODO: double check to see if this is even necessary
        general_styles = self.report_details.get('general_styles_goals')
        color_settings = general_styles.get('Color Settings')
        contrast = color_settings.get('Color Contrast (readability)')
        if type == "global":
            return "Normal"
        

    def process_contrast_report(self, report):
        """ checks to see if passes at best level or not """
        results = ""
        if report['normal AAA'] == 'Pass':
            results = "Success: Page passes at AAA rating for "
            results += "normal sized font.\n"
        elif report['normal AA'] == 'Pass':
            results = "Caution: Page passes at AA rating for normal "
            results += "sized font (not AAA).\n"
        elif report['large AAA'] == 'Pass':
            results = "Failed: Page only passes at large sized font "
            results += "at a AAA rating. It's okay for headers, but "
            results += "not for paragraphs and other non-headings.\n"
        elif report['large AA'] == 'Pass':
            results = "Failed: Page only passes at large sized font "
            results += "at a AA rating. It's only okay for large headers, "
            results += "but not for paragraphs and other non-headings.\n"
        else:
            results = "Failed: Text contrast does not pass for large "
            results += "or small text. You need a higher contrast between "
            results += "the background and foreground colors."
        return results
            

    def get_color_hex(self, color):
        color_hex = ""
        if "#" in color:
            color_hex = color
        elif keywords.is_a_keyword(color):
            color_hex = keywords.get_hex_by_keyword(color)
        elif "rgb" in color:
            color_hex = colors.rgb_to_hex(color)
        elif "hsl(" in color:
            hsl = colors.get_hsl_from_string(color)
            rgb = colors.hsl_to_rgb(hsl)
            color_hex = colors.rgb_to_hex(rgb)
        elif "hsla(" in color[0]:
            hsla = colors.get_hsl_from_string(color)
            a = hsla[-1]
            if len(hsla) == 4 and a < 1:
                results = "Warning: you are using HSLA with "
                results += "transparency applied. We cannot "
                results += "test contrast with transparency applied.\n"
                return results
            elif len(hsla) == 4 and a == 1:
                rgb = colors.hsl_to_rgb(color[:-1])
                color_hex = colors.rgb_to_hex(rgb)
        return color_hex

    def get_all_styles_in_order(self):
        """ returns each stylesheet object in order of appearance """
        # whether that's a styletag or external stylesheet
        all_styles = []
        
        # loop through CSS by file
        for file in self.order_of_css_by_file.keys():
            for item in self.order_of_css_by_file[file]:
                if item == 'style tag':
                    # get the stylesheet
                    styletag = self.get_styletag_object(file)
                    if styletag:
                        all_styles.append((file, styletag))
                else:
                    stylesheet = self.get_stylesheet_object(item)
                    if stylesheet:
                        all_styles.append((file, stylesheet))

        return all_styles

    def get_styletag_object(self, file):
        for styletag in self.style_tag_contents:
            if styletag.href in file:
                return styletag
        return None

    def get_stylesheet_object(self, item):
        for object in self.stylesheet_objects:
            if object.href in item:
                return object
        return None

    def get_final_global_colors(self, all_styles):
        """ get global colors from each stylesheet and each style tag """
        # track which stylesheets have already been checked, 
        # so there are no repetitions
        styles_checked = self.get_styles_checked(all_styles)

        # get global styles from only the styles that are checked 
        # so no duplicates
        global_color_data = {}
        for styles in styles_checked.values():
            global_colors_set = CSSinator.get_global_color_details(styles.rulesets)
            if global_colors_set:
                # we have global colors set - let's do something:
                global_color_data[styles.href] = global_colors_set
        print(global_color_data)
        # TODO: Process to determine whether and which files have global 
        applied_styles = []
        for page in self.html_files:
            filename = page.split("\\")[-1]
            # initialize applied_styles for each page
            applied = {
                "file": filename,
                "applied": False,
                "selector": "",
                "specificity": "",
                "bg-color": "",
                "color": ""
            }
            for styles in all_styles:
                if filename in styles[0]:
                    href = styles[1].href
                    if href in global_color_data.keys():
                        details = global_color_data[href]
                        applied = self.adjust_applied(applied, details) 
                    elif styles[0] == styles[1].href:
                        print("it must be a style tag in the page")
            if applied['applied']:
                applied_styles.append(applied)
            
        return applied_styles
    
    def adjust_applied(self, old_styles, new_styles):
        """ returns old_styles adjusted according to new styles """
        old_styles['applied']=True
        for style in new_styles:
            new_selector = style['selector']
            old_selector = old_styles['selector']
            if old_selector:
                # we need to adjust all that applies
                # if selectors are the same OR 
                # old specificity is greater than new, we keep
                # all old styles unless not set
                new_specificity = CSSinator.get_specificity(new_selector)
                if new_specificity >= old_styles['specificity']:
                    # new wins out for everything present
                    old_styles['selector'] = style['selector']
                    old_styles['specificity'] = new_specificity
                    if style.get('background-color'):
                        old_styles['bg-color'] = style['background-color']
                    elif style.get('background'):
                        old_styles['bg-color'] = style['background']
                    if style.get('color'):
                        old_styles['color'] = style['color']
                else:
                    # old specificity is greater, so only apply anything not set
                    if not old_styles['bg-color']:
                        if style.get('background-color'):
                            old_styles['bg-color'] = style['background-color']
                        elif style.get('background'):
                            old_styles['bg-color'] = style['background']
                    if not old_styles['color'] and style.get('color'):
                        old_styles['color'] = style['color']

            else:
                # this is the first time, get all styles and apply
                old_styles['selector'] = style['selector']
                old_styles['specificity'] = CSSinator.get_specificity(old_selector)
                if style.get('background-color'):
                    old_styles['bg-color'] = style['background-color']
                elif style.get('background'):
                    old_styles['bg-color'] = style['background']
                if style.get('color'):
                    old_styles['color'] = style['color']
                print()
        return old_styles

    def get_styles_checked(self, all_styles):
        styles_checked = {}
        for page, styles in all_styles:
            stylename = None
            if ".html" in styles.href:
                # it's a styletag
                stylename = page + " - styletag"
            else:
                stylename = styles.href
            if stylename not in styles_checked.keys():
                styles_checked[stylename] = styles
        return styles_checked

    def set_color_data_defaults(self):
        default_colors = {
            "color": "#000000",
            "background": "#ffffff"
            }
        general_data = {
            "specificity": 1,
            "colors": {},
            "contrast": ""
            }
        global_colors = {"name": "global",
                         "selector": "body"}
        anchor_defaults = {"color": "#0000ff",
                           "background": "#ffffff"}
        color_data = {
            "global": {},
            "headers": {},
            "anchors": {},
            "others": {}
        }
        general_data["colors"] = default_colors
        color_data["global"] = global_colors.copy()
        color_data["headers"] = general_data.copy()
        color_data["anchors"] = general_data.copy()
        color_data["anchors"]["colors"] = anchor_defaults
        return color_data


    def meets_page_colors(self, goals):
        meets = False
        try:
            if goals['Entire Page colors set'] == "background and foreground":
                for sheet in self.style_tag_contents:
                    if sheet.color_rulesets:
                        if self.are_background_and_foreground_set(sheet):
                            return True
                for sheet in self.stylesheet_objects:
                    if sheet.color_rulesets:
                        if self.are_background_and_foreground_set(sheet):
                            return True
            return meets
        except:
            print("We have an exception most likely with the key for goals.")
            return False
    
           
    def are_background_and_foreground_set(self, sheet):
        for rule in sheet.color_rulesets:
            if rule.selector in ('body', 'html'):
                if "background-color:" in rule.declaration_block.text and rule.declaration_block.text.count("color") > 1:
                    # both are set
                    print(rule.declaration_block.text)
                    return True
    
    
    def get_font_count(self, font_families):
        # Make sure there are no duplicates
        for font in font_families:
            num = font_families.count(font)
            if num > 1:
                font_families.pop(font)
        return len(font_families)


    def get_font_families(self):
        font_families = []
        rulesets = []
        for declaration in self.style_tag_contents:
            families = self.get_families(declaration)
            if families:
                for fam in families:
                    font_families.append(fam)
        for declaration in self.stylesheet_objects:
            families = self.get_families(declaration)
            if families:
                for fam in families:
                    font_families.append(fam)
        return font_families


    def get_families(self, declaration):
        families = []
        for ruleset in declaration.rulesets:
            for declaration in ruleset.declaration_block.declarations:
                if declaration.property in ("font", "font-family"):
                    families.append(declaration.value)
        return families


    def get_standard_requirements(self):
        # get index position of Standard Req and General Styles headers
        try:
            start = self.readme_list.index("* Standard Requirements:") + 1
        except ValueError:
            # there's no Standard Requirements
            logging.warn("There's no Standard Requirements in README? Is that intentional? Typo?")
            return
        if "* General Styles:" in self.readme_list:
            stop = self.readme_list.index("* General Styles:")
        elif "* Project-specific Requirements:" in self.readme_list:
            stop = self.readme_list.index("* Project-specific Requirements:")
        else:
            stop = len(self.readme_list)
        # take a slice in between for reqs
        requirements = self.readme_list[start:stop]

        # get each req and put into standard reqs dictionary
        for req in requirements:
            req = req.strip()
            split_req = req.split(":", 1)
            description = split_req[0][2:]
            goal_raw = split_req[1]
            min = 0
            if '0' in goal_raw or 'None' in goal_raw:
                max = 0
            else:
                max = re.findall(r'\d+', split_req[1])
                max = int(max[0])

            # add requirements to dictionary
            self.report_details['standard_requirements_goals'][description]={"min": min, "max": max}


    def get_standard_requirements_results(self):
        errors = self.get_css_errors()
        self.get_standard_requirements_results_by_key(errors, "CSS Errors")

        repeats = len(list(self.repeat_selectors.keys()))
        self.get_standard_requirements_results_by_key(repeats, "Repeat selectors")
         
        repeats = len(list(self.repeat_declarations_blocks.keys()))
        self.get_standard_requirements_results_by_key(repeats, "Repeat declaration blocks")
   
   
    def get_standard_requirements_results_by_key(self, results, key):
        range = self.report_details["standard_requirements_goals"][key]
        min = range["min"]
        max = range["max"]
        passed = results >= min and results <= max
        if passed:
            results = "Passed"
        else:
            results = "Failed"
        
        self.report_details["standard_requirements_results"][key] = results


    def get_css_errors(self):
        number = 0
        for errors in self.css_errors.values():
            if errors != "No errors":
                number += len(errors)
        return number


    def set_repeat_selectors(self):
        all_selectors = []
        # get the names of all linked stylesheets
        linked_stylesheets = self.get_linked_stylesheets()
        filenames = self.get_filenames_from_paths(linked_stylesheets)
        implemented_selectors = self.get_implemented_selectors(all_selectors, filenames)
        # sort then get repeated selectors (if any)
        all_selectors.sort()
        self.get_repeated_selectors(all_selectors, implemented_selectors)


    def get_repeated_selectors(self, all_selectors, implemented_selectors):
        for selector in all_selectors:
            count = all_selectors.count(selector)
            if count > 1:
                # get the stylesheets that "own" the selector
                for page in implemented_selectors.keys():
                    if selector in implemented_selectors[page]:
                        pages = self.repeat_selectors.get(selector)
                        if not pages:
                            self.repeat_selectors[selector] = [page, ]
                        elif page not in pages:
                            self.repeat_selectors[selector].append(page) 
                        else:
                            # At this point, only append if we have not yet matched the number of pages to the count
                            if len(self.repeat_selectors[selector]) < count:    
                                self.repeat_selectors[selector].append(page)
                       
                # sort the pages
                self.repeat_selectors[selector].sort()


    def get_implemented_selectors(self, all_selectors, filenames):
        implemented_selectors = self.get_selectors_from_implemented_stylesheets(all_selectors, filenames)
        # get selectors from style_tag_contents
        self.get_selectors_from_style_tags(all_selectors, implemented_selectors)
        return implemented_selectors


    def get_selectors_from_style_tags(self, all_selectors, implemented_selectors):
        for stylesheet in self.style_tag_contents:
            for selector in stylesheet.selectors:
                all_selectors.append(selector)
                try:
                    implemented_selectors[stylesheet.href].append(selector)
                except KeyError:
                    implemented_selectors[stylesheet.href] = [selector,]


    def get_selectors_from_implemented_stylesheets(self, all_selectors, filenames):
        implemented_selectors = {}
        for stylesheet_object in self.stylesheet_objects:
            if stylesheet_object.href in filenames:
                for selector in stylesheet_object.selectors:
                    if (selector, stylesheet_object.href) not in all_selectors:
                        all_selectors.append(selector)
                        try:
                            implemented_selectors[stylesheet_object.href].append(selector)
                        except KeyError:
                            implemented_selectors[stylesheet_object.href] = [selector,]
        return implemented_selectors


    def get_filenames_from_paths(self, linked_stylesheets):
        filenames = []
        for filename in linked_stylesheets:
            filename = clerk.get_file_name(filename)
            filenames.append(filename)
        return filenames


    def set_repeat_declaration_blocks(self):
        # no repeat blocks (per page)
        # any repeat blocks from a style tag?
        declaration_blocks = self.get_all_declaration_blocks()
        # just_blocks = list(declaration_blocks.keys())
        for block, sheets in declaration_blocks.items():
            count = len(sheets)
            if count > 1:
                self.repeat_declarations_blocks[block]= sheets


    def get_all_declaration_blocks(self):
        declaration_blocks = {}
        for sheet in self.style_tag_contents:
            for ruleset in sheet.rulesets:
                declaration_block = "{" + ruleset.declaration_block.text
                source = sheet.href
                try:
                    if declaration_blocks[declaration_block]:
                        declaration_blocks[declaration_block].append(source)
                    else:
                        declaration_blocks[declaration_block] = [source, ]
                except KeyError:
                    declaration_blocks[declaration_block] = [source, ]
        for sheet in self.stylesheet_objects:
            for ruleset in sheet.rulesets:
                declaration_block = "{" + ruleset.declaration_block.text
                source = sheet.href
                try:
                    if declaration_blocks[declaration_block]:
                        declaration_blocks[declaration_block].append(source)
                    else:
                        declaration_blocks[declaration_block] = [source, ]
                except KeyError:
                    declaration_blocks[declaration_block] = [source, ]
        return declaration_blocks


    def get_linked_stylesheets(self):
        stylesheets = []
        try:
            for file, sheets in self.linked_stylesheets.items():
                for sheet in sheets:
                    if sheet not in stylesheets:
                        stylesheets.append(sheet)
        except TypeError:
            print("no stylesheet found in {}".format(file))
        return stylesheets


    def set_readme_list(self):
        readme_list = self.readme_list[:]
        for i in range(len(self.readme_list)):
            if self.readme_list[i] == "### CSS":
                break
        self.readme_list = readme_list[i:] 


    def get_project_css_by_file(self, html_files):
        # create a dictionary of files in the project 
        # each with a list of CSS applied
        file_dict = {}
        for file in html_files:
            filename = clerk.get_file_name(file)
            file_dict[filename] = []
            head_children = self.get_children(file, "head")
            styles = self.get_css_elements(head_children)
            body_children = self.get_children(file, "body")
            styles += self.get_css_elements(body_children)
            file_dict[filename] = styles
        self.project_css_by_html_file = file_dict
    
    
    def get_order_of_css_by_file(self, html_files):
        file_dict = {}
        for file in html_files:
            filename = clerk.get_file_name(file)
            file_dict[filename] = []
            head_children = self.get_children(file, "head")
            for element in head_children:
                tag = element.name
                if tag == 'link' or tag == 'style':
                    type = tag
                    source = element.attrs.get('href')
                    if source:
                        if 'http' not in source and '.css' in source[-4:]:
                            file_dict[filename].append(source)
                    else:
                        file_dict[filename].append("style tag")
        self.order_of_css_by_file = file_dict
                    
    
    def check_pages_for_same_css_files(self):
        if len(self.html_files) == 1:
            # Should we also check to make sure that one page is using css?
            linked_stylesheets = list(self.linked_stylesheets.values())
            for sheet in linked_stylesheets:
                if sheet:
                    return True
            return False
        files = self.extract_only_style_tags_from_css_files(self.project_css_by_html_file)
        files = list(files.values())
        self.pages_contain_same_css_files = all(file == files[0] for file in files)
   
        
    def extract_only_style_tags_from_css_files(self, files_with_css):
        results = {}
        for page, styles in files_with_css.items():
            results[page] = []
            for style in styles:
                if "style_tag=" not in style:
                    results[page].append(style) 
        return results


    def get_children(self, path, parent):
        code = html.get_html(path)
        try:
            head = code.find(parent)
            children = head.findChildren()
            return children
        except:
            return None


    def get_css_elements(self, nodes):
        styles=[]
        if not nodes:
            return styles
        for el in nodes:
            if el.name == 'link':
                if el.attrs["href"] and el.attrs['href'][-4:] == '.css':
                    styles.append(el.attrs['href'])
            if el.name == 'style':
                # append styles to file_dict
                css_string = el.string
                css_string = str(css_string)
                styles.append("style_tag=" + css_string)
        return styles


    def get_num_css_files(self):
        css_files = clerk.get_all_files_of_type(self.__dir_path, 'css')
        num_css_files = len(css_files)
        self.report_details["num_css_files"] = num_css_files
        return num_css_files


    def get_style_tags(self):
        # get HTML files
        html_files = clerk.get_all_files_of_type(self.__dir_path, 'html')
        # get the contents of any style tag in each html doc
        for file in html_files:
            style_tags = html.get_elements("style", file)
            for tag in style_tags:
                filename = os.path.basename(file)
                css_object = stylesheet(filename, tag.string)
                self.style_tag_contents.append(css_object)
            self.report_details["style_tags"].append((file, len(style_tags)))
        return self.report_details["style_tags"]
  
    
    def get_num_style_tags(self):
        self.num_style_tags = len(self.report_details['style_tags'])
        return self.num_style_tags


    def get_css_code(self):
        # extract content from all CSS files
        self.css_files = clerk.get_all_files_of_type(self.__dir_path, "css")
        for file in self.css_files:
            # First check to make sure the file was actually used in the project
            filename = clerk.get_file_name(file)
            is_linked = self.file_is_linked(filename)
            if not is_linked:
                continue
            try:
                css_code = clerk.get_css_from_stylesheet(file)
                
                css = stylesheet(filename, css_code)
                self.stylesheet_objects.append(css)
            except:
                print("Something went wrong with getting stylesheet objects")
    
    
    def file_is_linked(self, filename):
        for sheets in self.linked_stylesheets.values():
            if sheets:
                for sheet in sheets:
                    if filename in sheet:
                        return True
        return False
    
    
    def validate_css(self):
        # Get CSS validation on CSS files
        errors = 0
        for file_path in self.css_files:
            # Run css code through validator
            # Get code
            code = clerk.file_to_string(file_path)
            errors_in_file = val.validate_css(code)
            # Add to number of errors
            errors += len(errors_in_file)
            page_name = clerk.get_file_name(file_path)
            if errors > 0:
                self.process_errors(page_name, errors_in_file)
        # Get CSS validation from style tag
        for tag in self.style_tag_contents:
            tag_errors = val.validate_css(tag.text)
            # No need to process an error if we have none
            if "Congratulations!" in tag_errors[0].text:
                continue
            errors += len(tag_errors)
            if len(tag_errors) > 0:
                self.process_errors(tag.href, tag_errors)

        # add any errors to css_errors
        self.css_errors = self.report_details["css_validator_results"]


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
            # We need to grab all tr.error contents for errors
            error_rows = self.get_error_rows(item)

            # process errors
            if error_rows:
                errors_dict[page_name] = []
                for row in error_rows:
                    row_dict = self.get_results_details("error", row)
                    errors_dict[page_name].append(row_dict)
                

            # process warnings
            warning_rows = self.get_warning_rows(item)
            if warning_rows:
                warnings_dict[page_name] = []
                for row in warning_rows:
                    row_dict = self.get_results_details("warning", row)
                    warnings_dict[page_name].append(row_dict)

        if errors_dict:
            self.report_details["css_validator_results"][page_name] = errors_dict[page_name]
        else:
            self.report_details["css_validator_results"][page_name] = "No errors"
        if warnings_dict:
            self.report_details["css_validator_results"][page_name] = warnings_dict[page_name]


    def get_error_rows(self, item):
        item_string = item.contents
        item_string = "".join([str(elem) for elem in item_string])
        error_soup = BeautifulSoup(item_string, 'html.parser')
        error_rows = error_soup.find_all('tr', {'class':'error'})
        return error_rows


    def get_results_details(self, type, tag):
        details = {}
        # check for warning or error
        details[type] = type
        line_number = tag.contents[1]['title']
        details["line_number"] = line_number
        context = tag.contents[3].text
        details["context"] = context
        message = tag.contents[5].text
        message = clerk.clear_extra_text(message)
        details["error_msg"] = message
        code = tag.contents[5].find('span')
        details['extract'] = code
        return details
  
    
    def get_warning_rows(self, item):
        item_string = item.contents
        item_string = "".join([str(elem) for elem in item_string])
        error_soup = BeautifulSoup(item_string, 'html.parser')
        rows = error_soup.find_all('tr', {'class':'warning'})
        return rows


    def publish_results(self):
        # Get report	
        report_content = html.get_html(report_path)
        # TODO Process all the CSS info into our CSS tables
        
        # Generate Validator Reports
        general_results = ""
        specific_results = ""
        cumulative_errors = 0
        has_errors = self.has_css_errors(self.css_errors)
        if not has_errors:
            # write 1 column entry indicating there are no errors
            congrats = "Congratulations, no errors were found."
            general_results = '<tr><td colspan="4">' + congrats + '</td></tr>'
            pages = self.css_errors.keys()
            for page in pages:
                specific_results += '<tr><td>' + page + '</td>'
                specific_results += '<td>No errors found</td>'
                specific_results += '<td>NA</td>' * 2 + '</tr>\n'
        else:
            # cumulative_errors = 0
            specific_results = ''
            for page, errors in self.css_errors.items():
                # Process general results
                num_errors = len(errors) 
                cumulative_errors += num_errors
                general_results += '<tr><td>' + page + '</td>'
                general_results += '<td>' + str(num_errors) + '</td>'
                general_results += '<td>' + str(cumulative_errors) + '</td></tr>'

                # process specific results
                for error in errors:
                    # get page, message, location, and extract
                    message = error['error_msg']
                    location = error['line_number']
                    has_extract = error.get('extract')
                    if has_extract:
                        extract = error['extract'].contents[0]
                    specific_results += '<tr><td>' + page + '</td>'
                    specific_results += '<td>' + message + '</td>'
                    specific_results += '<td>' + location + '</td>'
                    if has_extract:
                        specific_results += '<td><pre>' + extract.strip() + '</pre></td></tr>'
                    else:
                        specific_results += '<td>No extract</td></tr>'
        # create our tbody contents for general validation
        tbody_contents = BeautifulSoup(
            general_results, "html.parser")
        tbody_id = 'css-validation-general'
        report_content.find(id=tbody_id).replace_with(tbody_contents)
        
        # create our tbody contents for css validation errors
        tbody_contents = BeautifulSoup(
            specific_results, "html.parser")
        tbody_id = 'css-validation-specifics'
        report_content.find(id=tbody_id).replace_with(tbody_contents)
        
        # Generate CSS Goals Report 
        # did it meet CSS validator goals? [goal | actual | results]
        css_errors_goal = self.report_details['standard_requirements_goals']['CSS Errors']
        min = css_errors_goal['min']
        max = css_errors_goal['max']
        css_errors_goal = "<td>CSS Errors - Min: {} Max: {}</td>".format(min, max)
        css_validator_errors = "<td>Total CSS Errors: {}</td></tr>".format(cumulative_errors)
        css_validator_results = str(bool(cumulative_errors < max))
        css_validator_results = "<td>" + css_validator_results + "</td>"
        css_goals_tbody = "<tr>" + css_validator_errors + "</tr>" 

        # What about general styles goals?
        # Loop through general Styles Goals and get all goals and results
        general_styles_goals = ""
        for goal, details in self.report_details["general_styles_goals"].items():
            # Build out the table row
            goal_details = details['details']
            goal_description = goal_details.get('description')
            goal_str = "<strong>{}</strong>: {}".format(goal, goal_description)
            has_min_max = goal_details.get('minimum')
            if has_min_max:
                min = goal_details['minimum']
                max = goal_details['maximum']
                actual = goal_details['actual']
                actual_string = "Minimum: {} Maximum: {} Actual: {}".format(min, max, actual)
            else:
                actual_string = "Hmmm...."
                print("What now? No min or max")
            results = str(goal_details['meets'])
            general_styles_goals += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format( goal, actual_string, results)
        
        # Check standard requirements goals
        
        # Any project specific goals?
        
        
        # Save new HTML as report/report.html
        with open(report_path, 'w') as f:
            f.write(str(report_content.contents[0]))
   
    
    def has_css_errors(self, css_errors):
        result = False
        for page, item in css_errors.items():
            if isinstance(item, list):
                for el in item:
                    if isinstance(el, dict):
                        error = el.get('error')
                        if error:
                            return True
            else:
                if item == 'error':
                    return True
        return False
   
    
    def get_css_validation_results(self):
        results = ""
        cumulative_errors = 0
        for page in self.report_details['css_validator_results'].values():
            if page != 'No errors':
                errors = 0
                for item in page:
                    if 'error' in item.keys():
                        errors += 1
                        
        print(errors)
        if not self.validator_errors:
            return '<tr><td rowspan="4">Congratulations! No Errors Found</td></tr>'
        else:
            try:
                validation_report = self.validator_errors[validation_type].copy()
            except:
                print("Whoah Nelly")
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
