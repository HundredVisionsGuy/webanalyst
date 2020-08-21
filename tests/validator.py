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
import mechanicalsoup
from pathlib import Path
import bs4
import re

w3cURL = 'https://validator.w3.org/nu/?out=json'

# Instantiate a stateful browser
browser = mechanicalsoup.StatefulBrowser()


def get_num_errors(report):
    return len(report)


def clean_error_msg(msg):
    """ removes new lines, added spaces, and strips spaces """
    msg = msg.replace('\n', '')
    msg = re.sub(r'[ ]{2,}', ' ', msg)
    msg = msg.replace(" :", ":")
    return msg.strip()


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


def get_markup_validity(filepath):
    """ returns a list of errors (dict) """
    errors = []
    payload = open(filepath)
    with open(filepath, 'rb') as payload:
        headers = {'content-type': 'text/html; charset=utf-8',
                   'Accept-Charset': 'UTF-8'}
        r = requests.post(w3cURL, data=payload, headers=headers)
        errors = r.json()['messages']
        print("errors is a {}".format(type(errors)))
        for error in errors:
            print(error)
    return errors


def get_num_markup_errors(markup_errors):
    count = 0
    for i in markup_errors:
        if i['type'] == 'error':
            count += 1
    return count


def get_num_markup_warnings(markup_errors):
    count = 0
    for i in markup_errors:
        if i['type'] == 'info':
            count += 1
    return count


def get_html_file_names(dir_path=r'.' + os.sep + 'project'):
    names = []
    for subdir, dirs, files in os.walk(dir_path):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".html"):
                names.append(filepath)
    return names


def get_num_html_files():
    html_files = get_html_file_names()
    return len(html_files)


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


if __name__ == "__main__":
    path = 'tests/test_files/sample_with_errors.html'
    report = get_markup_validity(path)
    print("report is a {}.".format(type(report)))
    for item in report:
        print(item)
    num_errors = get_num_markup_errors(report)
    # how many html files in project directory?
    html_files = get_html_file_names()

    # test getting number of errorsz
    print(get_num_errors(report))

    css_code = clerk.get_css_from_style_tag(
        'tests/test_files/html_with_css.html')
    is_css_valid = validate_css(css_code)
    print(is_css_valid)
    is_css_valid = validate_css("p } color: #336699; }")
    print(is_css_valid)
    print(validate_css("#header { display: flex; }"))
