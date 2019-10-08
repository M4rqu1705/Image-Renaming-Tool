#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from PIL import Image, ImageTk

height = 750

# Declare globals to be used later
f_name, f_ext = "", ""
input_label = []
root = ''

def main():
    global input_label, f_name, f_ext, root

    # Image referencing is very frequent, so make sure we're searching inside
    # the image folder
    program_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(f"{program_path}/images")

    for fd in os.listdir('.'):
        f_name, f_ext = os.path.splitext(fd)

        root = tk.Tk()

        # IMAGE
        image = Image.open(f"{f_name}{f_ext}")
        imgWidth, imgHeight = image.size[:2]
        width = imgWidth*height//imgHeight
        image.thumbnail((width, height))
        image = ImageTk.PhotoImage(image=image)
        image_label = tk.Label(root, image=image, height=height, borderwidth=2, relief="solid")

        # INPUT LABEL
        input_label = tk.Entry(root, bd=5, width=50)
        input_label.focus_set()

        # BUTTONS
        ok_button = tk.Button(root, text="Ok", command=renameNext, borderwidth=2, relief="groove")
        cancel_button = tk.Button(root, text="Cancel", command=cancelRenaming, borderwidth=2, relief="groove")
        ok_button.config(bg="green")
        cancel_button.config(bg="red")

        # WINDOW CONFIGURATION
        deltax = (root.winfo_screenwidth() // 2) - (width // 2)
        deltay = (root.winfo_screenheight() // 2) - int(height / 1.85)
        root.geometry(f'{width}x{height+50}+{deltax}+{deltay}')
        root.lift()
        root.attributes("-topmost", True)
        root.title("Image Resizer")

        # BEHAVIOR CONFIGURATION
        root.bind('<Return>', renameNext)
        root.protocol("WM_DELETE_WINDOW", exit)

        # ORDER CONFIGURTION
        image_label.grid(row=0, column=0, columnspan=2)
        input_label.grid(row=1, column=0, sticky='e', padx=20, pady=10)
        ok_button.grid(row=1, column=1, sticky='w', ipadx=10)
        cancel_button.grid(row=1, column=1, sticky='w', ipadx=10, padx=55)

        root.mainloop()


def renameNext(*args):
    global input_label, f_name, f_ext, root
    new_name = input_label.get()
    if '.' not in new_name:
        new_name += f_ext
    os.rename(f"{f_name}{f_ext}", f"{new_name}")

    root.destroy()

def cancelRenaming(*args):
    global root
    root.destroy()


if __name__ == "__main__":
    main()
