# HTMLinator.py
# by Hundredvisionsguy
# A library to assess HTML levels and skills

from bs4 import BeautifulSoup
import validator as val
import os

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


if __name__ == "__main__":
    results = get_html('tests/report_template.html')
    print(results)
    print(type(results))
    gen_results_table = results.find(id="general-results-writing")
    print(gen_results_table)
    other_file = get_html('tests/test_files/html_with_css.html')
    tag = other_file.find("style")
    print(tag)
    # p = "<p>I was born a young child in Phoenix, Arizona. I was the last of five children, but I had a good childhood.</p>"
    # p_tag = BeautifulSoup(p, 'html.parser')
    # print(str(p_tag))
    # html_about_me_folder = "tests/test_files/projects/about_me/"
    # html_file_with_errors = "tests/test_files/sample_with_errors.html"

    # num = get_num_elements_in_file("doctype", html_file_with_errors)
    # print("Hello")
    # html_file_with_errors = "tests/test_files/sample_no_errors.html"
    # with open(html_file_with_errors) as fp:
    #     soup = BeautifulSoup(fp, 'html.parser')
    #     ps = get_num_elements('p', html_file_with_errors)
    #     print("There are {} {} elements in '{}'".format(
    #         ps, 'p', html_file_with_errors))
    #     p_list = get_elements('p', html_file_with_errors)
    #     for p in p_list:
    #         print(p.contents[0])
