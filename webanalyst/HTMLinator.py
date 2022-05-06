# HTMLinator.py
# by Hundredvisionsguy
# A library to assess HTML levels and skills

import os
import re

from bs4 import BeautifulSoup
from lxml import html

from . import clerk


def get_html(path):
    with open(path, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        return soup
    return None


def get_num_elements_in_file(el, path):
    with open(path, encoding="utf-8") as fp:
        if (
            el.lower() in ["doctype", "html", "head", "title", "body"]
            and el.lower() != "header"
        ):
            # bs4 won't find doctype
            contents = fp.read()
            contents = contents.lower()
            substring = el.lower()
            if el.lower() == "doctype":
                substring = "<!" + substring
            else:
                substring = "<" + substring

            # if the element is the head, you must use a regex
            # to not count the <header> tag
            if el.lower() == "head":
                count = len(re.findall(r"<head[\s>]", contents))
            else:
                count = contents.count(substring)
            # return the number of doctypes
            return count
        soup = BeautifulSoup(fp, "html.parser")
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
    with open(path, encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        elements = soup.find_all(el)
    return elements


def get_element_content(el):
    return el.get_text()


def uses_inline_styles(markup):
    tree = html.fromstring(markup)
    tags_with_inline_styles = tree.xpath("//@style")
    return bool(tags_with_inline_styles)


if __name__ == "__main__":
    file_with_inline_styles = "tests/test_files/sample_with_inline_styles.html"
    markup = clerk.file_to_string(file_with_inline_styles)
    has_inline_styles = uses_inline_styles(markup)
    print(has_inline_styles)
