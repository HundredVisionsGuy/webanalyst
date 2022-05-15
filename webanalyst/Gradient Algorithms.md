Gradient Algorithms

Check to see if gradient is in the value (for color or bg-color) and get contrast score for the lightest and darkest values of bg and foreground colors

If it is...
    GET lightest and darkest value in the colors for text
    GET lightest and darkest value in the bg colors
    GET contrast for each combination (L to D, L to L, D to D, D to L)
    SORT the contrast values
    return the lowest contrast score

RGBA / Hexwith Alpha Algorithm
Challenge: we need to know what is the background color of its context
    Default would be white
    How do we know the context?
    We would need the element and all ancestors

Possible Algorithm
    GET DOM tree of Body - we need a simplified tree
        only need elements (name, id, class, and maybe dict of details, such as color, bg color)
    GET all color rulesets
    FROM color rulesets 
        GET selectors (type, class, id, parent)
    FROM selectors
        Create a dictionary of elements, their IDs and Classes
    FOREACH element in DOM

Notes: {
    For alpha, we need element's color or bg color, and all containers with a color or bg color
}

IF rgba in color OR it's a hex and there are 9 total characters
    GET opposite color

Some Regex Possibilities
(?<!-moz-)radial-gradient|(?<!-ms-)radial-gradient|(?<!-webkit-)radial-gradient
(?<!-moz-)radial-gradient => will only grab radial-gradient if -moz- does NOT precede it (still grabs radial-gradient from other vendor prefixes)
