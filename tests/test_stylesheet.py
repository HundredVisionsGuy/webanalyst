import pytest 
import stylesheet 
import clerk

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

@pytest.fixture
def ruleset1():
    ruleset = stylesheet.Ruleset(declaration_block_with_selector)
    return ruleset

@pytest.fixture
def invalid_ruleset():
    ruleset = stylesheet.Ruleset(invalid_css)
    return ruleset

@pytest.fixture
def valid_color_declaration():
    dec = stylesheet.Declaration(declarations["valid1"])
    return dec 

@pytest.fixture 
def declaration_block1():
    block = stylesheet.DeclarationBlock(declaration_block_with_selector)
    return block

@pytest.fixture
def declaration_block2():
    block = stylesheet.DeclarationBlock(declaration_block_just_block)
    return block

@pytest.fixture
def layout_css():
    layout_css = clerk.file_to_string("tests/test_files/projects/large_project/css/layout.css")
    yield layout_css

def test_ruleset1_for_selector(ruleset1):
    assert ruleset1.selector == "article#gallery"

def test_invalid_ruleset_for_swapped_brace_position(invalid_ruleset):
    assert not invalid_ruleset.is_valid

def test_ruleset1_for_validity(ruleset1):
    assert ruleset1.is_valid

def test_declaration_block_with_selector(declaration_block1):
    assert len(declaration_block1.declarations) == 4

def test_declaration_block_without_selector(declaration_block2):
    assert len(declaration_block2.declarations) == 5

def test_valid_color_declaration_property(valid_color_declaration):
    expected = "color"
    results = valid_color_declaration.property
    assert expected == results

def test_valid_color_declaration_is_valid(valid_color_declaration):
    assert valid_color_declaration.is_valid

def test_invalid1_declaration_is_valid():
    dec = stylesheet.Declaration(declarations["invalid1"])
    assert not dec.is_valid

def test_invalid2_declaration_is_valid():
    dec = stylesheet.Declaration(declarations["invalid2"])
    assert not dec.is_valid

def test_invalid3_declaration_is_valid():
    dec = stylesheet.Declaration(declarations["invalid3"])
    assert not dec.is_valid

def test_nested_at_rules_for_three(layout_css):
    assert "@media" in layout_css

def test_nested_at_rules_for_non_nested_at_rule():
    with pytest.raises(Exception):
        stylesheet.NestedAtRules(declaration_block_with_selector)