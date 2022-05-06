
import pytest
from webanalyst import clerk

# TODO - separate tests based on command-line flag
css_file_path = 'test_files/projects/large_project/test.css'
html_file_path = 'test_files/sample_no_errors.html'
html_with_css = 'tests/test_files/html_with_css.html'
sample_txt_path = 'tests/test_files/sample.txt'
working_dir_txt_path = './README.md'
project_readme_path = './project/README.md'
report_template_path = './webanalyst/report_template.html'


@pytest.fixture
def test_code_one():
    test_code = """<!DOCTYPE html>\n<html lang="en">\n\n<head>
    <link rel="stylesheet" href="styles.css">    <meta charset="UTF-8">    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Me</title>\n    
    <style>\n        body {
                    color: #121212 background-fred: #f1f1f1;
                            }\n    </style>
    </head>\n\n<h1>About Me<h1>\n        
    <h2>Background</h2>\n        
    <p>I was born a young child in Phoenix, Arizona. 
    I was the last of five children, but I had a good childhood.</p>
    <h2>Hobbies</h2>     
    <p>I love to play <strong>guitar and code. I have both an electric 
    and acoustic guitar, but I prefer my acoustic.</p>
    </html>"""
    return test_code


@pytest.fixture
def test_code_two():
    test_code = """<!DOCTYPE html>\n<html lang="en">\n\n<head>
    <link rel="stylesheet" href="styles.css">    <meta charset="UTF-8">
    <link rel="stylesheet" href="mystyles.css">    
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Me</title>\n    
    <style>\n        body {
                    color: #121212 background-fred: #f1f1f1;
                            }\n    </style>
    </head>\n\n<h1>About Me<h1>\n        
    <h2>Background</h2>\n        
    <p>I was born a young child in Phoenix, Arizona. 
    I was the last of five children, but I had a good childhood.</p>
    <h2>Hobbies</h2>     
    <p>I love to play <strong>guitar and code. I have both an electric 
    and acoustic guitar, but I prefer my acoustic.</p>
    </html>"""
    return test_code


def test_clerk_for_file_exists_for_report_template():
    results = clerk.file_exists(report_template_path)
    expected = True
    assert results == expected


def test_get_file_type_for_html():
    filetype = clerk.get_file_type(html_file_path)
    assert filetype == 'html'


def test_get_file_type_for_css():
    filetype = clerk.get_file_type(css_file_path)
    assert filetype == 'css'


def test_get_css_from_style():
    css_code = clerk.get_css_from_style_tag(html_with_css)
    expected = "p {color:red;}"
    assert css_code == expected


def test_file_to_string_with_sample():
    sample_test = clerk.file_to_string(sample_txt_path)
    expected = "Hey!"
    assert sample_test == expected


def test_file_to_string_in_working_directory():
    sample_text = clerk.file_to_string(working_dir_txt_path)
    sample_text = sample_text[:13]
    expected = "# Web Analyst"
    assert sample_text == expected


def test_file_to_string_in_project_directory():
    readme_text = clerk.file_to_string(project_readme_path)
    expected = "# Project Name: "
    assert expected in readme_text


def test_get_all_project_files_from_large_project():
    expected = ['tests\\test_files\\projects\\large_project\\about.html',
                'tests\\test_files\\projects\\large_project\\gallery.html',
                'tests\\test_files\\projects\\large_project\\index.html',
                'tests\\test_files\\projects\\large_project\\css\\general.css',
                'tests\\test_files\\projects\\large_project\\css\\grid-layout.css',
                'tests\\test_files\\projects\\large_project\\css\\layout.css',
                'tests\\test_files\\projects\\large_project\\css\\navigation.css',
                'tests\\test_files\\projects\\large_project\\js\\scripts.js']
    results = clerk.get_all_project_files(
        'tests/test_files/projects/large_project')
    assert expected == results


def test_get_all_html_project_files_from_large_project():
    expected = ['tests\\test_files\\projects\\large_project\\about.html',
                'tests\\test_files\\projects\\large_project\\gallery.html',
                'tests\\test_files\\projects\\large_project\\index.html']
    results = clerk.get_all_files_of_type(
        'tests/test_files/projects/large_project', 'html')
    assert expected == results


def test_split_into_sentences():
    paragraph = "Hello, you! How are you? i am fine Mr. selenium.\nsee ya later."
    results = len(clerk.split_into_sentences(paragraph))
    expected = 4
    assert results == expected


def test_remove_inline_tags():
    paragraph = '<p>Site designed by <a href="mailto:guy@hundredvisions.com">Hundred visions Guy</a> &copy; 2019.</p>'
    results = clerk.remove_tags(paragraph)
    expected = 'Site designed by Hundred visions Guy &copy; 2019.'
    assert results == expected


def test_get_file_name_for_html_file_path():
    results = clerk.get_file_name(html_file_path)
    expected = 'sample_no_errors.html'
    assert results == expected


def test_get_file_name_for_css_file_path():
    results = clerk.get_file_name(css_file_path)
    expected = "test.css"
    assert results == expected


def test_clear_extra_text():
    sample = "\n             body has something       in here.    "
    expected = "body has something in here."
    results = clerk.clear_extra_text(sample)
    assert results == expected


def test_get_linked_css_for_one_filename(test_code_one):
    results = clerk.get_linked_css(test_code_one)
    assert "styles.css" in results


def test_get_linked_css_for_two_filenames(test_code_two):
    results = clerk.get_linked_css(test_code_two)
    assert "mystyles.css" in results and "styles.css" in results