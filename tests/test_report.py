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


def test_report_for_report_object(my_report):
    assert my_report


def test_get_readme_text_for_about_me(my_report):
    results = my_report.get_readme_text()[:24]
    expected = "# Project Name: About Me"
    assert results == expected


def test_report_for_report_title_from_about_me(my_report):
    my_report.set_title()
    results = my_report.get_title()
    expected = "About Me"
    assert results == expected


def test_report_for_get_description_for_about_me(my_report):
    my_report.set_description()
    results = my_report.get_description()
    expected = """Students are asked to create a single web page designed to give information about the student using Headings (h1 & h2), paragraphs, links, and bold and italics."""
    assert results == expected


def test_report_for_get_html_level(my_report):
    results = my_report.get_html_level()
    expected = "101"
    assert results == expected


def test_report_details_for_persistent_html_level(my_report):
    my_report.get_html_level()
    results = my_report.report_details["html_level"]
    expected = "101"
    assert results == expected
