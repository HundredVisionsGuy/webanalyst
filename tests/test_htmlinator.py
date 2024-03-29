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
