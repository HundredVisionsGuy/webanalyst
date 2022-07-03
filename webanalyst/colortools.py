import re

"""Main module."""
hex_map = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "a": 10,
    "b": 11,
    "c": 12,
    "d": 13,
    "e": 14,
    "f": 15,
}

contrast_ratio_map = {
    "Normal AA": 4.5,
    "Normal AAA": 7,
    "Large AA": 3,
    "Large AAA": 4.5,
    "Graphics UI components": 3,
}

rgb_all_forms_re = r"rgba\(.*?\)|rgb\(.*?\)"
hsl_all_forms_re = r"hsl\(.*?\)|hsla\(.*?\)"
hex_regex = r"(#\w{3}\s|#\w{6}\s|#\w{8}\s)"


def passes_color_contrast(level, hex1, hex2):
    ratio = contrast_ratio(hex1, hex2)
    min_ratio = contrast_ratio_map[level]
    return ratio >= min_ratio


def get_color_contrast_report(hex1, hex2):
    report = {}
    # check for gradients and apply to every color in the gradient
    # if "gradient" in hex1
    for key, item in contrast_ratio_map.items():
        contrast = contrast_ratio(hex1, hex2)
        passes = "Pass" if contrast >= item else "Fail"
        report[key] = passes
    return report


def rgb_to_hex(*args):
    # are there three separate values or 1 string
    if len(args) == 3:
        r, g, b = args
    else:
        try:
            rgb = args[0]
            r, g, b = extract_rgb_from_string(rgb)
        except Exception:
            # throw an exception
            return "err"
    # Convert r, g, b to hex
    r = hex(int(r))[2:]
    g = hex(int(g))[2:]
    b = hex(int(b))[2:]
    # prepend 0 if necessary
    if len(r) == 1:
        r = "0" + r
    if len(g) == 1:
        g = "0" + g
    if len(b) == 1:
        b = "0" + b
    return "#" + r + g + b


def hex_to_rgb(hex_code):
    """receives hex (str) -> returns rgb as tuple"""
    hex_code = hex_code.lower()
    if "#" in hex_code[0]:
        hex_code = hex_code[1:]
    r = hex_code[:2]
    g = hex_code[2:4]
    b = hex_code[4:]

    r = hex_to_decimal(r)
    g = hex_to_decimal(g)
    b = hex_to_decimal(b)

    return (r, g, b)


def get_hsl_from_string(hsl_string):
    numbers = re.findall("[0-9]+", hsl_string)
    for i in range(len(numbers)):
        numbers[i] = int(numbers[i])
    return tuple(numbers)


def has_alpha_channel(code):
    """returns a true if rgba, hsla, or 8 digit hex code"""
    if "#" in code:
        if len(code) == 9:
            return True
        else:
            return False
    if "hsla(" in code:
        return True
    if "rgba(" in code:
        return True 
    return False


def hsl_to_rgb(hsl):
    # From HSL to RGB color conversion
    # (https://www.rapidtables.com/convert/color/hsl-to-rgb.html)

    h, s, light = hsl
    s /= 100
    light /= 100
    c = (1 - abs(2 * light - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = light - c / 2
    if h < 60:
        r1, g1, b1 = (c, x, 0)
    elif h < 120:
        r1, g1, b1 = (x, c, 0)
    elif h < 180:
        r1, g1, b1 = (0, c, x)
    elif h < 240:
        r1, g1, b1 = (0, x, c)
    elif h < 300:
        r1, g1, b1 = (x, 0, c)
    else:
        r1, g1, b1 = (c, 0, x)
    r = round((r1 + m) * 255)
    g = round((g1 + m) * 255)
    b = round((b1 + m) * 255)
    return r, g, b


def rgb_as_string(rgb):
    """receive rgb as tuple -> returns formatted string"""
    r, g, b = rgb
    return f"rgb({r},{g},{b})"


def hex_to_decimal(c):
    """convert hex code (c) to a decimal value (base 10)"""
    # make sure to convert to lower case
    # so FF becomes ff
    if c[0].lower() not in hex_map.keys():
        raise ValueError(f"The value `{c}` is not a valid hex code.")
    c = c.lower()
    ones = hex_map[c[1]]
    sixteens = hex_map[c[0]] * 16
    return sixteens + ones


def extract_rgb_from_string(rgb):
    output = []
    if "," in rgb:
        sep = ","
    else:
        sep = " "
    rgb = rgb.split(sep)
    for i in rgb:
        try:
            output.append(i.split("(")[1].strip())
            continue
        except Exception:
            try:
                output.append(i.split(")")[0].strip())
            except Exception:
                output.append(i.strip())
                continue

    return output[0], output[1], output[2]


def is_hex(val):
    result = False
    result = "#" in val and (len(val) == 7 or len(val) == 4 or len(val) == 9)
    if not result:
        return False

    # check for proper hex digits
    for i in val:
        if i != "#" and i.lower() not in list(hex_map.keys()):
            result = False
    return result


def is_rgb(val):
    results = bool(re.match(rgb_all_forms_re, val))
    comma_count = val.count(",")
    results = results and (comma_count == 2 or comma_count == 3)
    return results


def is_hsl(val):
    results = bool(re.match(hsl_all_forms_re, val))
    comma_count = val.count(",")
    results = results and (comma_count == 2 or comma_count == 3)
    return results


def is_color_value(val):
    """ returns True if valid color value """
    if is_hex(val):
        return True
    if is_hsl(val):
        return True
    if is_rgb(val):
        return True
    return False


def get_relative_luminance(val):
    val /= 255
    if val <= 0.03928:
        return val / 12.92
    else:
        return ((val + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = rgb
    r = get_relative_luminance(r)
    g = get_relative_luminance(g)
    b = get_relative_luminance(b)
    return r * 0.2126 + g * 0.7152 + b * 0.0722


def contrast_ratio(hex1, hex2):
    try:
        rgb1 = hex_to_rgb(hex1)
        rgb2 = hex_to_rgb(hex2)
    except ValueError as e:
        print(f"Oops {str(e)}")
        return 0
    l1 = luminance(rgb1)
    l2 = luminance(rgb2)
    # Make sure l1 is the lighter of the two or swap them
    if l1 < l2:
        temp = l1
        l1 = l2
        l2 = temp
    ratio = (l1 + 0.05) / (l2 + 0.05)
    # get the ratio to 2 decimal places without rounding
    # take it to 3rd decimal place, then truncate (3rd has been rounded)
    ratio = format(ratio, ".3f")[:-1]
    return float(ratio)


def get_color_type(code):
    if "#" in code[0]:
        if len(code) > 7:
            return "hex_alpha"
        else:
            return "hex"
    if "hsla" in code[:4]:
        return "hsla"
    if "hsl" in code[:3]:
        return "hsl"
    if "rgba" in code[:4]:
        return "rgba"
    if "rgb" in code[:3]:
        return "rgb"


if __name__ == "__main__":
    hsl = get_hsl_from_string("hsl(355, 96%, 46%)")
    rgb = hsl_to_rgb((355, 96, 46))
    is_it_correct = is_rgb(rgb)
    valid_hex = is_hex("#336699")
    print(valid_hex)
    ratio = contrast_ratio("#336699", "#ffffff")
    print("Contrast ratio between #336699 and #ffffff is: {}".format(ratio))
    get_color_contrast_report("#336699", "#ffffff")
