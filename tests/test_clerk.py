import pytest
import clerk

# TODO - separate tests based on command-line flag
css_file_path = 'tests/test_files/test.css'
html_file_path = 'tests/test_files/sample_no_errors.html'
html_with_css = "tests/test_files/html_with_css.html"
sample_txt_path = 'tests/test_files/sample.txt'
working_dir_txt_path = 'sample.txt'
project_test_css_path = 'project/test.css'


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
    expected = "Sample text from working directory"
    assert sample_text == expected


def test_file_to_string_in_project_directory():
    sample_text = clerk.file_to_string(project_test_css_path)
    expected = "p { display: flex; color: fred; }"
    assert sample_text == expected


def test_get_all_project_files_from_test_project():
    expected = ['tests\\test_files\\project\\gallery.html',
                'tests\\test_files\\project\\index.html',
                'tests\\test_files\\project\\css\\general.css',
                'tests\\test_files\\project\\css\\grid-layout.css',
                'tests\\test_files\\project\\css\\layout.css',
                'tests\\test_files\\project\\css\\navigation.css',
                'tests\\test_files\\project\\js\\scripts.js']
    results = clerk.get_all_project_files('tests/test_files/project')
    assert expected == results


def test_get_all_html_project_files_from_test_project():
    expected = ['tests\\test_files\\project\\gallery.html',
                'tests\\test_files\\project\\index.html']
    results = clerk.get_all_files_of_type('tests/test_files/project', 'html')
    assert expected == results
