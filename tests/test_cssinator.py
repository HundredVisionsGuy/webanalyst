import pytest

from webanalyst import CSSinator as css
from webanalyst import clerk

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
declarations = {
    "valid1": "color: #336699;",
    "invalid1": "value;",
    "invalid2": "property:;",
    "invalid3": "property:val; something",
}

declaration_block_with_selector = """
article#gallery {
    display: flex;
    flex-wrap: wrap;
    width: 96vw;
    margin: 0 auto;
}"""

minified_declaration_block_with_selector = "article#gallery "
minified_declaration_block_with_selector += "{display: flex;flex-wrap: "
minified_declaration_block_with_selector += "wrap;width: 96vw;margin: 0 auto;}"

invalid_css = """
body }
    background: #efefef;
    color: #101010;
{
"""

declaration_block_just_block = """
    width: 200px;
    background-color: #7D8C45;
    padding: .7em;
    border: .3em solid #142326;
    margin: .5rem;
"""

css_with_comments = """
/* css.css */
body { font-size: 120%; }
/* other comment */
h1 { font-family: serif;}
"""
# specificity of 303
selectors_with_3_ids = "body #nav div#phred, p#red"
# specificity of 014
selectors_with_no_ids = "h1, h2, h3, a:active"
specificity303 = selectors_with_3_ids
specificity014 = selectors_with_no_ids

insane_gradient = """
-moz-radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
-webkit-radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
-o-radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
-ms-radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
radial-gradient(0% 200%, ellipse cover,
rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) 40%),
-moz-linear-gradient(top, rgba(169, 235, 206,.25) 0%,
rgba(42,60,87,.4) 200%),
-ms-linear-gradient(-45deg, #46ABA6 0%, #092756 200%)',
linear-gradient(-45deg, #46ABA6 0%, #092756 200%)'
"""

path_to_gradients_project = "tests/test_files/"
path_to_gradients_project += "projects/page_with_gradients_and_alpha/style.css"


@pytest.fixture
def stylesheet_with_gradients():
    css_code = clerk.file_to_string(path_to_gradients_project)
    stylesheet = css.Stylesheet("style.css", css_code)
    return stylesheet


@pytest.fixture
def css_code_1_split():
    code_split = css.separate_code(css_code_1_with_comments)
    return code_split


@pytest.fixture
def ruleset1():
    ruleset = css.Ruleset(declaration_block_with_selector)
    return ruleset


@pytest.fixture
def invalid_ruleset():
    ruleset = css.Ruleset(invalid_css)
    return ruleset


@pytest.fixture
def valid_color_declaration():
    dec = css.Declaration(declarations["valid1"])
    return dec


@pytest.fixture
def stylesheet_with_one_declaration_block():
    sheet = css.Stylesheet("local", declaration_block_with_selector, "")
    return sheet


@pytest.fixture
def declaration_block_no_selector():
    block = css.DeclarationBlock(declaration_block_just_block)
    return block


@pytest.fixture
def declaration_block_with_one_selector():
    block = css.DeclarationBlock(declaration_block_with_selector)
    return block


@pytest.fixture
def layout_css():
    layout_css = clerk.file_to_string(
        "tests/test_files/projects/large_project/css/layout.css"
    )
    yield layout_css


@pytest.fixture
def layout_css_at_rules(layout_css):
    rulesets = css.NestedAtRule(layout_css)
    yield rulesets


@pytest.fixture
def layout_css_stylesheet(layout_css):
    css_sheet = css.Stylesheet("layout.css", layout_css)
    return css_sheet


@pytest.fixture
def styles_with_multiple_selectors():
    styles = clerk.file_to_string(
        "tests/test_files/multiple_selectors.css"
    )
    sheet = css.Stylesheet("multiple_selectors.css", styles)
    yield sheet


@pytest.fixture
def navigation_styles():
    path = "tests/test_files/projects/large_project/css/"
    path += "navigation.css"
    styles = clerk.file_to_string(path)
    sheet = css.Stylesheet("navigation.css", styles)
    yield sheet


def test_separate_code_for_3_comments(css_code_1_split):
    assert len(css_code_1_split["comments"]) == 3


def test_separate_code_for_3_css_items(css_code_1_split):
    assert len(css_code_1_split["code"]) == 3


def test_ruleset1_for_selector(ruleset1):
    assert ruleset1.selector == "article#gallery"


def test_invalid_ruleset_for_swapped_brace_position(invalid_ruleset):
    assert not invalid_ruleset.is_valid


def test_ruleset1_for_validity(ruleset1):
    assert ruleset1.is_valid


def test_declaration_block_with_selector(declaration_block_with_one_selector):
    assert len(declaration_block_with_one_selector.declarations) == 4


def test_declaration_block_without_selector(declaration_block_no_selector):
    assert len(declaration_block_no_selector.declarations) == 5


def test_valid_color_declaration_property(valid_color_declaration):
    expected = "color"
    results = valid_color_declaration.property
    assert expected == results


def test_valid_color_declaration_is_valid(valid_color_declaration):
    assert valid_color_declaration.is_valid


def test_missing_end_semicolon_for_true_and_false():
    missing = "body {\n    font-size: 20px;\n    font-family: sans-serif"
    missing += "\ncolor: #336699\n}"
    result = css.missing_end_semicolon(missing)
    assert not result

    including = "body {\n    font-size: 20px;\n    font-family: sans-serif"
    including += "\ncolor: #336699;\n}"
    result = css.missing_end_semicolon(including)
    assert result


def test_invalid1_declaration_is_valid():
    dec = css.Declaration(declarations["invalid1"])
    assert not dec.is_valid


def test_invalid2_declaration_is_valid():
    dec = css.Declaration(declarations["invalid2"])
    assert not dec.is_valid


def test_invalid3_declaration_is_valid():
    dec = css.Declaration(declarations["invalid3"])
    assert not dec.is_valid


def test_nested_at_rules_for_three(layout_css):
    assert "@media" in layout_css


def test_nested_at_rules_for_non_nested_at_rule():
    with pytest.raises(Exception):
        css.NestedAtRule(declaration_block_with_selector)


def test_nested_at_rules_for_rules(layout_css_at_rules):
    rule = "@keyframes pulse"
    expected = layout_css_at_rules.rule
    assert rule == expected


def test_style_sheet_object_minify_method():
    sheet = css.Stylesheet("local", declaration_block_with_selector)
    results = css.minify_code(sheet.text)
    assert results == minified_declaration_block_with_selector


def test_style_sheet_object_extract_comments(layout_css_stylesheet):
    assert len(layout_css_stylesheet.comments) == 6


def test_style_sheet_object_extract_comments_for_first_comment(
    layout_css_stylesheet,
):
    assert layout_css_stylesheet.comments[0] == "/* layout.css */"


def test_stylesheet_extract_comments_for_code_after_extraction(
    layout_css_stylesheet,
):
    assert len(layout_css_stylesheet.comments) == 6


def test_stylesheet_extract_text_after_code_extraction(layout_css_stylesheet):
    assert layout_css_stylesheet.text[:6] == "body {"


def test_stylesheet_for_extracted_nested_at_rules(layout_css_stylesheet):
    assert len(layout_css_stylesheet.nested_at_rules) == 4


# Test properties of Stylesheet
def test_stylesheet_for_selectors_with_one(
    stylesheet_with_one_declaration_block,
):
    assert len(stylesheet_with_one_declaration_block.selectors) == 1


def test_layout_css_stylesheet_for_multiple_selectors(layout_css_stylesheet):
    assert len(layout_css_stylesheet.selectors) == 21


def test_has_required_property_for_display(layout_css_stylesheet):
    assert css.has_required_property("display", layout_css_stylesheet)


def test_has_required_property_for_border_radius(layout_css_stylesheet):
    assert css.has_required_property("border-radius", layout_css_stylesheet)


def test_get_id_score_for_3_ids():
    results = css.get_id_score(selectors_with_3_ids)
    assert results == 3


def test_get_id_score_for_no_ids():
    results = css.get_id_score(selectors_with_no_ids)
    assert not results


def test_get_type_score_for_3_type_selectors():
    results = css.get_type_score(selectors_with_3_ids)
    assert results == 3


def test_get_type_score_for_4_type_selectors():
    results = css.get_type_score(selectors_with_no_ids)
    assert results == 4


def test_get_type_score_for_descendant_selectors():
    selector = "header h1"
    results = css.get_type_score(selector)
    assert results == 2


def test_get_class_score_for_0_results():
    results = css.get_class_score(selectors_with_3_ids)
    assert results == 0


def test_get_class_score_for_3_results():
    selector = "a:hover, a:link, input[type=text]"
    results = css.get_class_score(selector)
    assert results == 3


def test_get_specificity_for_303():
    results = css.get_specificity(specificity303)
    assert results == "303"


def test_get_specificity_for_014():
    results = css.get_specificity(specificity014)
    assert results == "014"


def test_get_specificity_for_033():
    selector = "a:hover, a:link, input[type=text]"
    results = css.get_specificity(selector)
    assert results == "033"


def test_get_specificity_for_002():
    selector = "header h1"
    results = css.get_specificity(selector)
    assert results == "002"


def test_has_vendor_prefix_for_false():
    selector = "transition"
    results = css.has_vendor_prefix(selector)
    expected = False
    assert results == expected


def test_has_vendor_prefix_for_webkit():
    selector = "-webkit-transition"
    results = css.has_vendor_prefix(selector)
    expected = True
    assert results == expected


def test_has_vendor_prefix_for_moz():
    selector = "-moz-transition"
    results = css.has_vendor_prefix(selector)
    expected = True
    assert results == expected


def test_has_vendor_prefix_for_property_with_dash_not_prefix():
    selector = "background-color"
    results = css.has_vendor_prefix(selector)
    expected = False
    assert results == expected


def test_is_gradient_for_false():
    value = "rgba(155, 155, 155, 0)"
    results = css.is_gradient(value)
    assert not results


def test_is_gradient_for_true():
    value = "-moz-radial-gradient(0% 200%, ellipse cover, "
    value += "rgba(143, 193, 242, 0.22) 10%,rgba(240, 205, 247,0) "
    value += "40%),-moz-linear-gradient(top, rgba(169, 235, 206,"
    value += ".25) 0%, rgba(42,60,87,.4) 200%), "
    value += "-moz-linear-gradient(-45deg, #46ABA6 0%, #092756 200%)"
    results = css.is_gradient(value)
    assert results


def test_process_gradient_for_insane_css_for_four_returned_colors():
    colors = css.process_gradient(insane_gradient)
    results = len(colors)
    expected = 4
    assert results == expected


def test_sort_color_codes_for_two_rgbas():
    colors = ['rgba(143, 193, 242, 0.22)', 'rgba(240, 205, 247,0)']
    expected = ['rgba(240, 205, 247,0)', 'rgba(143, 193, 242, 0.22)']
    results = css.sort_color_codes(colors)
    assert results == expected


def test_sort_color_codes_for_three_hexes():
    colors = ['#336699', '#ff0000', '#4C3A51']
    expected = ['#ff0000', '#336699', '#4C3A51']
    results = css.sort_color_codes(colors)
    assert results == expected


def test_get_colors_from_gradient_for_hex():
    gradient = "linear-gradient(-45deg, #46ABA6 0%, #092756 200%)"
    expected = ["#46ABA6", "#092756"]
    results = css.get_colors_from_gradient(gradient)
    assert expected == results


def test_get_colors_from_gradient_for_rgba():
    gradient = "linear-gradient(-45deg, rgba(200, 100, 100, 0.5) 0% #336699 100%)"
    results = css.get_colors_from_gradient(gradient)
    assert "rgba(200, 100, 100, 0.5)" in results


def test_append_color_codes_for_none():
    colors = []
    gradient = "linear-gradient(to bottom, rgba(169, "
    gradient += "235, 206,.25) 0%,rgba(42,60,87,.4) 200%"
    css.append_color_codes("hsl", gradient, colors)
    assert not colors


def test_append_color_codes_for_rgba():
    colors = []
    gradient = (
        "linear-gradient(to bottom, "
        "rgba(169, 235, 206,.25) 0%,rgba(42,60,87,.4) 200%"
    )
    css.append_color_codes("rgb", gradient, colors)
    assert "rgba(169, 235, 206,.25)" in colors


def test_append_color_codes_for_rgb():
    colors = []
    gradient = (
        "linear-gradient(to bottom, rgb(169, 235, " "206,.25) 0%,rgba(42,60,87,.4) 200%"
    )
    css.append_color_codes("rgb", gradient, colors)
    assert "rgb(169, 235, 206,.25)" in colors


def test_append_color_codes_for_hex():
    colors = []
    gradient = "linear-gradient(-45deg, #46ABA6 0%, #092756 200%)"
    css.append_color_codes("hex", gradient, colors)
    assert "#092756" in colors


def test_append_color_codes_for_keyword_antiquewhite():
    colors = []
    gradient = "linear-gradient(-45deg, maroon 0%, #092756 200%)"
    css.append_color_codes("keywords", gradient, colors)
    assert "maroon" in colors


def test_is_required_selector_for_not_required():
    results = css.is_required_selector("id_selector", "nav ul {")
    assert not results


def test_is_required_selector_for_id_selector():
    selector = "main#main nav a.active"
    assert css.is_required_selector("id_selector", selector)


def test_is_required_selector_for_class_selector():
    selector = "main#main nav a.active"
    assert css.is_required_selector("class_selector", selector)


def test_is_required_selector_for_type_selector():
    selector = "main#main nav a.active"
    assert css.is_required_selector("type_selector", selector)


def test_is_required_selector_for_grouped_selectors():
    selector = "h1, h2, h3 {"
    assert css.is_required_selector("grouped_selector", selector)


def test_get_num_required_selectors_for_3_ids():
    css_code = "body #nav div#phred, p#red"
    css_code += "{ color: green;}"
    style_sheet = css.Stylesheet("styletag", css_code)
    results = css.get_number_required_selectors("id_selector", style_sheet)
    expected = 3
    assert results == expected


def test_get_num_required_selectors_for_layout_sheet(layout_css_stylesheet):
    results = css.get_number_required_selectors("class_selector", layout_css_stylesheet)
    expected = 29
    assert results == expected


def test_get_nested_at_rule_selectors(layout_css_stylesheet):
    results = css.get_nested_at_rule_selectors(layout_css_stylesheet)
    count = len(results)
    expected = 5
    assert count == expected


def test_has_repeat_selectors_for_false(navigation_styles):
    assert not css.has_repeat_selector(navigation_styles)


def test_has_repeat_selectors_for_true_layout(layout_css_stylesheet):
    assert css.has_repeat_selector(layout_css_stylesheet)


def test_has_repeat_selectors_for_true(styles_with_multiple_selectors):
    assert css.has_repeat_selector(styles_with_multiple_selectors)


# TODO: test stylesheet_with_gradients for color rulesets
# not sure what we want out of it.
