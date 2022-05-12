code = (
    "header h1 {background-color: rgb(114, 101, 87);}"
    "#menu-toggle.closed {transform: rotate(0deg);}}"
    "@media only screen and (min-width: 660px) {nav ul {"
    "flex-direction: row;}}@media only screen and "
    "(min-width: 911px) {header {display: flex;"
    "flex-direction: row;justify-content: space-between;"
    "border-bottom: .1rem solid rgb(114, 101, 87);"
    "margin-bottom: 2rem;}#menu-toggle {height: 0;"
    "opacity: 0;}nav.closed {top: 3.5rem;}nav li > a {"
    "font-size: 1.3rem;}}"
)


def restore_braces(split):
    result = []
    if len(split) <= 1:
        return split
    for item in split:
        if len(item) > 0:
            item = item + "}}"
            result.append(item)
    return result


def get_nested_at_rule(code, rule):
    at_rule = []
    at_split = code.split(rule)
    if len(at_split) > 1:
        if at_split[0] == "":
            # rule was at the beginning
            at_rule.append(rule + " " + at_split[1])
        else:
            at_rule.append(rule + " " + at_split[0])
    return at_rule


split_code = code.split("}}")
split_code = restore_braces(split_code)
code_segments = []

at_rules = []
for i in split_code:
    at_rule = get_nested_at_rule(i, "@media")
    if at_rule == []:
        continue
    at_rules.append(at_rule)

print(at_rules)
