from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import easygui

def loadImage():
    global my_img 
    global my_label
    
    filename = easygui.fileopenbox()
    my_img = ImageTk.PhotoImage(Image.open(filename))

    my_label.grid_forget()
    my_label = Label(image=my_img)
    my_label.grid(row=0, column=0, columnspan=2)


root = Tk()
root.title('WTUM Image Viewer')

my_img = ImageTk.PhotoImage(Image.open("images/sheep.jpg"))

my_label = Label(image=my_img)
my_label.grid(row=0,column=0,columnspan=2)

button_back = Button(root, text="LOAD IMAGE", command = loadImage)
button_exit = Button(root, text="EXIT PROGRAM", command=root.quit)

button_back.grid(row=1, column=0)
button_exit.grid(row=1,column=1)


root.mainloop()