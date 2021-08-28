# test_report.py
# Hundredvisionsguy
# Will test the various classes and methods in the report package

import pytest
from webanalyst import report
from webanalyst import clerk
from bs4 import BeautifulSoup

about_me_path = "tests/test_files/projects/about_me/"
about_me_file_path = about_me_path + "index.html"
large_project_path = "tests/test_files/projects/large_project/"
about_me_dnm_path = "tests/test_files/projects/about_me_does_not_meet/"
report_html_doc_path = "report/report.html"
multipage_meets_path = "tests/test_files/projects/multi_page_meets/"

@pytest.fixture
def about_me_report():
    my_report = report.Report(about_me_path)
    my_report.generate_report()
    yield my_report

@pytest.fixture
def about_me_dnm_report():
    my_report = report.Report(about_me_dnm_path)
    my_report.generate_report()
    yield my_report

@pytest.fixture
def large_project_report():
    my_test_project = report.Report(large_project_path)
    my_test_project.generate_report()
    yield my_test_project

@pytest.fixture
def multipage_meets_report():
    my_project = report.Report(multipage_meets_path)
    my_project.generate_report()
    yield my_project

@pytest.fixture
def about_me_readme_list():
    my_report = report.Report(about_me_path)
    my_list = my_report.get_readme_list()
    yield my_list

@pytest.fixture
def about_me_dnn_readme_list():
    my_report = report.Report(about_me_dnm_path)
    my_list = my_report.get_readme_list()
    yield my_list

@pytest.fixture
def large_project_readme_list():
    my_report = report.Report(large_project_path)
    my_list = my_report.get_readme_list()
    yield my_list


@pytest.fixture
def about_me_general_report(about_me_report):
    yield about_me_report.general_report

@pytest.fixture
def large_project_general_report(large_project_report):
    yield large_project_report.general_report


@pytest.fixture
def about_me_html_report(about_me_report):
    yield about_me_report.html_report

@pytest.fixture
def about_me_dnm_html_report(about_me_dnm_report):
    yield about_me_dnm_report.html_report

@pytest.fixture
def large_project_html_report(large_project_report):
    yield large_project_report.html_report

@pytest.fixture
def about_me_css_report(about_me_report):
    yield about_me_report.css_report

@pytest.fixture
def about_me_dnm_css_report(about_me_dnm_report):
    # css_report = report.CSSReport(about_me_dnn_readme_list, about_me_dnm_path)
    yield about_me_dnm_report.css_report

@pytest.fixture
def large_project_css_report(large_project_report):
    yield large_project_report.css_report

@pytest.fixture
def multi_page_meets_css_report(multipage_meets_report):
    yield multipage_meets_report.css_report

@pytest.fixture
def paragraph_tag():
    p = "<p>I was born a young child in Phoenix, Arizona. I was the last of five children, but I had a good childhood.</p>"
    p_tag = BeautifulSoup(p, 'html.parser')
    return p_tag

@pytest.fixture
def about_me_required_elements():
    return ['DOCTYPE', 'HTML', 'HEAD', 'TITLE', 'BODY', 'H1', 'H2', 'P', 'STRONG', 'EM']

def test_report_for_general_report_pre_generate_report():
    about_report = report.Report(about_me_path)
    assert not about_report.general_report

def test_report_for_general_report_post_generate_report():
    about_report = report.Report(about_me_path)
    about_report.generate_report()
    assert about_report.general_report

def test_about_me_report_for_report_object(about_me_report):
    assert about_me_report


def test_get_readme_text_for_about_me(about_me_report):
    results = about_me_report.get_readme_text()[:24]
    expected = "# Project Name: About Me"
    assert results == expected

# GeneralReport Tests


def test_large_project_general_report_for_set_paragraphs(large_project_general_report):
    # test for number of paragraphs
    paragraphs = large_project_general_report.get_paragraphs()
    num_paragraphs = len(paragraphs)
    expected = 4
    assert num_paragraphs == expected


def test_about_me_general_report_for_title(about_me_general_report):
    about_me_general_report.set_title()
    results = about_me_general_report.get_title()
    expected = "About Me"
    assert results == expected


def test_about_me_report_for_get_description(about_me_general_report):
    about_me_general_report.set_description()
    results = about_me_general_report.get_description()
    expected = """Students are asked to create a single web page designed to give information about the student using Headings (h1 & h2), paragraphs, links, and bold and italics."""
    assert results == expected


def test_about_me_report_for_wordcount(about_me_general_report):
    results = about_me_general_report.get_word_count()
    expected = 61
    assert results == expected


def test_about_me_general_report_for_get_num_words(about_me_general_report, paragraph_tag):
    results = about_me_general_report.get_num_words(paragraph_tag)
    expected = 22
    assert results == expected


def test_about_me_general_report_for_get_sentences(about_me_general_report):
    expected = 5
    results = len(about_me_general_report.sentences)
    assert results == expected


def test_about_me_general_report_for_set_min_number_files(about_me_general_report):
    html_num_results = about_me_general_report.report_details["min_number_files"]["HTML"]
    expected_html = 1
    assert html_num_results == expected_html

    css_num_results = about_me_general_report.report_details["min_number_files"]["CSS"]
    css_num_expected = 0
    assert css_num_results == css_num_expected


def test_about_me_general_report_for_num_files_results_html(about_me_general_report):
    meets_html_results = about_me_general_report.report_details["num_files_results"]["Meets HTML"]
    # It meets
    assert meets_html_results


def test_about_me_general_report_for_num_files_results_css(about_me_general_report):
    meets_css_results = about_me_general_report.report_details["num_files_results"]["Meets CSS"]
    # It meets
    assert meets_css_results


def test_general_report_for_analyze_results(about_me_general_report, large_project_general_report):
    # analyze about_me report
    about_me_general_report.analyze_results()
    # 3 paragraphs and 5 sentences
    expected_SPP = 1.6666666666666667
    assert about_me_general_report.report_details["writing_goal_results"]["actual_SPP"] == expected_SPP

    # Test meets_SPP
    expected = True
    assert about_me_general_report.report_details["writing_goal_results"]["meets_SPP"] == expected

    # 61 words & 5 sentences
    expected_WPS = 12.2
    assert about_me_general_report.report_details["writing_goal_results"]["actual_WPS"] == expected_WPS

    expected_meets_WPS = True
    meets_WPS_results = about_me_general_report.report_details["writing_goal_results"]["meets_WPS"]
    assert expected_meets_WPS == meets_WPS_results


def test_general_report_for_get_report_details_min_number_files(about_me_general_report):
    details = about_me_general_report.get_report_details()
    assert details['min_number_files']['HTML'] == 1


def test_publish_results_for_report_file_existing(about_me_general_report):
    results = clerk.file_exists(report.report_path)
    assert results

def test_general_report_for_get_report_results_string_for_spp(about_me_general_report):
    spp_input = ["general-spp-results",
                "Avg. Sentences / Paragraph",
                "[1, 5]"]
    actual = about_me_general_report.report_details["writing_goal_results"]
    results = report.Report.get_report_results_string(spp_input[0], spp_input[1], spp_input[2], actual["actual_SPP"], actual["meets_SPP"])
    expected = '<tr class="general-spp-results"><td>Avg. Sentences / Paragraph</td><td>[1, 5]</td><td>1.6666666666666667</td><td>Meets</td></tr>'
    assert results == expected

def test_general_report_for_get_report_results_string_for_wps(about_me_general_report):
    wps_input = ["general-wps-results",
                "Avg. Words / Sentence",
                "[10, 20]"]
    actual = about_me_general_report.report_details["writing_goal_results"]
    results = report.Report.get_report_results_string(wps_input[0], wps_input[1], wps_input[2], actual["actual_WPS"], actual["meets_WPS"])
    expected = '<tr class="general-wps-results"><td>Avg. Words / Sentence</td><td>[10, 20]</td><td>12.2</td><td>Meets</td></tr>'
    assert results == expected

def test_static_method_get_report_results_string_for_html(about_me_general_report):
    html_id = "general-html-files-results"
    type_column = "HTML"
    num_files = about_me_general_report.num_html_files
    target = about_me_general_report.report_details["min_number_files"]
    actual = about_me_general_report.report_details["num_files_results"]
    results = report.Report.get_report_results_string(html_id, type_column, target["HTML"], num_files, actual["Meets HTML"])
    expected = '<tr class="general-html-files-results"><td>HTML</td><td>1</td><td>1</td><td>Meets</td></tr>'
    assert results == expected

def test_general_report_for_get_report_results_string_for_css(about_me_general_report):
    html_id = "general-css-files-results"
    type_column = "CSS"
    num_files = about_me_general_report.num_css_files
    target = about_me_general_report.report_details["min_number_files"]
    actual = about_me_general_report.report_details["num_files_results"]
    results = report.Report.get_report_results_string(html_id, type_column, target["CSS"], num_files, actual["Meets CSS"])
    expected = '<tr class="general-css-files-results"><td>CSS</td><td>0</td><td>0</td><td>Meets</td></tr>'
    assert results == expected

def test_large_project_general_report_for_get_min_number_files_for_2_HTML(large_project_general_report):
    results = large_project_general_report.get_min_number_files("html")
    expected = 2
    assert results == expected

def test_large_project_general_report_for_get_min_number_files_for_2_CSS(large_project_general_report):
    results = large_project_general_report.get_min_number_files("css")
    expected = 2
    assert results == expected

# HTMLReport Tests


def test_about_me_html_report_for_get_html_level(about_me_html_report):
    results = about_me_html_report.get_html_level()
    expected = "101"
    assert results == expected


def test_about_me_html_report_for_num_of_files(about_me_html_report):
    results = about_me_html_report.get_num_html_files()
    expected = 1
    assert results == expected


def test_large_project_html_report_for_num_of_files(large_project_html_report):
    results = large_project_html_report.get_num_html_files()
    expected = 3
    assert results == expected


def test_about_me_html_report_for_can_attain_next_level(about_me_html_report):
    results = about_me_html_report.can_attain_level()
    expected = False
    assert results == expected

def test_about_me_html_report_for_analyze_results_can_attain_level_property_change(about_me_html_report):
    about_me_html_report.analyze_results()
    results = about_me_html_report.report_details["can_attain_level"]
    expected = False
    assert results == expected

def test_large_project_html_report_for_analyze_results_can_attain_level_property_change(large_project_html_report):
    large_project_html_report.analyze_results()
    results = large_project_html_report.report_details["can_attain_level"]
    expected = True 
    assert results == expected

def test_about_me_html_report_for_get_html_requirements_list(about_me_html_report):
    result_list = about_me_html_report.get_html_requirements_list()
    results = "### HTML" in result_list[0] and "`EM`: 2 or more" in result_list[-1]
    expected = True
    assert results == expected


def test_html_report_for_ammend_required_elements(about_me_html_report):
    about_me_html_report.ammend_required_elements()
    assert (
        "P", 3) in about_me_html_report.report_details["required_elements"].items()


def test_html_report_for_meeting_html5_essential_elements(about_me_html_report):
    results = about_me_html_report.meets_html5_essential_requirements()
    expected = True
    assert results == expected


def test_html_report_for_check_element_for_required_number(about_me_html_report):
    # There should be at least 3 paragraphs in about me
    results = about_me_html_report.check_element_for_required_number(
        about_me_file_path, "p", 3)
    expected = True
    assert results == expected


def test_html_report_for_get_required_elements(about_me_html_report, about_me_required_elements):
    results = about_me_html_report.get_required_elements()
    expected = about_me_required_elements
    assert results == expected


def test_html_report_for_meeting_essential_elements(about_me_html_report):
    results = about_me_html_report.meets_required_elements()
    expected = True
    assert results == expected

def test_html_report_for_set_required_elements_about_me_h1(about_me_html_report):
    about_me_html_report.set_required_elements_found()
    results = about_me_html_report.report_details["required_elements"]["H1"]
    assert results == 1


def test_html_report_for_set_required_elements_about_me_h2(about_me_html_report):
    about_me_html_report.set_required_elements_found()
    results = about_me_html_report.report_details["required_elements"]["H2"]
    assert results == 2

def test_html_report_meets_htmle5_essential_requirements_for_false(about_me_dnm_html_report):
    results = about_me_dnm_html_report.meets_html5_essential_requirements()
    assert results == False

def test_html_report_for_extract_el_from_dict_key_tuple(about_me_html_report):
    dictionary = {(0, 'H1'): 1, (1, 'H2'): 2, (2, 'P'): 3}
    expected = {'H1': 1, 'H2': 2, 'P': 3}
    results = about_me_html_report.extract_el_from_dict_key_tuple(dictionary)
    assert results == expected

def test_html_report_for_get_validator_goals_return_value(about_me_html_report):
    results = about_me_html_report.get_validator_goals()
    expected = 0
    assert results == expected

def test_html_report_for_get_validator_goals_to_set_details(about_me_html_report):
    results = about_me_html_report.report_details["validator_goals"]
    expected = 0
    assert results == expected

def test_large_project_html_report_for_get_validator_goals_return_value(large_project_html_report):
    results = large_project_html_report.get_validator_goals()
    expected = 2
    assert results == expected

def test_large_project_html_report_for_get_validator_goals_to_set_details(large_project_html_report):
    results = large_project_html_report.report_details["validator_goals"]
    expected = 2
    assert results == expected

def test_set_linked_stylesheets_for_no_CSS_files(about_me_html_report):
    expected = {'index.html': None}
    results = about_me_html_report.linked_stylesheets
    assert results == expected

def test_large_project_html_report_for_set_linked_stylesheets(large_project_html_report):
    expected = {"about.html":["css/navigation.css", "css/general.css", "css/layout.css"],"gallery.html":["css/navigation.css", "css/general.css", "css/layout.css"],"index.html":None
    }
    assert large_project_html_report.linked_stylesheets == expected


# CSSReport tests

def test_about_me_css_report_for_num_of_files(about_me_css_report):
    results = about_me_css_report.get_num_css_files()
    expected = 0
    assert results == expected

def test_about_me_css_report_for_report_details_num_css_files(about_me_css_report):
    about_me_css_report.get_num_css_files()
    results = about_me_css_report.report_details["num_css_files"]
    expected = 0
    assert results == expected

def test_large_project_css_report_for_report_details_num_css_files(large_project_css_report):
    large_project_css_report.get_num_css_files()
    results = large_project_css_report.report_details["num_css_files"]
    expected = 4
    assert results == expected

def test_about_me_css_report_for_num_style_tags(about_me_css_report):
    results = about_me_css_report.get_num_style_tags()
    expected = 1
    assert results == expected

def test_about_me_css_report_validate_css_for_0_errors(about_me_css_report):
    css_errors = about_me_css_report.report_details['css_validator_results']
    results = len(css_errors)
    expected = 0
    assert results == expected

def test_about_me_dnm_css_report_for_validate_css_results_for_2_errors(about_me_dnm_css_report):
    css_errors = about_me_dnm_css_report.report_details['css_validator_results']
    print(css_errors)
    results = len(css_errors)
    expected = 2
    assert results == expected

def test_about_me_css_report_for_get_project_css_by_file(about_me_css_report):
    # should have been generated
    about_me_css_report.generate_report(["tests\\test_files\\projects\\about_me_does_not_meet\\index.html",])
    num_css_tags = len(about_me_css_report.project_css_by_html_file["index.html"])
    assert num_css_tags == 1

def test_about_me_css_report_for_get_children_head(about_me_css_report):
    children = about_me_css_report.get_children('tests\\test_files\\projects\\about_me\\index.html', 'head')
    assert len(children) == 4

def test_large_project_css_report_for_get_children_head(large_project_css_report):
    children = large_project_css_report.get_children('tests\\test_files\\projects\\large_project\\gallery.html', 'head')
    assert len(children) == 8

def test_large_project_css_report_for_get_project_css_by_file(large_project_css_report):
    large_project_html_docs = ['tests\\test_files\\projects\\large_project\\gallery.html', 'tests\\test_files\\projects\\large_project\\index.html']
    large_project_css_report.generate_report(large_project_html_docs)
    num_css_files = len(large_project_css_report.project_css_by_html_file["gallery.html"])
    assert num_css_files == 3

def test_about_me_css_report_for_no_css_files(about_me_css_report):
    expected = 0
    results = len(about_me_css_report.css_files)
    assert results == expected

def test_large_project_css_report_for_4_css_files(large_project_css_report):
    expected = 4
    results = len(large_project_css_report.css_files)
    assert results == expected

def test_pages_contain_same_css_files_for_large_project_css_report_false(large_project_css_report):
    results = large_project_css_report.pages_contain_same_css_files
    assert results == False

def test_extract_only_style_tags_from_css_files_for_large_project_css_report_index_page(large_project_css_report):
    html_files = large_project_css_report.project_css_by_html_file
    results = large_project_css_report.extract_only_style_tags_from_css_files(html_files)
    assert len(results['index.html']) == 0

def test_extract_only_style_tags_from_css_files_for_large_project_css_report_gallery_page(large_project_css_report):
    html_files = large_project_css_report.project_css_by_html_file
    results = large_project_css_report.extract_only_style_tags_from_css_files(html_files)
    assert len(results['gallery.html']) == 3

def test_extract_only_style_tags_from_css_files_for_large_project_css_report_about_page(large_project_css_report):
    html_files = large_project_css_report.project_css_by_html_file
    results = large_project_css_report.extract_only_style_tags_from_css_files(html_files)
    assert len(results['about.html']) == 3

def test_pages_contain_same_css_files_for_multipage_meets_project_true(multi_page_meets_css_report):
    assert multi_page_meets_css_report.pages_contain_same_css_files

def test_pages_contain_same_css_files_for_large_project_false(large_project_css_report):
    assert not large_project_css_report.pages_contain_same_css_files

def test_set_repeat_selectors_for_large_report_body_selector(large_project_css_report):
    results = large_project_css_report.repeat_selectors["body"]
    assert 'general.css' in results

def test_set_repeat_selectors_for_large_report_body_selector_in_about_html(large_project_css_report):
    results = large_project_css_report.repeat_selectors["body"]
    assert 'about.html' in results

def test_get_filenames_from_path(large_project_css_report):
    full_paths = ['css/navigation.css', 'css/general.css', 'css/layout.css']
    expected = ['navigation.css', 'general.css', 'layout.css']
    results = large_project_css_report.get_filenames_from_paths(full_paths)
    assert results == expected

def test_get_implemented_selectors(large_project_css_report):
    selectors = []
    filenames = ['navigation.css', 'general.css', 'layout.css']
    implemented_selectors = large_project_css_report.get_implemented_selectors(selectors, filenames)
    results = implemented_selectors.get('general.css')
    expected = ['body', 'h1, h2, h3, h4, h5, h6', 'p']
    assert results == expected

def test_get_repeated_selectors(large_project_css_report):
    expected = {'.container': ['layout.css', 'layout.css'], '.image-gallery .display-box': ['layout.css', 'layout.css'], 'body': ['about.html', 'general.css', 'layout.css'], 'header': ['layout.css', 'navigation.css'], 'header h1': ['layout.css', 'navigation.css']}
    results = large_project_css_report.repeat_selectors
    assert results == expected

def test_file_is_linked_for_true(large_project_css_report):
    results = large_project_css_report.file_is_linked('navigation.css')
    assert results 

def test_file_is_linked_for_false(large_project_css_report):
    results = large_project_css_report.file_is_linked('grid-layout.css')
    assert results == False

def test_set_repeat_declaration_blocks(large_project_css_report):
    expected = ['layout.css', 'layout.css']
    results = large_project_css_report.repeat_declarations_blocks['{margin: 0;padding: 0;}']
    assert results == expected

def test_get_standard_requirements_large_project(large_project_css_report):
    expected = {'CSS Errors': {'min': 0, 'max': 0}, 'Repeat selectors': {'min': 0, 'max': 0}, 'Repeat declaration blocks': {'min': 0, 'max': 0}}
    results = large_project_css_report.report_details['standard_requirements_goals']
    assert results == expected

def test_get_standard_requirements_about_me_project(about_me_css_report):
    expected = {'CSS Errors': {'min': 0, 'max': 2}, 'Repeat selectors': {'min': 0, 'max': 0}, 'Repeat declaration blocks': {'min': 0, 'max': 0}}
    results = about_me_css_report.report_details['standard_requirements_goals']
    assert results == expected

def test_get_header_details_for_font_families_details(about_me_report):
    input_string = '    * Font Families: number of font families to be set'
    results = about_me_report.get_header_details(input_string)
    expected = {'title': 'Font Families', 'details': {'description': 'number of font families to be set'}}
    assert results == expected

def test_get_css_errors_for_does_not_meet(about_me_dnm_css_report):
    results = about_me_dnm_css_report.get_css_errors()
    expected = 4
    assert results == expected

def test_get_css_errors_for_0_errors(about_me_css_report):
    results = about_me_css_report.get_css_errors()
    expected = 0
    assert results == expected

# report.html relatd tests
def test_about_me_report_html_doc_for_general_results(about_me_general_report):
    report_contents = clerk.file_to_string(report_html_doc_path)
    report_tr = '<tr class="general-wps-results"><td>Avg. Words / Sentence</td><td>[10, 20]</td><td>12.2</td><td>Meets</td></tr>'
    assert report_tr in report_contents

def test_about_me_html_report_for_general_results_in_report_html_doc_contents(about_me_html_report):
    report_contents = clerk.file_to_string(report_html_doc_path)
    report_tr = '<tr class="general-wps-results"><td>Avg. Words / Sentence</td><td>[10, 20]</td><td>12.2</td><td>Meets</td></tr>'
    assert report_tr in report_contents

def test_about_me_html_report_for_html_results_in_report_html_doc_html_results_content(about_me_html_report):
    report_contents = clerk.file_to_string(report_html_doc_path)
    report_tr = '<tr><td>H2</td><td>2</td><td>2</td><td>Meets</td></tr>'
    assert report_tr in report_contents

