import pytest

from webanalyst import HTMLinator as html
from webanalyst import clerk

file_with_inline_styles = "tests/test_files/sample_with_inline_styles.html"


@pytest.fixture
def markup_with_inline_styles():
    markup = clerk.file_to_string(file_with_inline_styles)
    return markup


def test_html_report_for_file_that_uses_inline_styles(
    markup_with_inline_styles,
):
    assert html.uses_inline_styles(markup_with_inline_styles)


def test_htmlinator_for_uses_absolute_paths_for_True():
    code = ('<img src="https://cdn.pixabay.com/photo/2021/08/25/20/42/'
            'field-6574455__340.jpg" alt="image of field">')
    assert html.uses_absolute_paths(code)


def test_htmlinator_for_uses_absolute_paths_for_False():
    code_without = ('<img src="images/field-6574455__340.jpg'
                    ' alt= image of field>')
    assert not html.uses_absolute_paths(code_without)