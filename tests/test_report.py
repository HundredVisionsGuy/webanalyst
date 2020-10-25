# test_report.py
# Hundredvisionsguy
# Will test the various classes and methods in the report package

import pytest
import report
import clerk
from bs4 import BeautifulSoup

about_me_path = "tests/test_files/projects/about_me/"
about_me_file_path = about_me_path + "index.html"
large_project_path = "tests/test_files/projects/large_project/"
about_me_dnm_path = "tests/test_files/projects/about_me_does_not_meet/"

@pytest.fixture
def about_me_report():
    my_report = report.Report(about_me_path)
    return my_report

@pytest.fixture
def about_me_dnm_report():
    my_report = report.Report(about_me_dnm_path)
    return my_report

@pytest.fixture
def large_project_report():
    my_test_project = report.Report(large_project_path)
    return my_test_project


@pytest.fixture
def about_me_readme_list():
    my_report = report.Report(about_me_path)
    my_list = my_report.get_readme_list()
    return my_list

@pytest.fixture
def about_me_dnn_readme_list():
    my_report = report.Report(about_me_dnm_path)
    my_list = my_report.get_readme_list()
    return my_list

@pytest.fixture
def large_project_readme_list():
    my_report = report.Report(large_project_path)
    my_list = my_report.get_readme_list()
    return my_list


@pytest.fixture
def about_me_general_report(about_me_readme_list):
    general_report = report.GeneralReport(
        about_me_readme_list, about_me_path)
    general_report.generate_report()
    yield general_report
    # teardown time
    # delete files in report folder
    if clerk.file_exists(report.report_path):
        clerk.delete_file(report.report_path) 

@pytest.fixture
def large_project_general_report(large_project_readme_list):
    large_project_report = report.GeneralReport(
        large_project_readme_list, large_project_path)
    large_project_report.generate_report()
    return large_project_report


@pytest.fixture
def about_me_html_report(about_me_readme_list):
    html_report = report.HTMLReport(about_me_readme_list, about_me_path)
    html_report.generate_report()
    return html_report

@pytest.fixture
def about_me_dnn_html_report(about_me_dnn_readme_list):
    html_report = report.HTMLReport(about_me_dnn_readme_list, about_me_dnm_path)
    html_report.generate_report()
    return html_report

@pytest.fixture
def large_project_html_report(large_project_readme_list):
    html_report = report.HTMLReport(
        large_project_readme_list, large_project_path)
    html_report.generate_report()
    yield html_report


@pytest.fixture
def about_me_css_report(about_me_readme_list):
    css_report = report.CSSReport(about_me_readme_list, about_me_path)
    return css_report


@pytest.fixture
def large_project_css_report(large_project_readme_list):
    css_report = report.CSSReport(
        large_project_readme_list, large_project_path)
    return css_report


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
    about_me_general_report.publish_results()
    results = clerk.file_exists(report.report_path)
    assert results

def test_general_report_for_get_report_results_string_for_spp(about_me_general_report):
    spp_input = ["general-spp-results",
                "Avg. Sentences / Paragraph",
                "[1, 5]"]
    actual = about_me_general_report.report_details["writing_goal_results"]
    results = report.Report.get_report_results_string(spp_input[0], spp_input[1], spp_input[2], actual["actual_SPP"], actual["meets_SPP"])
    expected = '<tr id="general-spp-results"><td>Avg. Sentences / Paragraph</td><td>[1, 5]</td><td>1.6666666666666667</td><td>Meets</td></tr>'
    assert results == expected

def test_general_report_for_get_report_results_string_for_wps(about_me_general_report):
    wps_input = ["general-wps-results",
                "Avg. Words / Sentence",
                "[10, 20]"]
    actual = about_me_general_report.report_details["writing_goal_results"]
    results = report.Report.get_report_results_string(wps_input[0], wps_input[1], wps_input[2], actual["actual_WPS"], actual["meets_WPS"])
    expected = '<tr id="general-wps-results"><td>Avg. Words / Sentence</td><td>[10, 20]</td><td>12.2</td><td>Meets</td></tr>'
    assert results == expected

def test_static_method_get_report_results_string_for_html(about_me_general_report):
    html_id = "general-html-files-results"
    type_column = "HTML"
    num_files = about_me_general_report.num_html_files
    target = about_me_general_report.report_details["min_number_files"]
    actual = about_me_general_report.report_details["num_files_results"]
    results = report.Report.get_report_results_string(html_id, type_column, target["HTML"], num_files, actual["Meets HTML"])
    expected = '<tr id="general-html-files-results"><td>HTML</td><td>1</td><td>1</td><td>Meets</td></tr>'
    assert results == expected

def test_general_report_for_get_report_results_string_for_css(about_me_general_report):
    html_id = "general-css-files-results"
    type_column = "CSS"
    num_files = about_me_general_report.num_css_files
    target = about_me_general_report.report_details["min_number_files"]
    actual = about_me_general_report.report_details["num_files_results"]
    results = report.Report.get_report_results_string(html_id, type_column, target["CSS"], num_files, actual["Meets CSS"])
    expected = '<tr id="general-css-files-results"><td>CSS</td><td>0</td><td>0</td><td>Meets</td></tr>'
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
    expected = 2
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

def test_html_report_meets_htmle5_essential_requirements_for_false(about_me_dnn_html_report):
    results = about_me_dnn_html_report.meets_html5_essential_requirements()
    assert results == False

def test_html_report_for_extract_el_from_dict_key_tuple(about_me_html_report):
    dictionary = {(0, 'H1'): 1, (1, 'H2'): 2, (2, 'P'): 3}
    expected = {'H1': 1, 'H2': 2, 'P': 3}
    results = about_me_html_report.extract_el_from_dict_key_tuple(dictionary)
    assert expected == results

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

# CSSReport tests


def test_about_me_css_report_for_num_of_files(about_me_css_report):
    results = about_me_css_report.get_num_css_files()
    expected = 0
    assert results == expected


def test_about_me_css_report_for_num_style_tags_1(about_me_css_report):
    results = about_me_css_report.get_num_style_tags()
    expected = 1
    assert results == expected
