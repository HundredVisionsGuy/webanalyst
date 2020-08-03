# HTMLinator.py
# by Hundredvisionsguy
# A library to assess HTML levels and skills

from bs4 import BeautifulSoup
import validator as val


def get_num_elements(el, path):
    with open(path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        elements = soup.find_all(el)
    return len(elements)


def get_elements(el, path):
    with open(path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        elements = soup.find_all(el)
    return elements


def get_element_content(el):
    return el.get_text()


if __name__ == "__main__":
    p = "<p>I was born a young child in Phoenix, Arizona. I was the last of five children, but I had a good childhood.</p>"
    p_tag = BeautifulSoup(p, 'html.parser')
    print(str(p_tag))
    print("Hello")
    html_file_with_errors = "tests/test_files/sample_no_errors.html"
    with open(html_file_with_errors) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        ps = get_num_elements('p', html_file_with_errors)
        print("There are {} {} elements in '{}'".format(
            ps, 'p', html_file_with_errors))
        p_list = get_elements('p', html_file_with_errors)
        for p in p_list:
            print(p.contents[0])
