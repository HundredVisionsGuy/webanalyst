#import pytest
#from html.parser import HTMLParser
import requests
import pycurl
import certifi
import io
import json
import os
import clerk
import cssutils
import subprocess
import sys

parser = cssutils.CSSParser(raiseExceptions=SyntaxError)

def get_markup_validity(filepath):
  w3cURL = 'https://validator.w3.org/nu/?out=json'
  errors = []
  payload = open(filepath)
  with open(filepath,'rb') as payload:
    headers = {'content-type': 'text/html; charset=utf-8', 'Accept-Charset': 'UTF-8'}
    r = requests.post(w3cURL, data=payload, headers=headers)
    errors = r.json()['messages']
  return errors

def is_css_str_valid(str_code):
  try:
    parser.parseString(str_code) 
    return True
  except:
    return False

def get_css_errors(str_code):
  try:
    parser.parseString(str_code)
    return ""
  except Exception as e:
    return str(e)

def get_num_errors(report):
  num = len(report)
  return num

def get_html_file_names():
  names = []
  for filename in os.listdir('./project'):
    if filename.endswith(".html"):
      names.append(filename)
  return names

def get_num_html_files():
  html_files = get_html_file_names()
  return len(html_files)

if __name__ == "__main__":
  path = './project/sample.html'
  report = get_markup_validity(path)
  print("report is a {}.".format(type(report)))
  for item in report:
    print(item)
  
  # how many html files in project directory?
  html_files = get_html_file_names()
  
  # test getting number of errors
  print(get_num_errors(report))
  
  css_code = clerk.get_css('test_files/html_with_css.html')
  is_css_valid = is_css_str_valid(css_code)
  print(is_css_valid)
  is_css_valid = is_css_str_valid("p } color: #336699; }")
  print(is_css_valid)
  print(get_css_errors("#header { display: flex; }"))