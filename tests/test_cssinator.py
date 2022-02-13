import pytest
import webanalyst.CSSinator as css
import webanalyst.clerk as clerk

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
    "invalid3": "property:val; something"}

declaration_block_with_selector = """
article#gallery {
    display: flex;
    flex-wrap: wrap;
    width: 96vw;
    margin: 0 auto;
}
"""
minified_declaration_block_with_selector = "article#gallery {display: flex;flex-wrap: wrap;width: 96vw;margin: 0 auto;}"

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

selectors_with_3_ids = "body #nav div#phred, p#red"
selectors_with_no_ids = "h1, h2, h3, a:active"

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
        "tests/test_files/projects/large_project/css/layout.css")
    yield layout_css


@pytest.fixture
def layout_css_at_rules(layout_css):
    rulesets = css.NestedAtRule(layout_css)
    yield rulesets


@pytest.fixture
def layout_css_stylesheet(layout_css):
    css_sheet = css.Stylesheet("layout.css", layout_css)
    return css_sheet

def test_separate_code_for_3_comments(css_code_1_split):
    assert len(css_code_1_split['comments']) == 3


def test_separate_code_for_3_css_items(css_code_1_split):
    assert len(css_code_1_split['code']) == 3

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
    assert sheet.text == minified_declaration_block_with_selector


def test_style_sheet_object_extract_comments(layout_css_stylesheet):
    assert len(layout_css_stylesheet.comments) == 6


def test_style_sheet_object_extract_comments_for_first_comment(layout_css_stylesheet):
    assert layout_css_stylesheet.comments[0] == "/* layout.css */"


def test_stylesheet_extract_comments_for_code_after_extraction(layout_css_stylesheet):
    assert len(layout_css_stylesheet.comments) == 6


def test_stylesheet_extract_text_after_code_extraction(layout_css_stylesheet):
    assert layout_css_stylesheet.text[:6] == "body {"


def test_stylesheet_for_extracted_nested_at_rules(layout_css_stylesheet):
    assert len(layout_css_stylesheet.nested_at_rules) == 4

# Test properties of Stylesheet
def test_stylesheet_for_selectors_with_one(stylesheet_with_one_declaration_block):
    assert len(stylesheet_with_one_declaration_block.selectors) == 1

def test_layout_css_stylesheet_for_multiple_selectors(layout_css_stylesheet):
    assert len(layout_css_stylesheet.selectors) == 22
    
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
    
def test_get_class_score_for_0_results():
    results = css.get_class_score(selectors_with_3_ids)
    assert results == 0
    
def test_get_class_score_for_3_results():
    selector = "a:hover, a:link, input[type=text]"
    results = css.get_class_score(selector)
    assert results == 3