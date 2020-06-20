import validator as val
import pytest

# Get all files in project with *.html extension
# append them to a list
html_files = val.get_html_file_names()

@pytest.mark.parametrize('filename', html_files)
def test_no_html_validator_errors(filename):
  path = './project/' + filename
  no_errors = val.get_markup_validity(path)
  num_errors = len(no_errors)
  assert num_errors == 0

# type(no_errors)
# print("There are {} errors.".format(val.get_num_errors(no_errors)))

# with_errors = val.get_markup_validity('tests/test_files/sample_with_errors.html')
# for i in with_errors:
#   print(i)