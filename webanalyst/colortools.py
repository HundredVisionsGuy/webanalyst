"""Main module."""
hex_map = {"0": 0,
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
           "f": 15}

def rgb_to_hex(*args):
    # are there three separate values or 1 string
    if len(args) == 3:
        r, g, b = args
    else:
        try:
            rgb = args[0]
            r, g, b = extract_rgb_from_string(rgb)
        except:
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
    """ receives hex (str) -> returns rgb as tuple """
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

def rgb_as_string(rgb):
    """ receive rgb as tuple -> returns formatted string """
    r, g, b = rgb
    return f"rgb({r},{g},{b})"

def hex_to_decimal(c):
    # make sure to convert to lower case
    # so FF becomes ff
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
        except:
            try:
                output.append(i.split(")")[0].strip())
            except:
                output.append(i.strip())
                continue

    return output[0], output[1], output[2]

def is_hex(val):
    result = False
    result = "#" in val and (len(val) == 7 or len(val) == 4)
    if not result:
        return False
    
    #check for proper hex digits
    for i in val:
        if i != "#" and i not in list(hex_map.keys()):
            result = False
    return result

def get_relative_luminance(val):
    val /= 255
    if val <= 0.03928:
        return val / 12.92
    else:
        return ((val + 0.055) / 1.055)**2.4
              
def luminance(rgb):
    r, g, b = rgb
    r = get_relative_luminance(r)
    g = get_relative_luminance(g)
    b = get_relative_luminance(b)
    return r * 0.2126 + g * 0.7152 + b * 0.0722
    
def contrast_ratio(hex1, hex2):
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
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

if __name__ == "__main__":
    valid_hex = is_hex("#336699")
    print(valid_hex)