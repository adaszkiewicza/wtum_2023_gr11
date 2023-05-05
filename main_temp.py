from tkinter import *
from PIL import Image, ImageTk
import easygui
from gan import gan_function
import numpy as np
import tensorflow as tf

def load_image():
    global image 
    global left_frame
    global root
    global label1
    global label2
    global original_img
    global original_img_resized
    
    filename = easygui.fileopenbox(filetypes=["*.gif"])
    imaget = Image.open(filename)
    imaget = imaget.resize((400,400))
    image = ImageTk.PhotoImage(imaget)
    original_img_resized = image
    label1 = Label(left_frame, image=image).grid(row=1, column=0, padx=5, pady=5)

    generated_img = image
    img = tf.io.read_file(filename)
    img = preprocess_image(img)
    original_img = img
    generate_picture(img, image)


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
img = Image.open("images/wow.gif")
imaget = img.resize((400,400))

image = ImageTk.PhotoImage(imaget)
label1 = Label(left_frame, image=image).grid(row=1, column=0, padx=5, pady=5)
label2 = Label(right_frame, image=image).grid(row=1,column=0, padx=5, pady=5)

Button(bottom_frame, text="LOAD IMAGE", command=load_image).grid(row=0, column=0, padx=5, pady=5)
Checkbutton(bottom_frame, text='Is generated from noise', onvalue=1, offvalue=0).grid(row=0,column=1,padx=5,pady=5)
selected_artist = Listbox(bottom_frame, height=3)
selected_artist.grid(row=0, column=2, padx=5, pady=5)
selected_artist.insert(0, "Monet")
selected_artist.insert(1, "Van Gogh")
selected_artist.insert(2, "Ukiyoe")
selected_artist.selection_set(0)
selected_artist.bind("<<ListboxSelect>>", lambda event: selected_artist_changed())
Button(bottom_frame, text="EXIT APPLICATION", command=root.quit).grid(row=0, column=3, padx=5, pady=5)

######
monet_generator = gan_function(0)
vangogh_generator = gan_function(1)
ukiyoe_generator = gan_function(2)

def preprocess_image(img):
    # img = tf.io.read_file(img_path)
    img = tf.io.decode_image(img)
    img_rows,img_cols,channel = 256,256,3
    return tf.reshape(tf.cast(tf.image.resize(img,(int(img_rows),int(img_cols))),tf.float32) / 127.5 - 1,(1,img_rows,img_cols,channel))

def generate_picture(img, image):
    selected_index = selected_artist.curselection()
    if selected_index:
        index = selected_index[0]
        if index == 0:
            prediction = monet_generator(img, training=False)[0].numpy()
            prediction = (prediction * 127.5 + 127.5).astype(np.uint8)

        elif index == 1:
            prediction = vangogh_generator(img, training=False)[0].numpy()
            prediction = (prediction * 127.5 + 127.5).astype(np.uint8)

        elif index == 2:
            prediction = ukiyoe_generator(img, training=False)[0].numpy()
            prediction = (prediction * 127.5 + 127.5).astype(np.uint8)

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
    generate_picture(original_img, original_img_resized)
# Load your model

# Preprocess your image
# img = tf.io.read_file("images/8-bit City_1920x1080.jpg")
# img = preprocess_image(img)

# # Generate the Monet-esque version of your image
# prediction = monet_generator(img, training=False)[0].numpy()
# prediction = (prediction * 127.5 + 127.5).astype(np.uint8)
#
# # Plot the original and generated images
# fig, ax = plt.subplots(1, 2, figsize=(12, 6))
# ax[0].imshow((img[0] * 127.5 + 127.5).numpy().astype(np.uint8))
# ax[1].imshow(prediction)
# ax[0].set_title("Input Photo")
# ax[1].set_title("Monet-esque")
# ax[0].axis("off")
# ax[1].axis("off")
# plt.show()

# Generate the Monet-esque version of your image
# prediction = monet_generator(img, training=False)[0].numpy()
# monet_esque = (prediction * 127.5 + 127.5).astype(np.uint8)



root.mainloop()