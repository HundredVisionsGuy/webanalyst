# test_report.py
# Hundredvisionsguy
# Will test the various classes and methods in the report package

import pytest
import report
import clerk
from bs4 import BeautifulSoup

about_me_dir_path = "tests/test_files/projects/about_me/"
large_project_path = "tests/test_files/projects/large_project/"


@pytest.fixture
def my_report():
    my_report = report.Report(about_me_dir_path)
    return my_report


@pytest.fixture
def my_large_project_report():
    my_test_project = report.Report(large_project_path)
    return my_test_project


@pytest.fixture
def report_readme_list():
    my_report = report.Report(about_me_dir_path)
    my_list = my_report.get_readme_list()
    return my_list


@pytest.fixture
def large_project_readme_list():
    my_report = report.Report(large_project_path)
    my_list = my_report.get_readme_list()
    return my_list


@pytest.fixture
def my_general_report(report_readme_list):
    general_report = report.GeneralReport(
        report_readme_list, about_me_dir_path)
    general_report.generate_report()
    return general_report


@pytest.fixture
def my_large_project_general_report(large_project_readme_list):
    large_project_report = report.GeneralReport(
        large_project_readme_list, large_project_path)
    large_project_report.generate_report()
    return large_project_report


@pytest.fixture
def my_html_report(report_readme_list):
    html_report = report.HTMLReport(report_readme_list, about_me_dir_path)
    return html_report


@pytest.fixture
def my_large_project_html_report(large_project_readme_list):
    html_report = report.HTMLReport(
        large_project_readme_list, large_project_path)
    return html_report


@pytest.fixture
def my_css_report(report_readme_list):
    css_report = report.CSSReport(report_readme_list, about_me_dir_path)
    return css_report


@pytest.fixture
def my_large_project_css_report(large_project_readme_list):
    css_report = report.CSSReport(
        large_project_readme_list, large_project_path)
    return css_report


@pytest.fixture
def paragraph_tag():
    p = "<p>I was born a young child in Phoenix, Arizona. I was the last of five children, but I had a good childhood.</p>"
    p_tag = BeautifulSoup(p, 'html.parser')
    return p_tag


def test_report_for_report_object(my_report):
    assert my_report


def test_get_readme_text_for_about_me(my_report):
    results = my_report.get_readme_text()[:24]
    expected = "# Project Name: About Me"
    assert results == expected


def test_general_report_for_report_title_from_about_me(my_general_report):
    my_general_report.set_title()
    results = my_general_report.get_title()
    expected = "About Me"
    assert results == expected


def test_general_report_for_get_description_for_about_me(my_general_report):
    my_general_report.set_description()
    results = my_general_report.get_description()
    expected = """Students are asked to create a single web page designed to give information about the student using Headings (h1 & h2), paragraphs, links, and bold and italics."""
    assert results == expected


def test_html_report_for_get_html_level(my_html_report):
    results = my_html_report.get_html_level()
    expected = "101"
    assert results == expected


def test_report_for_about_me_wordcount(my_general_report):
    results = my_general_report.get_word_count()
    expected = 61
    assert results == expected


def test_general_report_get_num_words(my_general_report, paragraph_tag):
    results = my_general_report.get_num_words(paragraph_tag)
    expected = 22
    assert results == expected


def test_html_report_for_num_of_files(my_html_report):
    results = my_html_report.get_num_html_files()
    expected = 1
    assert results == expected


def test_css_report_for_num_of_files(my_css_report):
    results = my_css_report.get_num_css_files()
    expected = 0
    assert results == expected


def test_css_report_for_num_style_tags_1(my_css_report):
    results = my_css_report.get_num_style_tags()
    expected = 1
    assert results == expected
