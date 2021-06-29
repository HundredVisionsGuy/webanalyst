# HTMLinator.py
# by Hundredvisionsguy
# A library to assess HTML levels and skills

from attr import attrs
from bs4 import BeautifulSoup
import validator as val
import os
import clerk
import re
from lxml import html


def get_html(path):
    with open(path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        return soup
    return None


def get_num_elements_in_file(el, path):
    with open(path) as fp:
        if el.lower() in ['doctype', 'html', 'head', 'title', 'body']:
            # bs4 won't find doctype
            contents = fp.read()
            contents = contents.lower()
            substring = el.lower()
            if el.lower() == 'doctype':
                substring = '<!' + substring
            else:
                substring = '<' + substring
            count = contents.count(substring)
            # return # of doctypes
            return count
        soup = BeautifulSoup(fp, 'html.parser')
        elements = soup.find_all(el.lower())
    return len(elements)


def get_num_elements_in_folder(el, dir_path):
    elements = 0
    for subdir, dirs, files in os.walk(dir_path):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".html"):
                elements += get_num_elements_in_file(el, filepath)
    return elements


def get_elements(el, path):
    with open(path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        elements = soup.find_all(el)
    return elements


def get_element_content(el):
    return el.get_text()

def uses_inline_styles(markup):
    tree = html.fromstring(markup)
    tags_with_inline_styles = tree.xpath('//@style')
    return bool(tags_with_inline_styles)

if __name__ == "__main__":
    file_with_inline_styles = "tests/test_files/sample_with_inline_styles.html"
    markup = clerk.file_to_string(file_with_inline_styles)
    has_inline_styles = uses_inline_styles(markup)
    print(has_inline_styles)