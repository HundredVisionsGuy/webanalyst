import stylesheet as styles

# Purpose:
# verify correct syntax using expanded syntax
# see [Use expanded syntax](https://developer.mozilla.org/en-US/docs/MDN/Contribute/Guidelines/Code_guidelines/CSS#Use_expanded_syntax)
# to be used by report.py

def get_repeat_selectors(sheet):
    repeat_selectors = []
    sheet.sort_selectors()
    for selector in sheet.selectors:
        count = sheet.selectors.count(selector)
        if count > 1:
            if [selector, count] not in repeat_selectors:
                repeat_selectors.append([selector, count])
    return repeat_selectors

if __name__ == "__main__":
    import clerk

    # Test off of large project
    layout_css = clerk.file_to_string(
        "tests/test_files/projects/large_project/css/layout.css")
    
    test_sheet = styles.Stylesheet("local", layout_css, "file")
    repeat_selectors = get_repeat_selectors(test_sheet)
    print(repeat_selectors)
