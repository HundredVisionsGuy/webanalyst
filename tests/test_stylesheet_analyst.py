import pytest

from webanalyst import CSSinator as styles
from webanalyst import clerk
from webanalyst import stylesheet_analyst as css_analyst

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
css_with_only_global_color = """
body {
    color: #336699;
    font-family: tahoma, sans-serif;
    font-size: 110%;
}
"""


@pytest.fixture
def stylesheet_with_3_repeat_selectors():
    my_stylesheet = styles.Stylesheet("local", css_with_3_repeat_selectors)
    yield my_stylesheet


@pytest.fixture
def large_project_general_css():
    css = clerk.file_to_string(
        "tests/test_files/projects/large_project/css/general.css"
    )

    test_sheet = styles.Stylesheet("local", css, "file")
    yield test_sheet


@pytest.fixture
def large_project_layout_css():
    css = clerk.file_to_string("tests/test_files/projects/large_project/css/layout.css")

    test_sheet = styles.Stylesheet("local", css, "file")
    yield test_sheet


@pytest.fixture
def large_project_navigation_css():
    css = clerk.file_to_string(
        "tests/test_files/projects/large_project/css/navigation.css"
    )

    test_sheet = styles.Stylesheet("local", css, "file")
    yield test_sheet


@pytest.fixture
def css_with_only_color_applied():
    sheet = styles.Stylesheet("local", css_with_only_global_color, "file")
    return sheet


@pytest.fixture
def css_for_testing():
    css = clerk.file_to_string("tests/test_files/css_for_testing.css")
    sheet = styles.Stylesheet("local", css, "file")
    return sheet


def test_applies_global_colors_for_large_project_general(
    large_project_general_css,
):
    results = css_analyst.applies_global_colors(large_project_general_css)
    assert results


def test_applies_global_colors_for_large_project_layout(
    large_project_layout_css,
):
    results = css_analyst.applies_global_colors(large_project_layout_css)
    assert not results


def test_applies_global_colors_for_just_color_should_fail(
    css_with_only_color_applied,
):
    results = css_analyst.applies_global_colors(css_with_only_color_applied)
    assert not results


def test_stylesheet_analyst_for_3_repeat_selectors(
    stylesheet_with_3_repeat_selectors,
):
    results = css_analyst.get_repeat_selectors(stylesheet_with_3_repeat_selectors)
    expected = ["body", 3]
    assert expected in results


def test_stylesheet_analyst_for_no_repeat_selectors():
    my_stylesheet = styles.Stylesheet("local", css_with_no_repeat_selectors)
    repeat_selectors = css_analyst.get_repeat_selectors(my_stylesheet)
    results = repeat_selectors
    assert not results


def test_stylesheet_analyst_for_has_type_selector_true(
    stylesheet_with_3_repeat_selectors,
):
    assert css_analyst.has_type_selector(stylesheet_with_3_repeat_selectors)


def test_applies_global_font_with_no_global_font_applied(
    large_project_layout_css,
):
    results = css_analyst.applies_global_font(large_project_layout_css)
    assert not results


def test_applies_global_font_with_global_font_applied(
    large_project_general_css,
):
    results = css_analyst.applies_global_font(large_project_general_css)
    assert results


def test_has_descendant_selector_for_false(large_project_general_css):
    results = css_analyst.has_descendant_selector(large_project_general_css)
    assert not results


def test_has_descendant_selector_for_true(large_project_layout_css):
    results = css_analyst.has_descendant_selector(large_project_layout_css)
    assert results


def test_has_descendant_selector_against_multiple_selectors():
    multiple = "h1, h2, h3, h4 { font-size: xx-large; }"
    multiple_sheet = styles.Stylesheet("local", multiple, "text")
    results = css_analyst.has_descendant_selector(multiple_sheet)
    assert not results


def test_has_multiple_selector_for_true():
    multiple = "h1, h2, h3, h4 { font-size: xx-large; }"
    multiple_sheet = styles.Stylesheet("local", multiple, "text")
    results = css_analyst.has_multiple_selector(multiple_sheet)
    assert results


def test_has_multiple_selector_for_false(large_project_navigation_css):
    results = css_analyst.has_multiple_selector(large_project_navigation_css)
    assert not results


def test_has_direct_child_selector_for_true(large_project_navigation_css):
    results = css_analyst.has_direct_child_selector(large_project_navigation_css)
    assert results


def test_has_direct_child_selector_for_false(large_project_general_css):
    results = css_analyst.has_direct_child_selector(large_project_general_css)
    assert not results


def test_has_pseudo_selector_for_true(large_project_navigation_css):
    results = css_analyst.has_psuedoselector(large_project_navigation_css)
    assert results


def test_has_pseudo_selector_for_false(large_project_general_css):
    results = css_analyst.has_psuedoselector(large_project_general_css)
    assert not results


def test_has_repeat_selectors_for_false(large_project_general_css):
    results = css_analyst.has_repeat_selectors(large_project_general_css)
    assert not results


def test_has_repeat_selectors_for_true(css_for_testing):
    results = css_analyst.has_repeat_selectors(css_for_testing)
    assert results


def test_has_class_selector_for_false(large_project_general_css):
    results = css_analyst.has_class_selector(large_project_general_css)
    assert not results


def test_has_class_selector_for_true(large_project_navigation_css):
    results = css_analyst.has_class_selector(large_project_navigation_css)
    assert results


def test_has_id_selector_for_false(large_project_general_css):
    results = css_analyst.has_id_selector(large_project_general_css)
    assert not results


def test_has_id_selector_for_true(large_project_navigation_css):
    results = css_analyst.has_id_selector(large_project_navigation_css)
    assert results
