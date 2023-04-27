###############################################################
#Description: Simulates a paint canvas
#Date: 4/27/23
###############################################################
#Created referencing nikhilkumarsingh's paint.py on GitHub
#May have to click with mouse in the beginning to activate pyautogui function
from tkinter import *
from tkinter import colorchooser
import pyautogui
import keyboard
import threading
import queue
import FaceTrack
import Rasp_pi_Data

#Failsafe for if the mouse is rendered inaccessible
pyautogui.FAILSAFE = True

#Create the main GUI (window, bg color, size)
class Background(Canvas):
    DEFAULT_COLOR = "Black"
    def __init__(self, master, q, p, z, mouse_func):
        super(Background, self).__init__(master)
        self.c = Canvas(self, width = 900, height = 600, bg = "white")
        self.c.pack(side = "top", fill = "both", expand = True)
        self.mouse_func = mouse_func
        self.q = q
        self.p = p
        self.z = z

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
        #When the user clicks and drags the mouse, start painting
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

    #Function for creating a line
    def paint(self, event):
        #If something is in the q queue
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

    #Function for using button output to do nothing, click, or drag the mouse
    def auto_draw(self, z):
        #If something is in the z queue
        if z.qsize() > 0:
            #Retrieve and remove it from the queue and process the if statement
            data = z.get()
            if mouse_func == 0:
                pass
            elif mouse_func == 1:
                pyautogui.click(button = "left")
            elif mouse_func == 2:
                pyautogui.mouseDown(button = "left")

#Run the code when the file is run as a script and include GUI setup
if __name__ == "__main__":
    master = Tk()
    master.title("FacePaint")
    message = Label(master, text = "Welcome to FacePaint!")
    message.pack(side = BOTTOM)
    #Instantiate the queues
    q = queue.Queue()
    p = queue.Queue()
    z = queue.Queue()
    #Runs the face tracking program in the background
    face_track_thr = threading.Thread(target = FaceTrack.main, args=(q,))
    #Continuously runs the method auto_draw to check the value of mouse_func
    auto_draw_thr = threading.Thread(target = Background.auto_draw, args = (p,))
    #Continuously receives updated data from the Raspberry pi.
    rasp_data_thr = threading.Thread(target = Rasp_pi_Data.get_rasp_data, args = (z,))
    view = Background(master, q, p, z, mouse_func)
    face_track_thr.start()
    auto_draw_thr.start()
    rasp_data_thr.start()
    view.pack(side = "top", fill = "both", expand = True)
    master.mainloop()

