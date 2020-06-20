import pytest
import clerk 

css_file_path = 'test_files/test.css'
html_file_path = 'test_files/sample_no_errors.html'

def test_get_file_type_for_html():
  filetype = clerk.get_file_type(html_file_path)
  assert filetype == 'html'

def test_get_file_type_for_css():
  filetype = clerk.get_file_type(css_file_path)
  assert filetype == 'css'