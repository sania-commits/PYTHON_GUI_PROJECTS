from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
root.title("Wallpaper Viewer")
root.geometry("300x450")
root.configure(background='black')

text_label = Label(root,text='Wallpaper Viewer App',fg="white",bg="black")
text_label.pack(pady=(10,20))
text_label.config(font=('verdana',11))
# Path setup:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "wallpaper_viewer")
# Load images:
img_array = []

files = [
    file for file in os.listdir(IMG_DIR)
    if file.lower().endswith((".jpg",".jpeg",".png"))
]

for file in files:
    img_path = os.path.join(IMG_DIR, file)

    img = Image.open(img_path)
    img = img.resize((200, 300))

    photo = ImageTk.PhotoImage(img)
    img_array.append(photo)

# Current image index:
current = 0

# Image label:
image_label = Label(root,bg="black")
image_label.pack()
image_label.config(image=img_array[current])

def show_next():
    global current
    current += 1
    if current >= len(img_array):
        current = 0

    image_label.config(image=img_array[current])

def show_previous():
    global current
    current -= 1
    if current < 0:
        current = len(img_array) - 1

    image_label.config(image = img_array[current])

# Button frame:
button_frame = Frame(root, bg="black")
button_frame.pack(pady=10)

prev_btn = Button(button_frame, text="Previous", command=show_next)
prev_btn.pack(side="left", padx=10)

next_btn = Button(button_frame, text="Next", command=show_previous)
next_btn.pack(side="right", padx=10)

root.mainloop()