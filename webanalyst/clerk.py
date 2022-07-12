"""A collection of functions for dealing with files and file content.

This was a library I created for previous projects that deal with files
and file paths in order to get code from files, lists of files in
project folders, file extensions, and allows us to capture just files
of a particular type. I also developed my projects on Windows OS, so
these functions were designed to work with the file paths on Windows,
Mac, and Linux (Windows is the one with backslashes - wacky, I know.).

  Typical usage example:

  extension = get_file_type("path/to/file.js")

  code_string = file_to_string("path/to/file.html")

  project_path = "path/to/project"
  all_project_files = get_all_project_files(project_path)
  just_css_files = get_all_files_of_type(project_path, "css")
"""
# SPDX-License-Identifier: BSD-3-Clause

import collections
import re
from pathlib import Path
import nltk
from bs4 import BeautifulSoup

nltk.download('punkt')
working_dir = Path.cwd()

# tag removal pattern
TAG_RE = re.compile(r"<[^>]+>")


def file_exists(file_path: str) -> bool:
    """ Returns True or False: whether file in path exists.

    Args:
        file_path (str): The file location

    Returns:
        bool: True or False: True if file exists False if not
    """
    filename = Path(file_path)
    return filename.exists()


def delete_file(filepath: str):
    """ deletes file in path but only if it exists

    Args:
        file_path (str): The file location

    Returns:
        None
    """
    data_file = Path(filepath)
    try:
        data_file.unlink()
    except IsADirectoryError as e:
        print(f"Error: {data_file} : {e.strerror}")


def get_path_list(path: str) -> list:
    """ Returns a list of each path part using slash as separator.

    Args:
        file_path (str): The file location using the Posix format
            (forward/slashes)

    Returns:
        path_list (list): A path of each folder in a path, with the
            file at the end.
            Example: path/to/file.ext will be
            ["path", "to", "file.ext"]
    """
    path_list = path.split("/")
    return path_list


def get_full_path_string(path: str):
    """returns absolute path to file in relative path.

    Args:
        file_path (str): The file location using the Posix format
            (forward/slashes)

    Returns:
        full_path (Path Object): will be a WindowsPath (if Windows) or
            PosixPath (if Mac or Linux)
    """
    full_path = working_dir
    p_list = get_path_list(path)
    for i in p_list:
        full_path = full_path / i
    return full_path


def file_to_string(path: str) -> str:
    """ Returns contents of file as a string.

    Args:
        path (str): The path to a file using Posix format (forward
            slashes e.g. path/to/file.ext)

    Returns:
        file_text (str): The contents of the file in utf-8 string
            format.
    """
    my_file = get_full_path_string(path)
    file_text = my_file.read_text(encoding="utf-8")
    return file_text


def get_file_type(path: str) -> str:
    """ returns the extension of the file in the path.

    Args:
        path (str): The path to a file using Posix format (forward
            slashes e.g. path/to/file.ext)

    Returns:
        extension (str): The extension of the file type (without)
        the dot (eg. html, js, css, pdx, png)
    """
    my_file = get_full_path_string(path)
    suffix = my_file.suffix
    extension = suffix[1:]
    return extension


def get_file_name(path: str) -> str:
    """ returns the name of the file in the path.

    Args:
        path (str): The path to a file using Posix format (forward
            slashes e.g. path/to/file.ext)

    Returns:
        filename (str): The name of the file (with extension)
    """
    filename = Path(path).name
    return filename


def get_linked_css(contents_str: str) -> list:
    """returns a list of linked CSS files.

    Args:
        contents_str (str): HTML code from a file in string format.

    Returns:
        filenames (list): A list of all filenames extracted from CSS
            link tags.
            Note: no external stylesheets will be included (only
            local files).
    """
    filenames = []
    soup = BeautifulSoup(contents_str, "html.parser")
    linked_files = soup.find_all("link")

    if len(linked_files) > 1:
        for file in linked_files:
            linked_file = file.attrs.get('href')
            if "https://" in linked_file or "http://" in linked_file:
                continue
            filenames.append(linked_file)
    elif len(linked_files) == 1:
        filename = linked_files[0].attrs.get('href')
        if "https://" in filename or "http://" in filename:
            return None
        filenames.append(filename)
    else:
        return None
    return filenames


def get_all_project_files(dir_path: str) -> list:
    """ returns a list of all files from the directory in the path.

    Args:
        dir_path (str): The path to a directory using Posix format
            (forward slashes e.g. path/to/file.ext)

    Returns:
        files (list): A list of all html, css, and javascript files
    """
    files = []
    files += get_all_files_of_type(dir_path, "html")
    files += get_all_files_of_type(dir_path, "css")
    files += get_all_files_of_type(dir_path, "js")
    return files


def get_all_files_of_type(dir_path: str, filetype: str) -> list:
    """ returns all files of a particular type from a directory.

    Args:
        dir_path (str): The path to a directory using Posix format
            (forward slashes e.g. path/to/file.ext)
        file_type (str): An extension in the form of a string (without
            the dot (html, css, js, etc.))

    Returns:
        files (list): A list of all html, css, and javascript files
    """
    pattern = "*." + filetype + "*"
    output = []
    files = collections.Counter(str(f) for f in Path(dir_path).rglob(pattern))
    output += files.keys()
    return output


def split_into_sentences(contents: str) -> list:
    """ Returns a list of each sentence from the text.

    Args:
        contents (str): A string of text (typically from a tag) that
            most likely has punctuation.

    Returns:
        sentences (list): A list of each sentence from the text
            each in string format
    """
    sentences = nltk.tokenize.sent_tokenize(contents)
    return sentences


def remove_tags(element: str) -> str:
    """Removes all HTML tags from another tag's contents

    Args:
        element (str): the contents of a tag as a string form which might or
        might not have extra tags (in particular inline tags, such as <em>
        or <a>, etc.)

    Returns:
        tagless_content (str): the contents of the tag minus any inner tags.
    """
    tagless_content = TAG_RE.sub("", element)
    return tagless_content


def clear_extra_text(my_text: str) -> str:
    """Removes line returns and extra spaces from my_text.

    Args:
        my_text (str): text which may include line returns or extra space.

    Returns:
        stripped_text (str): text without any line returns or additional spaces.
    """
    my_text = my_text.replace("\n", "")
    my_text = re.sub(r"\s+", " ", my_text)
    stripped_text = my_text.strip()
    return stripped_text


if __name__ == "__main__":
    html_with_css = "./tests/test_files/html_with_css.html"

    # get full path of a relative link
    p_list = get_full_path_string(html_with_css)

    # get the extension of a file
    extension = get_file_type(html_with_css)
    print("the extension for {} is {}".format(html_with_css, extension))

    # get all the code from a file as a string
    code_string = file_to_string(html_with_css)
    print(code_string)

    # test get_all_project_files()
    test_project_files = "project"
    results = get_all_project_files(test_project_files)
    for i in results:
        print(i)

    # test getting list of all files with .css extension
    test_project_files = "./tests/test_files/project"
    results = get_all_files_of_type(test_project_files, "css")
    for i in results:
        print(i)
