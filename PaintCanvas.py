###############################################################
#Description: Simulates a paint canvas
#Date: 4/20/23
###############################################################
#Created referencing nikhilkumarsingh's paint.py on GitHub
from tkinter import *
from tkinter import colorchooser
import EyeTrack
import threading
import queue
from sys import exit

#Create the main GUI (window, bg color, size)
class Background(Canvas):
    DEFAULT_COLOR = "Black"
    def __init__(self, master, q):
        super(Background, self).__init__(master)
        self.c = Canvas(self, width = 900, height = 600, bg = "white")
        self.c.pack(side = "top", fill = "both", expand = True)
        #Define q
        self.q = q
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

    #Clean up before starting, have button detection, and a default color
    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        #When the user presses the left mouse button and moves across the screen, call the paint function
        self.c.bind("<B1-Motion>", self.paint)
        #When the user releases the button, stop painting
        self.c.bind("<ButtonRelease-1>", self.reset)

    #Function for erasing
    def erase(self):
        self.color = "white"

    #Function for clearing the screen
    def clear(self):
       self.c.delete('all')

    #Function for choosing a color using a color wheel
    def choose_color(self):
        self.color = colorchooser.askcolor(color = self.color)[1]

    #Function for cqreating a line
    def paint(self, event):
        #If something is in the queue
        if q.qsize() > 0:
            #Retrieve and remove it from the queue and process the if statement
            data = q.get()
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y, width = 7, fill = self.color, capstyle = ROUND, smooth = TRUE, splinesteps = 36)
            self.old_x = event.x
            self.old_y = event.y

    #Stop painting
    def reset(self, event):
        self.old_x, self.old_y = None, None

#Run the code when the file is run as a script and include GUI setup
if __name__ == "__main__":
    master = Tk()
    master.title("FacePaint")
    message = Label(master, text = "Welcome to FacePaint!")
    message.pack(side = BOTTOM)
    #Create a new instance of the Queue class from the queue module
    q = queue.Queue()
    #Identify the target data as cx and xy in EyeTrack
    background_thr = threading.Thread(target = EyeTrack.main, args = (q,))
    view = Background(master, q)
    view.pack(side = "top", fill = "both", expand = True)
    #EyeTrack.main()
    #EyeTrack.cv2.destroyAllWindows()
    #Start the thread
    background_thr.start()
    master.mainloop()
    exit()
