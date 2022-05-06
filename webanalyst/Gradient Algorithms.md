Gradient Algorithms

Check to see if gradient is in the value (for color or bg-color) and get the lowest contrast score of all the scores

If it is...
    SET contrast score to 100
    GET all colors listed in the gradient
    FOR each color
        GET new contrast score
        IF new contrast score is less than contrast score
            SET contrast score to new contrast score

    return contrast score

RGBA / Hexwith Alpha Algorithm
Challenge: we need to know what is the background color of its context
    Default would be white
    How do we know the context?
    We would need the element and all ancestors

IF rgba in color OR it's a hex and there are 9 total characters
    GET opposite color

Some Regex Possibilities
(?<!-moz-)radial-gradient|(?<!-ms-)radial-gradient|(?<!-webkit-)radial-gradient
(?<!-moz-)radial-gradient => will only grab radial-gradient if -moz- does NOT precede it (still grabs radial-gradient from other vendor prefixes)
