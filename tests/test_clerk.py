import pytest
import clerk 

css_file_path =  'test_files/test.css'
html_file_path = 'test_files/sample_no_errors.html'
html_with_css =  "test_files/html_with_css.html"
sample_txt_path = 'test_files/sample.txt'

def test_get_file_type_for_html():
  filetype = clerk.get_file_type(html_file_path)
  assert filetype == 'html'

def test_get_file_type_for_css():
  filetype = clerk.get_file_type(css_file_path)
  assert filetype == 'css'

def test_get_css_from_style():
  css_code = clerk.get_css(html_with_css)
  expected = "p {color:red;}"
  assert css_code == expected

def test_file_to_string_with_sample():
  sample_test = clerk.file_to_string(sample_txt_path)
  expected = "Hey!"
  assert sample_test == expected