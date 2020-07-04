# test_cssinator.py

import pytest
import CSSinator

css_code_repeat_selectors = """p { font-size: 1.1em; }
  p { color: #336699;}
  p { margin: 0}"""

css_code_correct = """p { color: #336699; }
em { display: flex; }"""

@pytest.fixture
def css_list():
  return CSSinator.split_css(css_code_correct) 

def test_for_split_css():
  expected = ['p ', ' color: #336699; ', 'em ', ' display: flex; ', '']
  results = CSSinator.split_css(css_code_correct)
  assert results == expected
def test_get_selectors(css_list):
  expected = ['p', 'em']
  results = CSSinator.get_selectors(css_list)
  assert results == expected
def test_get_declarations(css_list):
  expected = ['color: #336699;', 'display: flex;']
  results = CSSinator.get_declarations(css_list)
  assert results == expected