import pytest
import HTMLinator as HT
import clerk
import validator as val
from bs4 import BeautifulSoup

browser = val.browser
html_file_with_errors = "tests/test_files/sample_with_errors.html"


@pytest.fixture
def index_doc():
    doc = """
    <h1>About Me</h1>
    <h2>Background</h2>
    <p>I was born a young child in Phoenix, Arizona. I was the last of five children, but I had a good childhood.</p>
    <p>My favorite memories were of bicycling, exploring the ditch near my house, and making movies with our 8mm camera.
    </p>
    <h2>Hobbies</h2>
    <p>I love to play guitar and code. I have both an electric and acoustic guitar, but I prefer my acoustic.</p>
    """
    index_doc = BeautifulSoup(doc, 'html.parser')
    return index_doc


@pytest.fixture
def p_tags(index_doc):
    return index_doc.find_all("p")


@pytest.fixture
def p_tag():
    p = "<p>I was born a young child in Phoenix, Arizona. I was the last of five children, but I had a good childhood.</p>"
    p_tag = BeautifulSoup(p, 'html.parser')
    return p_tag


@pytest.fixture
def error_report():
    return val.get_markup_validity(html_file_with_errors)


def test_get_number_of_elements_for_p():
    results = HT.get_num_elements('p', html_file_with_errors)
    expected = 2
    assert results == expected


def test_get_number_of_elements_for_none():
    results = HT.get_num_elements('q', html_file_with_errors)
    expected = 0
    assert results == expected


def test_get_elements_for_p_in_index(p_tags):
    path = "tests/test_files/projects/about_me/index.html"
    results = HT.get_elements("p", path)
    expected = p_tags
    assert results == expected


def test_get_element_content_for_p(p_tag):
    results = HT.get_element_content(p_tag)
    expected = "I was born a young child in Phoenix, Arizona. I was the last of five children, but I had a good childhood."
    assert results == expected
