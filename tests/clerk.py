# clerk.py
import io 
import os.path
import AdvancedHTMLParser as h_parser

def file_to_string(path):
  THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
  my_file = os.path.join(THIS_FOLDER, path)
  f = open(my_file, "r")
  file = f.read()
  file = file.replace('\n','')
  file = file.replace('  ', '')
  return file 

def get_file_type(path):
  extension = os.path.splitext(path)[1]
  return extension [1:]

def get_css(path):
  css = ''
  full_code = file_to_string(path)
  parser = h_parser.AdvancedHTMLParser()
  parser.parseStr(full_code)
  css_advancedTag = parser.getElementsByTagName('style')
  css = css_advancedTag[0].innerText
  return css

if __name__ == "__main__":
  html_with_css = "test_files/html_with_css.html"
  extension = get_file_type(html_with_css)
  type(extension)
  code_string = file_to_string(html_with_css)
  css_code = get_css(html_with_css)
  type(css_code)