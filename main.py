import easygui
import numpy as np
import tensorflow as tf
from tkinter import *
from PIL import Image, ImageTk
from gan import gan_function
from enum import Enum

from super_image import ImageLoader, MdsrModel
import os

from diffusion import DIFF_MODELS_CONFIG, DiffImageGeneration

EXAMPLE_PATH = "images/example.jpg"
# if you thik it looks ugly set to False
RESIZE_WITH_AI = True
# you CANNOT change first val, you can change second (but make it a multiple of 256 so resize looks nice) 
IMAGE_DISPLAY_SIZE = (512, 512) if RESIZE_WITH_AI else (256, 256)

class Painters(Enum):
    MONET = 0
    VANGOGH = 1
    UKIYOE = 2
    CEZANNE = 3

class App:
    def __init__(self):
        self.setup_generators()
        self.resizing_model_x2 = MdsrModel.from_pretrained('eugenesiow/mdsr', scale=2)

        self.setup_root()
        self.setup_listbox()
        self.setup_image_first()
        
        self.diff_window = DiffWindow(self.root, self.diff_generation_finished_callback)

    def run(self):
        self.root.mainloop()

    def setup_generators(self):
        self.monet_generator = gan_function(Painters.MONET.value)
        self.vangogh_generator = gan_function(Painters.VANGOGH.value)
        self.ukiyoe_generator = gan_function(Painters.UKIYOE.value)
        self.cezanne_generator = gan_function(Painters.CEZANNE.value)

    def setup_root(self):
        self.root = Tk()
        self.root.title("Create unique images that look like paintings!")  # title of the GUI window
        self.root.maxsize(1200, 1200)  # specify the max size the window can expand to
        self.root.config(bg="skyblue")  # specify background color

        # Create left and right frames
        self.left_frame = Frame(self.root, width=200, height=400, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.right_frame = Frame(self.root, width=650, height=400, bg='grey')
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

        self.bottom_frame = Frame(self.root, width = 880, height=100, bg='grey')
        self.bottom_frame.grid(row=1,columnspan=2, padx=10, pady=5)

        # Create frames and labels in left_frame
        Label(self.left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)
        # Create frames and labels in right_frame
        Label(self.right_frame, text="Result Image").grid(row=0, column=0, padx=5, pady=5)

        Button(self.bottom_frame, text="LOAD IMAGE", command=self.load_image).grid(row=0, column=0, padx=5, pady=5)

        Button(self.bottom_frame, text="GENERATE IMAGE", command=self.on_open_generation_window).grid(row=0, column=1, padx=5, pady=5)

    def setup_listbox(self):
        self.selected_artist = Listbox(self.bottom_frame, height=len(Painters))
        self.selected_artist.grid(row=0, column=2, padx=5, pady=5)
        self.selected_artist.insert(Painters.MONET.value, "Monet")
        self.selected_artist.insert(Painters.VANGOGH.value, "Van Gogh")
        self.selected_artist.insert(Painters.UKIYOE.value, "Ukiyoe")
        self.selected_artist.insert(Painters.CEZANNE.value, "Cezanne")
        self.selected_artist.selection_set(0)
        self.selected_artist.bind("<<ListboxSelect>>", lambda event: self.selected_artist_changed())

    def setup_image_first(self):
        image = Image.open(EXAMPLE_PATH)
        image = self.resize_image(image)

        self.label_original = Label(self.left_frame, image=image)
        self.label_original.image = image
        self.label_original = self.label_original.grid(row=1, column=0, padx=5, pady=5)

        self.first_image_generate(EXAMPLE_PATH)

    def first_image_generate(self, PATH):
        img_to_generate_painting = tf.io.read_file(PATH)
        img_to_generate_painting = self.preprocess_image(img_to_generate_painting)
        self.original_img = img_to_generate_painting
        self.generate_picture(img_to_generate_painting)

    def generate_picture(self, img, is_generated_diff=False):
        selected_index = self.selected_artist.curselection()
        if selected_index:
            index = selected_index[0]
            if index == 0:
                prediction = self.monet_generator(img, training=False)[0].numpy()

            elif index == 1:
                prediction = self.vangogh_generator(img, training=False)[0].numpy()

            elif index == 2:
                prediction = self.ukiyoe_generator(img, training=False)[0].numpy()

            elif index == 3:
                prediction = self.cezanne_generator(img, training=False)[0].numpy()

        else:
            prediction = self.monet_generator(img, training=False)[0].numpy()

        prediction = (prediction * 127.5 + 127.5).astype(np.uint8)
        generated_img = Image.fromarray(prediction)
        generated_img = self.resize_image(generated_img, is_generated_diff)

        self.label_generated = Label(self.right_frame, image=generated_img)
        self.label_generated.image = generated_img
        self.label_generated.grid(row=1, column=0, padx=5, pady=5)

    def preprocess_image(self, img):
        img = tf.io.decode_image(img)
        img_rows, img_cols, channel = 256, 256, 3
        return tf.reshape(tf.cast(tf.image.resize(img, (int(img_rows), int(img_cols))), tf.float32) / 127.5 - 1,
                        (1, img_rows, img_cols, channel))

    def selected_artist_changed(self):
        self.generate_picture(self.original_img)

    def on_open_generation_window(self):
        self.diff_window.open()

    def resize_image(self, image, is_generated_diff=False):
        if RESIZE_WITH_AI and is_generated_diff:
            inputs = ImageLoader.load_image(image)
            preds = self.resizing_model_x2(inputs)

            image_filename = 'res.png'
            ImageLoader.save_image(preds, image_filename)

            image = Image.open(image_filename)
            os.remove(image_filename)
        else:
            image = image.resize(IMAGE_DISPLAY_SIZE)

        return ImageTk.PhotoImage(image)

    def diff_generation_finished_callback(self, image):
        inputs = ImageLoader.load_image(image)
        preds = self.resizing_model_x2(inputs)

        image_filename = 'temp.png'
        ImageLoader.save_image(preds, image_filename)

        image = Image.open(image_filename)
        image = self.resize_image(image, True)

        self.label_original = Label(self.left_frame, image=image)
        self.label_original.image = image
        self.label_original = self.label_original.grid(row=1, column=0, padx=5, pady=5)

        img_to_generate_painting = tf.io.read_file(image_filename)
        img_to_generate_painting = self.preprocess_image(img_to_generate_painting)
        self.original_img = img_to_generate_painting
        self.generate_picture(img_to_generate_painting, True)

        os.remove(image_filename)
    

    def load_image(self):
        filename = easygui.fileopenbox(filetypes=["*.png", "*.jpg"]) # need to change so that they are both in one tab and
                            # so that only files of these types can be selected (still better than GIFs, so its improvement)
        image = Image.open(filename)
        image = self.resize_image(image)

        self.label_original = Label(self.left_frame, image=image)
        self.label_original.image = image
        self.label_original = self.label_original.grid(row=1, column=0, padx=5, pady=5)

        img_to_generate_painting = tf.io.read_file(filename)
        img_to_generate_painting = self.preprocess_image(img_to_generate_painting)
        self.original_img = img_to_generate_painting
        self.generate_picture(img_to_generate_painting)

class DiffWindow:
    def __init__(self, master, generation_finished_callback):
        self.master = master
        self.diff_image_generator = DiffImageGeneration()
        self.diff_image_generator.set_callbacks(self.step_callback, self.finished_callback)
        self.master_callback = generation_finished_callback

    def open(self):
        self.diff_window = Toplevel(self.master)
        self.diff_window.title('Generate an image using diffusion')
        Label(self.diff_window, text='Generate an image using diffusion')
        self.setup_listbox()
        self.setup_button()
        self.setup_label()
        

    def setup_listbox(self):
        self.listbox = Listbox(self.diff_window, height=len(DIFF_MODELS_CONFIG))
        for index, model_name in enumerate(DIFF_MODELS_CONFIG):
            self.listbox.insert(index, model_name)
        
        self.listbox.selection_set(0)
        self.listbox.bind("<<ListboxSelect>>", lambda event: self.on_selection_changed())
        self.listbox.pack(side=LEFT)

    def setup_button(self):
        button = Button(self.diff_window, text="GENERATE", command=self.on_generate_clicked)
        button.pack(side=RIGHT)

    def on_selection_changed(self):
        self.diff_image_generator.switch_active_model(self.listbox.curselection()[0])
    
    def setup_label(self):
        self.label = Label(self.diff_window, text='Status: not doing anything')
        self.label.pack(side=TOP)

    def step_callback(self, iter, max_iter):
        self.label.config(text=f'Status: {(iter / max_iter * 100):.2f}%')
        self.label.update_idletasks()
    
    def finished_callback(self, image):
        self.diff_window.destroy()
        self.master_callback(image)

    def on_generate_clicked(self):
        self.diff_image_generator.generate_image()


if __name__ == '__main__':
    app = App()
    app.run()
