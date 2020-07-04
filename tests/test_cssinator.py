# test_cssinator.py

import pytest
import CSSinator

browser = CSSinator.browser
valid_css_code = "p { font-size: 3em; }"
invalid_css_code = """ body {
   font-family: Arial, Helvetica, sans-serif;
   font-size: 100pct;
 }
 #graphic, h1 {
   text-align: center;
 }
 p {
   align: left;
 }"""

@pytest.fixture
def invalid_results():
  results = CSSinator.validate_css(invalid_css_code)
  return results

@pytest.fixture
def errors_list(invalid_results):
  errors = CSSinator.get_css_errors_list(invalid_results)
  return errors

@pytest.fixture
def valid_results():
  results = CSSinator.validate_css(valid_css_code)
  return results

def test_css_validator_link():
  response = browser.open("https://jigsaw.w3.org/css-validator")
  results = response.status_code
  assert results == 200

def test_is_css_valid_for_no_errors():
  expected = True
  results = CSSinator.is_css_valid(valid_css_code)
  assert expected == results

def test_is_css_valid_for_errors():
  expected = False
  results = CSSinator.is_css_valid(invalid_css_code)
  assert expected == results

def test_get_num_errors_three(errors_list):
  expected = 2
  results = CSSinator.get_num_errors(errors_list)
  assert results == expected

def test_get_css_errors_with_valid_css(valid_results):
  expected = []
  results = CSSinator.get_css_errors_list(valid_results)
  assert results == expected

def test_clean_error_msg():
  expected = "Value Error: display phred is not a display value: phred"
  msg = '\n                                Value Error :  display                                             phred is not a display value : \n                                            \n                                    phred\n                                \n'
  results = CSSinator.clean_error_msg(msg)
  assert results == expected

def test_validate_css_with_no_errors(valid_results):
  results = CSSinator.validate_css(valid_css_code)
  assert results == valid_results

def test_validate_css_with_errors(invalid_results):
  results = CSSinator.validate_css(invalid_css_code)
  assert results == invalid_results