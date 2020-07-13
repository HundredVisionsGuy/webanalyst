import pytest
import HTMLinator as HT
import clerk
import validator as val

browser = val.browser
html_file_with_errors = "tests/test_files/sample_with_errors.html"


@pytest.fixture
def error_report():
    return val.get_markup_validity(html_file_with_errors)


def test_get_number_of_elements_for_p():
    results = HT.get_num_elements('p', html_file_with_errors)
    expected = 2
    assert results == expected


def test_get_number_of_elements_for_none():
    results = HT.get_num_elements('q', html_file_with_errors)
    expected = 0
    assert results == expected
