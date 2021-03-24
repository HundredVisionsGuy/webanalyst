import pytest 
import stylesheet 

declarations = {
    "valid1": "color: #336699;",
    "invalid1": "value;",
    "invalid2": "property:;",
    "invalid3": "property:val; something"}

@pytest.fixture
def valid_color_declaration():
    dec = stylesheet.Declaration(declarations["valid1"])
    return dec 

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