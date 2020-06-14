#import pytest
#from html.parser import HTMLParser
import requests
import pycurl
import certifi
import io
import json

def validate_html(filepath):
  w3cURL = 'https://validator.w3.org/nu/?out=json'
  errors = []
  payload = open(filepath)
  with open(filepath,'rb') as payload:
    headers = {'content-type': 'text/html; charset=utf-8', 'Accept-Charset': 'UTF-8'}
    r = requests.post(w3cURL, data=payload, headers=headers)
    errors = r.json()['messages']
  return errors

if __name__ == "__main__":
  report = validate_html('./project/sample.html')
  print("report is a {}.".format(type(report)))
  for item in report:
    print(item)