# clerk.py
import io 
import AdvancedHTMLParser as h_parser
from pathlib import Path

working_dir = Path.cwd()

def get_path_list(path):
  path_list = path.split('/')
  return path_list

def get_full_path_string(path):
  """path must be a relative path starting with working directory """
  full_path = working_dir
  p_list = get_path_list(path)
  for i in p_list:
    full_path = full_path / i
  return full_path

def file_to_string(path):
  my_file = get_full_path_string(path) 
  file = my_file.read_text()
  return file 

def get_file_type(path):
  my_file = get_full_path_string(path)
  suffix = my_file.suffix
  return suffix[1:]

def get_css_from_style_tag(path):
  full_code = file_to_string(path)
  parser = h_parser.AdvancedHTMLParser()
  parser.parseStr(full_code)
  css_advancedTag = parser.getElementsByTagName('style')
  return css_advancedTag[0].innerText

def get_all_project_files():
  return []

if __name__ == "__main__":
  html_with_css = "tests/test_files/html_with_css.html"
  p_list = get_full_path_string(html_with_css)
  extension = get_file_type(html_with_css)
  print("the extension for {} is {}".format(html_with_css, extension))
  code_string = file_to_string(html_with_css)
  print(code_string)
  css_code = get_css_from_style_tag(html_with_css)
  print("the type of the CSS code is {}".format(type(css_code)))