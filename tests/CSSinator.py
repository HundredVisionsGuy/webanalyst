# CSSinator.py
# by Chris Winikka
# a set of tools to analyze CSS

import mechanicalsoup
from pathlib import Path
import bs4
import re

# Instantiate a stateful browser
browser = mechanicalsoup.StatefulBrowser()

def is_css_valid(code):
  """Checks to make sure CSS code is valid"""
  validate_css(code)
  return bool(browser.get_current_page().select('#congrats'))

def validate_css(css_code):
  browser.open("https://jigsaw.w3.org/css-validator")
  # Fill-in the search form
  browser.select_form('#validate-by-input form')
  browser["text"] = css_code
  browser.submit_selected()
  results = browser.get_current_page().select('#results_container')
  return results
  
def get_css_errors_list(val_results):
  soup = bs4.BeautifulSoup(str(val_results), 'lxml')
  errors = soup.find_all('td')
  num_errors = len(errors)
  error_list = []
  for i in range(num_errors):
    if (i - 2) % 3 == 0:
      msg = errors[i].text 
      msg = clean_error_msg(msg)
      error_list.append(msg)
  return error_list

def get_num_errors(errors_list):
  return len(errors_list)

def clean_error_msg(msg):
  """ removes new lines, added spaces, and strips spaces """
  msg = msg.replace('\n','')
  msg = re.sub(r'[ ]{2,}', ' ', msg)
  msg = msg.replace(" :", ":")
  return msg.strip()

if __name__ == "__main__":
  resp = browser.open("https://jigsaw.w3.org/css-validator")
  print(resp)
  valid_css = "p { color: #336699; }"
  invalid_css = "p { display: phred; } em { stoiky-lob"

  # validate valid CSS
  results = validate_css(valid_css)
  print(results)
  is_valid = is_css_valid(valid_css)
  print("Are results valid? {}".format(is_valid))

  # validate invalid CSS
  results = validate_css(invalid_css)
  print(results)
  print("Results are of a {} type.".format(type(results)))
  is_valid = is_css_valid(invalid_css)
  print("Are results valid? {}".format(is_valid))

  result_list = get_css_errors_list(results)
  for i in result_list:
    print(i)
  