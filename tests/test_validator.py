import validator as val
import pytest

html_files = val.get_html_file_names()
browser = val.browser
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
# Fixtures
@pytest.mark.parametrize('filename', html_files)
def test_no_html_validator_errors(filename):
  path = './project/' + filename
  no_errors = val.get_markup_validity(path)
  num_errors = len(no_errors)
  assert num_errors == 0

@pytest.fixture
def invalid_results():
  results = val.validate_css(invalid_css_code)
  return results

@pytest.fixture
def errors_list(invalid_results):
  errors = val.get_css_errors_list(invalid_results)
  return errors

@pytest.fixture
def valid_results():
  results = val.validate_css(valid_css_code)
  return results

# Test HTML validation

# Test CSS validation
def test_css_validator_link():
  response = browser.open("https://jigsaw.w3.org/css-validator")
  results = response.status_code
  assert results == 200

def test_is_css_valid_for_no_errors():
  expected = True
  results = val.is_css_valid(valid_css_code)
  assert expected == results

def test_is_css_valid_for_errors():
  expected = False
  results = val.is_css_valid(invalid_css_code)
  assert expected == results

def test_get_num_errors_three(errors_list):
  expected = 2
  results = val.get_num_errors(errors_list)
  assert results == expected

def test_get_css_errors_with_valid_css(valid_results):
  expected = []
  results = val.get_css_errors_list(valid_results)
  assert results == expected

def test_clean_error_msg():
  expected = "Value Error: display phred is not a display value: phred"
  msg = '\n                                Value Error :  display                                             phred is not a display value : \n                                            \n                                    phred\n                                \n'
  results = val.clean_error_msg(msg)
  assert results == expected

def test_validate_css_with_no_errors(valid_results):
  results = val.validate_css(valid_css_code)
  assert results == valid_results

def test_validate_css_with_errors(invalid_results):
  results = val.validate_css(invalid_css_code)
  assert results == invalid_results