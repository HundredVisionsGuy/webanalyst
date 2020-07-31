# test_report.py
# Hundredvisionsguy
# Will test the various classes and methods in the report package

import pytest
import report
import clerk

about_me_readme_path = "tests/test_files/projects/about_me/README.md"


@pytest.fixture
def my_report():
    my_report = report.Report(about_me_readme_path)
    return my_report


@pytest.fixture
def report_readme_list():
    my_report = report.Report(about_me_readme_path)
    my_list = my_report.get_readme_list()
    return my_list


@pytest.fixture
def my_general_report(report_readme_list):
    general_report = report.GeneralReport(report_readme_list)
    return general_report


@pytest.fixture
def my_html_report(report_readme_list):
    html_report = report.HTMLReport(report_readme_list)
    return html_report


@pytest.fixture
def my_css_report(report_readme_list):
    css_report = report.CSSReport(report_readme_list)
    return css_report


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
