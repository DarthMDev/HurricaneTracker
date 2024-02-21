import csv
import turtle
import os
import sys
from glob import glob 
from pprint import pprint
# constants
global CATEGORIES_TO_COLORS
global CATEGORIES_TO_WIDTHS
global CATEGORIES_TO_WIND_SPEEDS
CATEGORIES_TO_WIND_SPEEDS = {
    1: range(74, 96),
    2: range(96, 111),
    3: range(111, 131),
    4: range(131, 156),
    5: range(156, 1000)
}
CATEGORIES_TO_COLORS = {
    0: 'white',
    1: 'blue',
    2: 'green',
    3: 'yellow',
    4: 'orange',
    5: 'red'
}
CATEGORIES_TO_WIDTHS = {
    0: 1,
    1: 2,
    2: 3,
    3: 7,
    4: 11,
    5: 15
}


def graphical_setup():
    """Creates the Turtle and the Screen with the map background
       and coordinate system set to match latitude and longitude.

       :return: a tuple containing the Turtle and the Screen

       DO NOT CHANGE THE CODE IN THIS FUNCTION!
    """
    import tkinter
    turtle.setup(965, 600)  # set size of window to size of map

    wn = turtle.Screen()

    # kludge to get the map shown as a background image,
    # since wn.bgpic does not allow you to position the image
    canvas = wn.getcanvas()
    turtle.setworldcoordinates(-90, 0, -17.66, 45)  # set the coordinate system to match lat/long

    map_bg_img = tkinter.PhotoImage(file="images/atlantic-basin.png")

    # additional kludge for positioning the background image
    # when setworldcoordinates is used
    canvas.create_image(-1175, -580, anchor=tkinter.NW, image=map_bg_img)

    t = turtle.Turtle()
    wn.register_shape("images/hurricane.gif")
    t.shape("images/hurricane.gif")

    return t, wn, map_bg_img


def track_storm(filename):
    """Animates the path of the storm.
    """
    (t, wn, map_bg_img) = graphical_setup()

    # your code to animate storm here
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        
        storms = list(reader)



   
    # based on wind data set the category
    for storm in storms:
        for category, winds in CATEGORIES_TO_WIND_SPEEDS.items():
            if int(storm['Wind']) in winds:
                storm['Category'] = category
                break
        else:
            storm['Category'] = 0
    # now animate the storm
    index = 0
    # set the intiail position of the turtle based on the storm longitude and latitude
    t.penup()
    t.speed(0)
    t.setposition(float(storms[index]['Lon']), float(storms[index]['Lat']))
    t.pendown()
    for storm in storms:
       
        # pen down at the start of the storm
        if index == 0:
            t.pendown()
        # stop at the end of the storm

        elif index == len(storms):
            t.penup()
            break
        t.goto(float(storm['Lon']), float(storm['Lat']))
        t.color(CATEGORIES_TO_COLORS[storm['Category']])
        t.width(CATEGORIES_TO_WIDTHS[storm['Category']])
        t.speed(10)
        if storm['Category'] > 0:
            # write it above the storm
            t.write(storm['Category'])
        index += 1

    # without the final call to wn.exitonclick() in main,
    # the background image will not be displayed
    # also need to return map_bg_img so that it is not garbage collected
    return wn, map_bg_img


def main():

    # your code here

    # also you'll need to fix the call below so that it calls
    # the track_storm function
    
    storm_name = input("Enter the name of the storm: ")
    storm_name.lower()
    # each storm has a file with the same name as the storm
    # in the data directory
    if not os.path.exists("data" + os.path.sep + f'{storm_name}.csv'):
        print('Invalid storm name')
        sys.exit(1)
        
    filename = "data" + os.path.sep + storm_name + ".csv"
    

    wn, map_bg_img = track_storm(filename)


    # the line below needs to be the last line of main()
    # you'll need to get the wn from track_storm
    wn.exitonclick()


if __name__ == "__main__":
    main()
