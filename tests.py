import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
import sys
import os


def next_image(self):
    global image_paths, index, root, widgets

    if index < len(image_paths) - 1:
        index += 1
    else:
        index = 0

    img_path = image_paths[index]
    image_name = img_path.split('/')[-1]

    image = ImageTk.PhotoImage(image=process_image(img_path, widgets["image_label"].winfo_height()))
    widgets["image_label"].config(image=image)
    widgets["image_label"].image = image
    widgets["image_name_label"].config(text=f'Image Name\n{image_name}')


def previous_image(self):
    global image_paths, index, root, widgets

    if 0 < index:
        index -= 1
    else:
        index = len(image_paths)-1

    img_path = image_paths[index]
    image_name = img_path.split('/')[-1]

    image = ImageTk.PhotoImage(image=process_image(img_path, widgets["image_label"].winfo_height()))
    widgets["image_label"].config(image=image)
    widgets["image_label"].image = image
    widgets["image_name_label"].config(text=f'Image Name\n{image_name}')


def perform_renaming(self):
    global image_paths, index, widgets

    new_name = widgets['entry_label'].get().strip()
    old_name = widgets['image_name_label']['text'].split('\n')[-1]
    f_name, f_ext = old_name.split('.')

    if '.' not in new_name:
        new_name += "." + f_ext

    if new_name not in image_paths:
        os.rename(f"{old_name}", f"{new_name}")
        image_paths = os.listdir('.')

        # Shortcuts to 'refresh' window
        image_paths = sorted(image_paths)
        index = image_paths.index(new_name)
        next_image(); previous_image(); cancel_renaming()
    else:
        sys.stderr.write(f"COULD NOT RENAME IMAGE! {new_name} is already in use")


def cancel_renaming(self):
    global widgets

    widgets['entry_label'].delete(0,len(widgets['entry_label'].get()))
    widgets['entry_label'].insert(0,' ')
    widgets['entry_label'].focus_set()


def file_dialog(self):
    global image_paths, widgets
    folder = tkinter.filedialog.askdirectory(
            initialdir='..',
            title='Where did you locate your images?'
            )
    widgets['current_directory_label']['text'] = folder
    os.chdir(folder)

    image_paths = os.listdir('.')
    print(image_paths)
    image_paths = sorted(image_paths)


def process_image(img_path, desired_size):
    # Pre-process data ready for edge cases
    try:
        desired_size = int(desired_size)
    except e:
        sys.stderr.write("Desired height is not an integer")

    img_path = str(img_path)
    while str(img_path).count('\\') > 0:
        img_path.replace('\\', '/')
    if not os.path.isfile(img_path):
        sys.stderr.write(f"Provided image file path '{img_path}' does not exist. Try fixing it")
        return Image.new("RGB", (desired_size, desired_size))

    # Get and process image
    image = Image.open(img_path)
    old_size = image.size
    # Size ratio only takes into account largest dimension.
    size_ratio = float(desired_size)/max(old_size)
    new_size = (old_size[0]*size_ratio, old_size[1]*size_ratio)
    # Actually resize image in place
    image.thumbnail(new_size, Image.ANTIALIAS)
    # Create new black square
    new_image = Image.new("RGB", (desired_size, desired_size))
    # Paste resized image into black square
    new_image.paste(image, (int(desired_size-new_size[0])//2, int(desired_size-new_size[1])//2))

    return new_image


def main():
    global image_paths, index, root, widgets

    root.state('zoomed')
    root.title("image renaming tool".title())

    # BEHAVIOR CONFIGURATION
    root.bind('<Return>', perform_renaming)
    root.bind('<Escape>', cancel_renaming)
    root.bind('<Left>', previous_image)
    root.bind('<Right>', next_image)
    root.bind('<Control-o>', file_dialog)

    max_width, max_height = root.maxsize()
    desired_size = int(max_height*5/6)

    # IMAGE
    img_path = image_paths[index]
    image_name = img_path.split('/')[-1]

    image = ImageTk.PhotoImage(image=process_image(img_path, desired_size))
    image_label = tk.Label(
            root,
            image=image,
            height=desired_size,
            borderwidth=2,
            relief="solid")

    # IMAGE NAME LABEL
    label_width = max_width//3
    image_name_label = tk.Label(
            root,
            text=f'Image Name\n{image_name}',
            font=("Verdana", 16),
            justify="center")

    # NEW NAME ENTRY
    entry_label = tk.Entry(
            root,
            font=("Verdana", 14),
            justify="left",
            borderwidth=3,
            relief="solid"
            )
    entry_label.focus_set()
    entry_label.insert(0," ")

    # CURRENT DIRECTORY LABEL
    current_directory_label = tk.Label(
            root,
            text=os.getcwd(),
            font=("Verdana", 16),
            justify="left",
            background="white",
            borderwidth=2,
            relief="solid",
            wraplength=(max_width*20)//80
            )

    # BUTTONS
    ok_button = tk.Button(
            root,
            text = "Ok",
            font=("Verdana", 14),
            justify="left",
            command = perform_renaming,
            borderwidth = 2,
            relief = "groove",
            background = "green")

    cancel_button = tk.Button(root,
            text = "Cancel",
            font=("Verdana", 14),
            justify="left",
            command = cancel_renaming,
            borderwidth = 2,
            relief = "groove",
            background = "red")

    previous_image_button = tk.Button(root,
            text = "<",
            font=("Verdana", 14),
            justify="center",
            command = previous_image,
            borderwidth = 2,
            relief = "groove",
            background = "gray")

    next_image_button = tk.Button(root,
            text = ">",
            font=("Verdana", 14),
            justify="center",
            command = next_image,
            borderwidth = 2,
            relief = "groove",
            background = "gray")

    folder_open_button = tk.Button(root,
            text = "Open Folder",
            font=("Verdana", 14),
            justify="center",
            command = file_dialog,
            borderwidth = 2,
            relief = "groove",
            background = "gray")

    # Global `widgets` dictionary to manipulate content later
    widgets = {
            "image_label":image_label,
            "image_name_label":image_name_label,
            "entry_label":entry_label,
            "current_directory_label":current_directory_label,
            "ok_button":ok_button,
            "cancel_button":cancel_button,
            "previous_image_button":previous_image_button,
            "next_image_button":next_image_button,
            "folder_open_button":folder_open_button
            }

    # POSITIONING
    image_label.place(
            x = (max_height-desired_size)//6,
            y = (max_height-desired_size)//3,
            height = desired_size,
            width = desired_size)

    image_name_label.place(
            x = (max_width*47//80),
            y = (max_height-desired_size)*5//6,
            width = label_width)

    entry_label.place(
            x = (max_width*47//80),
            y = (max_height-desired_size)*8//6,
            width = label_width)

    current_directory_label.place(
            x = (max_width*54)//80,
            y = (max_height*8)//10,
            width = (max_width*20)//80
            )

    ok_button.place(
            x = (max_width*57//80),
            y = (max_height-desired_size)*10//6
            )

    cancel_button.place(
            x = (max_width*60//80),
            y = (max_height-desired_size)*10//6
            )

    previous_image_button.place(
            x = (max_width*6)//80,
            y = (max_height*9)//10
            )

    next_image_button.place(
            x = (max_width*32)//80,
            y = (max_height*9)//10
            )

    folder_open_button.place(
            x = (max_width*47)//80,
            y = (max_height*8)//10
            )


    root.mainloop()


if __name__ == "__main__":
    global image_paths, index, root, widgets

    # Declare and initialize globals for later use
    os.chdir('./images')
    image_paths = os.listdir('.')
    index = 0
    root = tk.Tk()
    widgets = dict()

    main()
