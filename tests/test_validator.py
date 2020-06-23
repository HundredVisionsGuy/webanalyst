import validator as val
import pytest

# Get all files in project with *.html extension
# append them to a list
html_files = val.get_html_file_names()

@pytest.mark.parametrize('filename', html_files)
def test_no_html_validator_errors(filename):
  path = './project/' + filename
  no_errors = val.get_markup_validity(path)
  num_errors = len(no_errors)
  assert num_errors == 0

def test_get_css_validity_with_errors():
  error_str = "p } color: blue;{"
  is_valid = val.is_css_str_valid(error_str)
  assert is_valid == False

def test_get_css_validity_with_no_errors():
  code = "p { color: #336600; }"
  is_valid = val.is_css_str_valid(code)
  assert is_valid == True

def test_get_css_errors_no_start_curley():
  css_error = val.get_css_errors('p } color: #336699; }')
  expected = "CSSStyleRule: No start { of style declaration found: 'p } color: #336699; }' [1:22: ]"
  assert css_error == expected