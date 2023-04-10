from tkinter import *
from PIL import Image, ImageTk
import easygui

def load_image():
    global image 
    global left_frame
    global root
    global label1
    global label2
    
    filename = easygui.fileopenbox(filetypes=["*.gif"])
    imaget = Image.open(filename)
    imaget = imaget.resize((400,400))
    image = ImageTk.PhotoImage(imaget)
    label1 = Label(left_frame, image=image).grid(row=1, column=0, padx=5, pady=5)
    label2 = Label(right_frame, image=image).grid(row=1,column=0, padx=5, pady=5)

root = Tk()  # create root window
root.title("Basic GUI Layout")  # title of the GUI window
root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color

# Create left and right frames
left_frame = Frame(root, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = Frame(root, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)

bottom_frame = Frame(root, width = 880, height=100, bg='grey')
bottom_frame.grid(row=1,columnspan=2, padx=10, pady=5)

# Create frames and labels in left_frame
Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)
# Create frames and labels in left_frame
Label(right_frame, text="Result Image").grid(row=0, column=0, padx=5, pady=5)

# load image to be "edited"
imaget = Image.open("images/wow.gif")
imaget = imaget.resize((400,400))

image = ImageTk.PhotoImage(imaget)
label1 = Label(left_frame, image=image).grid(row=1, column=0, padx=5, pady=5)
label2 = Label(right_frame, image=image).grid(row=1,column=0, padx=5, pady=5)

Button(bottom_frame, text="LOAD IMAGE", command=load_image).grid(row=0, column=0, padx=5, pady=5)
Checkbutton(bottom_frame, text='Is generated from noise', onvalue=1, offvalue=0).grid(row=0,column=1,padx=5,pady=5)
w = Listbox(bottom_frame, height=3)
w.grid(row=0,column=2,padx=5,pady=5)
w.insert(1, "Jan Matejko")
w.insert(2, "Da Vinci")
w.insert(3, "Van Gogh")
Button(bottom_frame, text="EXIT APPLICATION", command=root.quit).grid(row=0, column=3, padx=5, pady=5)

root.mainloop()