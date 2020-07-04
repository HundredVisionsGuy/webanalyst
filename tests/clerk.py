# clerk.py
import io 
import AdvancedHTMLParser as h_parser
from pathlib import Path
import collections

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
def get_all_project_files(dir):
  files = []
  files += get_all_files_of_type(dir, 'html')
  files += get_all_files_of_type(dir, 'css')
  files += get_all_files_of_type(dir, 'js')
  return files
def get_all_files_of_type(dir, filetype):
  pattern = "*." + filetype + "*"
  output = []
  files = collections.Counter(str(f) for f in Path(dir).rglob(pattern))
  output += files.keys()
  return output

if __name__ == "__main__":
  html_with_css = "tests/test_files/html_with_css.html"

  # get full path of a relative link
  p_list = get_full_path_string(html_with_css)
  
  # get the extension of a file
  extension = get_file_type(html_with_css)
  print("the extension for {} is {}".format(html_with_css, extension))

  # get all the code from a file as a string
  code_string = file_to_string(html_with_css)
  print(code_string)

  # extract CSS code from the style tag
  css_code = get_css_from_style_tag(html_with_css)

  # test get_all_project_files()
  test_project_files = 'project'
  results = get_all_project_files(test_project_files)
  for i in results:
    print(i)

  # test getting list of all files with .css extension
  test_project_files = 'tests/test_files/project'
  results = get_all_files_of_type(test_project_files, '*.css*')
  for i in results:
    print(i)