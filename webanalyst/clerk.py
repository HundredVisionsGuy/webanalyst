# clerk.py
import collections
import re
from pathlib import Path

import AdvancedHTMLParser as h_parser

working_dir = Path.cwd()
# sentence splitting patterns
alphabets = r"([A-Za-z])"
prefixes = r"(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = r"(Inc|Ltd|Jr|Sr|Co)"
starters = r"(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|"
starters += r"Their\s|Our\s|We\s|But\s|However\s|"
starters += r"That\s|This\s|Wherever)"
acronyms = r"([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = r"[.](com|net|org|io|gov)"
# tag removal pattern
TAG_RE = re.compile(r"<[^>]+>")


def file_exists(filename):
    filename = Path(filename)
    return filename.exists()


def delete_file(filepath):
    data_file = Path(filepath)
    try:
        data_file.unlink()
    except IsADirectoryError as e:
        print(f"Error: {data_file} : {e.strerror}")


def get_path_list(path):
    path_list = path.split("/")
    return path_list


def get_full_path_string(path):
    """path must be a relative path starting with working directory"""
    full_path = working_dir
    p_list = get_path_list(path)
    for i in p_list:
        full_path = full_path / i
    return full_path


def file_to_string(path):
    my_file = get_full_path_string(path)
    file = my_file.read_text(encoding="utf-8")
    return file


def get_file_type(path):
    my_file = get_full_path_string(path)
    suffix = my_file.suffix
    return suffix[1:]


def get_file_name(path):
    return Path(path).name


def get_css_from_style_tag(path):
    full_code = file_to_string(path)
    parser = h_parser.AdvancedHTMLParser()
    parser.parseStr(full_code)
    css_advancedTag = parser.getElementsByTagName("style")
    return css_advancedTag[0].innerText


def get_linked_css(contents_str):
    """returns a list of linked CSS files"""
    filenames = []
    parser = h_parser.AdvancedHTMLParser()
    parser.parseStr(contents_str)
    linked_files = parser.getElementsByTagName("link")
    if len(linked_files) > 1:
        for file in linked_files:
            linked_file = file.getAttribute("href")
            if "https://" in linked_file:
                continue
            filenames.append(linked_file)
    elif len(linked_files) == 1:
        filename = linked_files[0].getAttribute("href")
        filenames.append(filename)
    else:
        return None
    return filenames


def get_css_from_stylesheet(path):
    return file_to_string(path)


def get_all_project_files(dir):
    files = []
    files += get_all_files_of_type(dir, "html")
    files += get_all_files_of_type(dir, "css")
    files += get_all_files_of_type(dir, "js")
    return files


def get_all_files_of_type(dir, filetype):
    pattern = "*." + filetype + "*"
    output = []
    files = collections.Counter(str(f) for f in Path(dir).rglob(pattern))
    output += files.keys()
    return output


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub(r"\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(
        alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]",
        "\\1<prd>\\2<prd>\\3<prd>",
        text,
    )
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if '"' in text:
        text = text.replace('."', '".')
    if "!" in text:
        text = text.replace('!"', '"!')
    if "?" in text:
        text = text.replace('?"', '"?')
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def remove_tags(element):
    """Removes all HTML tags from block tag (str)"""
    return TAG_RE.sub("", element)


def clear_extra_text(str):
    """Removes line returns and extra spaces"""
    str = str.replace("\n", "")
    str = re.sub(r"\s+", " ", str)
    return str.strip()


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

    # extract CSS code from the style tag
    css_code = get_css_from_style_tag(html_with_css)

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
