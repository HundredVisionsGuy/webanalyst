# test_report.py
# Hundredvisionsguy
# Will test the various classes and methods in the report package

import pytest
import report
import clerk
from bs4 import BeautifulSoup

about_me_path = "tests/test_files/projects/about_me/"
large_project_path = "tests/test_files/projects/large_project/"


@pytest.fixture
def about_me_report():
    my_report = report.Report(about_me_path)
    return my_report


@pytest.fixture
def my_large_project_report():
    my_test_project = report.Report(large_project_path)
    return my_test_project


@pytest.fixture
def about_me_readme_list():
    my_report = report.Report(about_me_path)
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
    return general_report


@pytest.fixture
def my_large_project_general_report(large_project_readme_list):
    large_project_report = report.GeneralReport(
        large_project_readme_list, large_project_path)
    large_project_report.generate_report()
    return large_project_report


@pytest.fixture
def about_me_html_report(about_me_readme_list):
    html_report = report.HTMLReport(about_me_readme_list, about_me_path)
    return html_report


@pytest.fixture
def my_large_project_html_report(large_project_readme_list):
    html_report = report.HTMLReport(
        large_project_readme_list, large_project_path)
    return html_report


@pytest.fixture
def about_me_css_report(about_me_readme_list):
    css_report = report.CSSReport(about_me_readme_list, about_me_path)
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


def test_about_me_report_for_report_object(about_me_report):
    assert about_me_report


def test_get_readme_text_for_about_me(about_me_report):
    results = about_me_report.get_readme_text()[:24]
    expected = "# Project Name: About Me"
    assert results == expected


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


def test_about_me_html_report_for_get_html_level(about_me_html_report):
    results = about_me_html_report.get_html_level()
    expected = "101"
    assert results == expected


def test_about_me_report_for_wordcount(about_me_general_report):
    results = about_me_general_report.get_word_count()
    expected = 61
    assert results == expected


def test_about_me_general_report_for_get_num_words(about_me_general_report, paragraph_tag):
    results = about_me_general_report.get_num_words(paragraph_tag)
    expected = 22
    assert results == expected


def test_about_me_html_report_for_num_of_files(about_me_html_report):
    results = about_me_html_report.get_num_html_files()
    expected = 1
    assert results == expected


def test_large_project_html_report_for_num_of_files(my_large_project_html_report):
    results = my_large_project_html_report.get_num_html_files()
    expected = 2
    assert results == expected


def test_about_me_css_report_for_num_of_files(about_me_css_report):
    results = about_me_css_report.get_num_css_files()
    expected = 0
    assert results == expected


def test_about_me_css_report_for_num_style_tags_1(about_me_css_report):
    results = about_me_css_report.get_num_style_tags()
    expected = 1
    assert results == expected
