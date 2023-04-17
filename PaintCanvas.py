###############################################################
#Description: Simulates a paint canvas
#Date: 4/17/23
###############################################################
#Created referencing nikhilkumarsingh's paint.py on GitHub
from tkinter import *
from tkinter import colorchooser

#Create the main GUI (window, bg color, size)
class Background(Canvas):
    DEFAULT_COLOR = "Black"
    def __init__(self, master):
        Canvas.__init__(self, master)
        self.c = Canvas(self, width = 900, height = 600, bg = "white")
        self.c.pack(side = "top", fill = "both", expand = True)

        #Button for choosing a color
        self.color_button = Button(master, text = "Colors", command = self.choose_color)
        self.color_button.pack(side = "top")

        #Button for erasing
        self.eraser_button = Button(master, text = "Eraser", command = self.erase)
        self.eraser_button.pack(side = "left")

        #Button for clearing all
        self.clear_button = Button(master, text = "Clear", command = self.clear)
        self.clear_button.pack(side = "right")

        self.setup()

    #Clean up before starting and have button detection and a default color
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.c.bind("<B1-Motion>", self.paint)
        self.c.bind("<ButtonRelease-1>", self.reset)

    #Function for erasing
    def erase(self):
        self.color = "white"

    #Function for clearing the screen
    def clear(self):
       self.c.delete('all')

    #Function for choosing a color
    def choose_color(self):
        self.color = colorchooser.askcolor(color = self.color)[1]

    #Function for creating a line
    def paint(self, event):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y, width = 7, fill = self.color, capstyle = ROUND, smooth = TRUE, splinesteps = 36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None



#Run the code when the file is run as a script and include GUI setup
if __name__ == "__main__":
    master = Tk()
    master.title("iPaint")
    message = Label(master, text = "Welcome to iPaint!")
    message.pack(side = BOTTOM)
    view = Background(master)
    view.pack(side = "top", fill = "both", expand = True)
    master.mainloop()