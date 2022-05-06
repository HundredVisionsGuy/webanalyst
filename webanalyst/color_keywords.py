# color_keywords.py
# a set of variables and functions to process color keywords and their
# hexadecimal values

basic_color_keywords = {
    "black": "#000000",
    "silverk": "#C0C0C0",
    "grayk": "#808080",
    "whitek": "#FFFFFF",
    "maroon": "#800000",
    "red": "#FF0000",
    "purple": "#800080",
    "fuchsia": "#FF00FF",
    "green": "#008000",
    "lime": "#00FF00",
    "olive": "#808000",
    "yellow": "#FFFF00",
    "navy": "#000080",
    "blue": "#0000FF",
    "teal": "#008080",
    "aqua": "#00FFFF",
}

extended_color_keywords = [
    "aliceblue	#F0F8FF	rgb(240, 248, 255)	Shades",
    "antiquewhite	#FAEBD7	rgb(250, 235, 215)	Shades",
    "aqua	#00FFFF	rgb(0, 255, 255)	Shades",
    "aquamarine	#7FFFD4	rgb(127, 255, 212)	Shades",
    "azure	#F0FFFF	rgb(1240, 255, 255)	Shades",
    "beige	#F5F5DC	rgb(245, 245, 220)	Shades",
    "bisque	#FFE4C4	rgb(255, 228, 196)	Shades",
    "black	#000000	rgb(0, 0, 0)	Shades",
    "blanchedalmond	#FFEBCD	rgb(255, 235, 205)	Shades",
    "blue	#0000FF	rgb(0, 0, 255)	Shades",
    "blueviolet	#8A2BE2	rgb(138, 43, 226)	Shades",
    "brown	#A52A2A	rgb(165, 42, 42)	Shades",
    "burlywood	#DEB887	rgb(222, 184, 135)	Shades",
    "cadetblue	#5F9EA0	rgb(95, 158, 160)	Shades",
    "chartreuse	#7FFF00	rgb(95, 158, 160)	Shades",
    "chocolate	#D2691E	rgb(210, 105, 30)	Shades",
    "coral	#FF7F50	rgb(255, 127, 80)	Shades",
    "cornflowerblue	#6495ED	rgb(100, 149, 237)	Shades",
    "cornsilk	#FFF8DC	rgb(255, 248, 220)	Shades",
    "crimson	#DC143C	rgb(220, 20, 60)	Shades",
    "cyan	#00FFFF	rgb(0, 255, 255)	Shades",
    "darkblue	#00008B	rgb(0, 0, 139)	Shades",
    "darkcyan	#008B8B	rgb(0, 139, 139)	Shades",
    "darkgoldenrod	#B8860B	rgb(184, 134, 11)	Shades",
    "darkgray	#A9A9A9	rgb(169, 169, 169)	Shades",
    "darkgreen	#006400	rgb(0, 100, 0)	Shades",
    "darkkhaki	#BDB76B	rgb(189, 183, 107)	Shades",
    "darkmagenta	#8B008B	rgb(139, 0, 139)	Shades",
    "darkolivegreen	#556B2F	rgb(85, 107, 47)	Shades",
    "darkorange	#FF8C00	rgb(255, 140, 0)	Shades",
    "darkorchid	#9932CC	rgb(153, 50, 204)	Shades",
    "darkred	#8B0000	rgb(139, 0, 0)	Shades",
    "darksalmon	#E9967A	rgb(233, 150, 122)	Shades",
    "darkseagreen	#8FBC8F	rgb(143, 188, 143)	Shades",
    "darkslateblue	#483D8B	rgb(72, 61, 139)	Shades",
    "darkslategray	#2F4F4F	rgb(47, 79, 79)	Shades",
    "darkturquoise	#00CED1	rgb(0, 206, 209)	Shades",
    "darkviolet	#9400D3	rgb(148, 0, 211)	Shades",
    "deeppink	#FF1493	rgb(255, 20, 147)	Shades",
    "deepskyblue	#00BFFF	rgb(0, 191, 255)	Shades",
    "dimgray	#696969	rgb(0, 191, 255)	Shades",
    "dodgerblue	#1E90FF	rgb(30, 144, 255)	Shades",
    "firebrick	#B22222	rgb(178, 34, 34)	Shades",
    "floralwhite	#FFFAF0	rgb(255, 250, 240)	Shades",
    "forestgreen	#228B22	rgb(34, 139, 34)	Shades",
    "fuchsia	#FF00FF	rgb(255, 0, 255)	Shades",
    "gainsboro	#DCDCDC	rgb(220, 220, 220)	Shades",
    "ghostwhite	#F8F8FF	rgb(248, 248, 255)	Shades",
    "gold	#FFD700	rgb(255, 215, 0)	Shades",
    "goldenrod	#DAA520	rgb(218, 165, 32)	Shades",
    "gray	#7F7F7F	rgb(127, 127, 127)	Shades",
    "green	#008000	rgb(0, 128, 0)	Shades",
    "greenyellow	#ADFF2F	rgb(173, 255, 47)	Shades",
    "honeydew	#F0FFF0	rgb(240, 255, 240)	Shades",
    "hotpink	#FF69B4	rgb(255, 105, 180)	Shades",
    "indianred	#CD5C5C	rgb(205, 92, 92)	Shades",
    "indigo	#4B0082	rgb(75, 0, 130)	Shades",
    "ivory	#FFFFF0	rgb(255, 255, 240)	Shades",
    "khaki	#F0E68C	rgb(240, 230, 140)	Shades",
    "lavender	#E6E6FA	rgb(230, 230, 250)	Shades",
    "lavenderblush	#FFF0F5	rgb(255, 240, 245)	Shades",
    "lawngreen	#7CFC00	rgb(124, 252, 0)	Shades",
    "lemonchiffon	#FFFACD	rgb(255, 250, 205)	Shades",
    "lightblue	#ADD8E6	rgb(173, 216, 230)	Shades",
    "lightcoral	#F08080	rgb(240, 128, 128)	Shades",
    "lightcyan	#E0FFFF	rgb(224, 255, 255)	Shades",
    "lightgoldenrodyellow	#FAFAD2	rgb(250, 250, 210)	Shades",
    "lightgreen	#90EE90	rgb(144, 238, 144)	Shades",
    "lightgrey	#D3D3D3	rgb(211, 211, 211)	Shades",
    "lightpink	#FFB6C1	rgb(255, 182, 193)	Shades",
    "lightsalmon	#FFA07A	rgb(255, 160, 122)	Shades",
    "lightseagreen	#20B2AA	rgb(32, 178, 170)	Shades",
    "lightskyblue	#87CEFA	rgb(135, 206, 250)	Shades",
    "lightslategray	#778899	rgb(119, 136, 153)	Shades",
    "lightsteelblue	#B0C4DE	rgb(176, 196, 222)	Shades",
    "lightyellow	#FFFFE0	rgb(255, 255, 224)	Shades",
    "lime	#00FF00	rgb(0, 255, 0)	Shades",
    "limegreen	#32CD32	rgb(50, 205, 50)	Shades",
    "linen	#FAF0E6	rgb(250, 240, 230)	Shades",
    "magenta	#FF00FF	rgb(255, 0, 255)	Shades",
    "maroon	#800000	rgb(128, 0, 0)	Shades",
    "mediumaquamarine	#66CDAA	rgb(102, 205, 170)	Shades",
    "mediumblue	#0000CD	rgb(0, 0, 205)	Shades",
    "mediumorchid	#BA55D3	rgb(186, 85, 211)	Shades",
    "mediumpurple	#9370DB	rgb(147, 112, 219)	Shades",
    "mediumseagreen	#3CB371	rgb(60, 179, 113)	Shades",
    "mediumslateblue	#7B68EE	rgb(123, 104, 238)	Shades",
    "mediumspringgreen	#00FA9A	rgb(0, 250, 154)	Shades",
    "mediumturquoise	#48D1CC	rgb(72, 209, 204)	Shades",
    "mediumvioletred	#C71585	rgb(199, 21, 133)	Shades",
    "midnightblue	#191970	rgb(25, 25, 112)	Shades",
    "mintcream	#F5FFFA	rgb(245, 255, 250)	Shades",
    "mistyrose	#FFE4E1	rgb(255, 228, 225)	Shades",
    "moccasin	#FFE4B5	rgb(255, 228, 181)	Shades",
    "navajowhite	#FFDEAD	rgb(255, 222, 173)	Shades",
    "navy	#000080	rgb(0, 0, 128)	Shades",
    "navyblue	#9FAFDF	rgb(159, 175, 223)	Shades",
    "oldlace	#FDF5E6	rgb(253, 245, 230)	Shades",
    "olive	#808000	rgb(128, 128, 0)	Shades",
    "olivedrab	#6B8E23	rgb(107, 142, 35)	Shades",
    "orange	#FFA500	rgb(255, 165, 0)	Shades",
    "orangered	#FF4500	rgb(255, 69, 0)	Shades",
    "orchid	#DA70D6	rgb(218, 112, 214)	Shades",
    "palegoldenrod	#EEE8AA	rgb(238, 232, 170)	Shades",
    "palegreen	#98FB98	rgb(152, 251, 152)	Shades",
    "paleturquoise	#AFEEEE	rgb(175, 238, 238)	Shades",
    "palevioletred	#DB7093	rgb(219, 112, 147)	Shades",
    "papayawhip	#FFEFD5	rgb(255, 239, 213)	Shades",
    "peachpuff	#FFDAB9	rgb(255, 218, 185)	Shades",
    "peru	#CD853F	rgb(205, 133, 63)	Shades",
    "pink	#FFC0CB	rgb(255, 192, 203)	Shades",
    "plum	#DDA0DD	rgb(221, 160, 221)	Shades",
    "powderblue	#B0E0E6	rgb(176, 224, 230)	Shades",
    "purple	#800080	rgb(128, 0, 128)	Shades",
    "red	#FF0000	rgb(255, 0, 0)	Shades",
    "rosybrown	#BC8F8F	rgb(188, 143, 143)	Shades",
    "royalblue	#4169E1	rgb(65, 105, 225)	Shades",
    "saddlebrown	#8B4513	rgb(139, 69, 19)	Shades",
    "salmon	#FA8072	rgb(250, 128, 114)	Shades",
    "sandybrown	#FA8072	rgb(244, 164, 96)	Shades",
    "seagreen	#2E8B57	rgb(46, 139, 87)	Shades",
    "seashell	#FFF5EE	rgb(255, 245, 238)	Shades",
    "sienna	#A0522D	rgb(160, 82, 45)	Shades",
    "silver	#C0C0C0	rgb(192, 192, 192)	Shades",
    "skyblue	#87CEEB	rgb(135, 206, 235)	Shades",
    "slateblue	#6A5ACD	rgb(106, 90, 205)	Shades",
    "slategray	#708090	rgb(112, 128, 144)	Shades",
    "snow	#FFFAFA	rgb(255, 250, 250)	Shades",
    "springgreen	#00FF7F	rgb(0, 255, 127)	Shades",
    "steelblue	#4682B4	rgb(70, 130, 180)	Shades",
    "tan	#D2B48C	rgb(210, 180, 140)	Shades",
    "teal	#008080	rgb(0, 128, 128)	Shades",
    "thistle	#D8BFD8	rgb(216, 191, 216)	Shades",
    "tomato	#FF6347	rgb(255, 99, 71)	Shades",
    "turquoise	#40E0D0	rgb(64, 224, 208)	Shades",
    "violet	#EE82EE	rgb(238, 130, 238)	Shades",
    "wheat	#F5DEB3	rgb(245, 222, 179)	Shades",
    "white	#FFFFFF	rgb(255, 255, 255)	Shades",
    "whitesmoke	#F5F5F5	rgb(245, 245, 245)	Shades",
    "yellow	#FFFF00	rgb(255, 255, 0)	Shades",
    "yellowgreen	#9ACD32	rgb(139, 205, 50)	Shades",
]


def get_basic_color_keywords():
    return basic_color_keywords


def get_full_color_keywords():
    """returns a dictionary of all color keywords with their hex value"""
    color_keywords = basic_color_keywords
    for i in extended_color_keywords:
        items = i.split("\t")
        key = items[0]
        val = items[1]
        color_keywords[key] = val
    return color_keywords


def get_all_keywords():
    keywords = list(get_full_color_keywords().keys())
    return keywords


def is_a_keyword(word):
    return word in get_all_keywords()


def get_hex_by_keyword(word):
    keywords = get_full_color_keywords()
    hex = keywords.get(word)
    return hex


if __name__ == "__main__":
    # keywords = get_full_color_keywords()
    print(get_hex_by_keyword("beige"))
