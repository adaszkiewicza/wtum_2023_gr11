from tkinter import *
from PIL import Image, ImageTk
import easygui
from gan import gan_function
import numpy as np
import tensorflow as tf

MONET = 0
VANGOGH = 1
UKIYOE = 2
EXAMPLE_PATH = "images/example.jpg"

def preprocess_image(img):
    img = tf.io.decode_image(img)
    img_rows, img_cols, channel = 256, 256, 3
    return tf.reshape(tf.cast(tf.image.resize(img, (int(img_rows), int(img_cols))), tf.float32) / 127.5 - 1,
                      (1, img_rows, img_cols, channel))

def generate_picture(img):
    selected_index = selected_artist.curselection()
    if selected_index:
        index = selected_index[0]
        if index == 0:
            prediction = monet_generator(img, training=False)[0].numpy()

        elif index == 1:
            prediction = vangogh_generator(img, training=False)[0].numpy()

        elif index == 2:
            prediction = ukiyoe_generator(img, training=False)[0].numpy()

    else:
        prediction = monet_generator(img, training=False)[0].numpy()

    prediction = (prediction * 127.5 + 127.5).astype(np.uint8)
    generated_img = Image.fromarray(prediction)
    generated_img = generated_img.resize((400, 400))
    generated_img = ImageTk.PhotoImage(generated_img)

    label2 = Label(right_frame, image=generated_img)
    label2.image = generated_img
    label2.grid(row=1, column=0, padx=5, pady=5)

def selected_artist_changed():
    generate_picture(original_img)

def load_image():
    global image
    global left_frame
    global root
    global label1
    global label2
    global original_img
    
    filename = easygui.fileopenbox(filetypes=["*.gif"])
    image = Image.open(filename)
    image = image.resize((400, 400))
    image = ImageTk.PhotoImage(image)
    label1 = Label(left_frame, image=image).grid(row=1, column=0, padx=5, pady=5)

    img_to_generate_painting = tf.io.read_file(filename)
    img_to_generate_painting = preprocess_image(img_to_generate_painting)
    original_img = img_to_generate_painting
    generate_picture(img_to_generate_painting)

def first_image_generate(PATH):
    global original_img
    img_to_generate_painting = tf.io.read_file(PATH)
    img_to_generate_painting = preprocess_image(img_to_generate_painting)
    original_img = img_to_generate_painting
    generate_picture(img_to_generate_painting)

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
# Create frames and labels in right_frame
Label(right_frame, text="Result Image").grid(row=0, column=0, padx=5, pady=5)

Button(bottom_frame, text="LOAD IMAGE", command=load_image).grid(row=0, column=0, padx=5, pady=5)
Checkbutton(bottom_frame, text='Is generated from noise', onvalue=1, offvalue=0).grid(row=0, column=1, padx=5, pady=5)
selected_artist = Listbox(bottom_frame, height=3)
selected_artist.grid(row=0, column=2, padx=5, pady=5)
selected_artist.insert(0, "Monet")
selected_artist.insert(1, "Van Gogh")
selected_artist.insert(2, "Ukiyoe")
selected_artist.selection_set(0)
selected_artist.bind("<<ListboxSelect>>", lambda event: selected_artist_changed())

monet_generator = gan_function(MONET)
vangogh_generator = gan_function(VANGOGH)
ukiyoe_generator = gan_function(UKIYOE)

# load image to be "edited"
image = Image.open(EXAMPLE_PATH)
image = image.resize((400, 400))
image = ImageTk.PhotoImage(image)
label1 = Label(left_frame, image=image).grid(row=1, column=0, padx=5, pady=5)
first_image_generate(EXAMPLE_PATH)

root.mainloop()
