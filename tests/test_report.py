# test_report.py
# Hundredvisionsguy
# Will test the various classes and methods in the report package

import pytest
import report
import clerk

about_me_directory = "tests/test_files/projects/about_me/"
about_me_readme_path = about_me_directory + "README.md"


@pytest.fixture
def readme():
    readme_text = clerk.file_to_string(about_me_readme_path)
    return readme_text


@pytest.fixture
def my_report():
    my_report = report.Report()
    return my_report


def test_report_for_report_object():
    assert my_report


def test_get_readme_text_for_about_me(readme):
    results = readme[:24]
    expected = "# Project Name: About Me"
    assert results == expected


def test_report_for_readme_text_first_line(my_report):
    my_report.set_readme_text(about_me_readme_path)
    results = my_report.get_readme_text()[:14]
    expected = "# Project Name"
    assert results == expected
