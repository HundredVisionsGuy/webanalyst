import pytest
import webanalyst.stylesheet_analyst as css_analyst
import webanalyst.CSSinator as styles

css_with_3_repeat_selectors = """
body {
    font-family: calibri, sans-serif;
    font-size: 120%; 
}
h1 { color: green; }
h2 { font-family: tahoma, sans-serif; }
body {
    margin: 0;
    padding: 1em .5em;
}
p { font-size: 1.1em;
}
body {
    line-height: 1.3;
}
"""
css_with_no_repeat_selectors = """
body {
    font-family: calibri, sans-serif;
    font-size: 120%; 
}
h1 { color: green; }
h2 { font-family: tahoma, sans-serif; }
p { font-size: 1.1em;
}
"""

@pytest.fixture
def stylesheet_with_3_repeat_selectors():
    my_stylesheet = styles.Stylesheet("local", css_with_3_repeat_selectors)
    yield my_stylesheet


def test_stylesheet_analyst_for_3_repeat_selectors(stylesheet_with_3_repeat_selectors):
    results = css_analyst.get_repeat_selectors(stylesheet_with_3_repeat_selectors)
    expected = ["body", 3]
    assert expected in results

def test_stylesheet_analyst_for_no_repeat_selectors():
    my_stylesheet = styles.Stylesheet("local", css_with_no_repeat_selectors)
    results = repeat_selectors = css_analyst.get_repeat_selectors(my_stylesheet)
    assert not results

def test_stylesheet_analyst_for_has_type_selector_true(stylesheet_with_3_repeat_selectors):
    assert css_analyst.has_type_selector(stylesheet_with_3_repeat_selectors)