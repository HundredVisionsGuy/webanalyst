import pytest
import CSSinator as css

css_code_1_with_comments = """
/* comment #1 */
body {
    font-size: 1.1em;
    color: white;
    background-color: black;
}
/* comment #2 */
h1, h2, h3 {
    font-family: sans-serif;
}
p {
    font-size: 1.2em;
}
/* one more comment */
.float-right {
    float: right;
}
"""


@pytest.fixture
def css_code_1_split():
    code_split = css.separate_code(css_code_1_with_comments)
    return code_split


def test_separate_code_for_3_comments(css_code_1_split):
    assert len(css_code_1_split['comments']) == 3


def test_separate_code_for_3_css_items(css_code_1_split):
    assert len(css_code_1_split['code']) == 3
