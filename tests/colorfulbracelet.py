"""
Tracy will draw a beaded bracelet for her birthday.
* There must be 36 beads
* Each bead should have a radius of 10 pixels
* The bracelet must have a diameter of 200
"""
# Declare useful variables to solve the problem
NUMBER_OF_BEADS = 36
BEAD_RADIUS = 10
BRACELET_RADIUS = 100
speed(5)

def draw_bracelet():
    # set the first color
    bead_color = "blue"
    for i in range(NUMBER_OF_BEADS):
        # move out by bracelet radius amount
        move_out(BRACELET_RADIUS)
        
        # draw bead
        draw_bead(BEAD_RADIUS, bead_color)
        
        # change the color
        bead_color = new_bead_color(bead_color)
        
        # return to the center
        return_to_center()
        
        # turn
        turn()

def move_out(distance):
    penup()
    forward(distance)
    pendown()
    
def draw_bead(radius, bead_color):
    # draw a bead of various colors
    color(bead_color)
    begin_fill()
    circle(radius)
    end_fill()
    
def return_to_center():
    penup()
    setposition(0, 0)
    pendown()

def turn():
    # turn to the left by 1 / 36th of a rotation
    amount = int((360 / NUMBER_OF_BEADS))
    #print("Amount of turn is " + str(amount)
    left(amount)
    
def new_bead_color(bead_color):
    # check the color
    # if it was blue, we change to red
    if bead_color == "blue":
        bead_color = "red"
    # if it was red, we change to purple
    elif bead_color == "red":
        bead_color = "purple"
    # otherwise, set it to blue
    else:
        bead_color = "blue"
        
    # return the new color
    return bead_color
    
draw_bracelet()