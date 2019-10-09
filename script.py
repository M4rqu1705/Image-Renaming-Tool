import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
import sys
import os


def next_image(*args):
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
    widgets["image_name_label"].config(text=image_name)


def previous_image(*args):
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
    widgets["image_name_label"].config(text=image_name)


def perform_renaming(*args):
    global image_paths, index, widgets

    new_name = widgets['entry_label'].get().strip()
    old_name = widgets['image_name_label']['text'].split('\n')[-1]
    f_name, f_ext = old_name.split('.')

    if '.' not in new_name:
        try:
            if '.' not in [new_name[-4], new_name[-3]]:
                new_name += "." + f_ext
        except:
            new_name += "." + f_ext

    if new_name not in image_paths and all(char not in ['<','>',':','"','/','\\','|','?','*'] for char in new_name):
        os.rename(f"{old_name}", f"{new_name}")
        widgets['history_label']['text'] += f"\n[>>] Renamed '{old_name}' to '{new_name}'"

        image_index = image_paths.index(old_name)
        image_paths[image_index] = new_name
        #  image_paths = os.listdir('.')

        # Shortcuts to 'refresh' window
        index = image_paths.index(new_name)
        next_image(); previous_image(); cancel_renaming()
    else:
        sys.stderr.write(f"COULD NOT RENAME IMAGE! '{new_name}' is already in use")
        widgets['history_label']['text'] += f"\n[!!] Could not rename image!  '{new_name}' is already in use or invalid character used"


def cancel_renaming(*args):
    global widgets

    widgets['entry_label'].delete(0,len(widgets['entry_label'].get()))
    widgets['entry_label'].insert(0,' ')
    widgets['entry_label'].focus_set()


def folder_dialog(*args):
    global root, image_paths, widgets
    folder = tkinter.filedialog.askdirectory(initialdir='..', title='Where did you locate your images?')
    if folder.strip() not in ["", None]:
        temp = "/".join(folder.split('/')[-2:])
        widgets['current_directory_label']['text'] = temp
        widgets['history_label']['text'] += f"\n[>>] Moved to new folder '{temp}'"
        os.chdir(folder)


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
        return Image.new("HEX", (desired_size, desired_size), "#7C0A02")

    # Get and process image
    image = Image.open(img_path)
    old_size = image.size
    # Size ratio only takes into account largest dimension.
    size_ratio = float(desired_size)/max(old_size)
    new_size = (old_size[0]*size_ratio, old_size[1]*size_ratio)
    # Actually resize image in place
    image.thumbnail(new_size, Image.ANTIALIAS)
    # Create new black square
    new_image = Image.new("RGB", (desired_size, desired_size), "#7C0A02")
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
    root.bind('<Control-o>', folder_dialog)

    max_width, max_height = root.maxsize()
    print(max_width, ",", max_height)
    desired_size = max_height

    # DECORATIVE FRAMES
    image_background = tk.Frame(root, background="#7C0A02")
    left_frame = tk.Frame(root, background="#B22222")
    right_frame = tk.Frame(root, background="#E25822")
    control_panel_background = tk.Frame(root, background="#F1BC31")

    # IMAGE
    img_path = image_paths[index]
    image_name = img_path.split('/')[-1]

    image = ImageTk.PhotoImage(image=process_image(img_path, desired_size))
    image_label = tk.Label(root, image=image)

    # LABELS
    label_width = max_width//3
    image_name_label = tk.Label(
            root,
            text=image_name,
            font=("Verdana", 20),
            justify="left",
            background="#FFFFFF")
    current_directory_label = tk.Label(
            root,
            text="/".join(os.getcwd().split('\\')),
            font=("Verdana", 18),
            justify="left",
            background="#FFFFFF",
            borderwidth=2,
            relief="solid",
            wraplength=max_width*0.240234)
    history_label = tk.Label(
            root,
            text="",
            font=("Verdana", 18),
            justify="left",
            background="#FFFFFF",
            borderwidth=2,
            relief="solid",
            wraplength=max_width*0.301432,
            anchor='s'
            )

    # ENTRY
    entry_label = tk.Entry(
            root,
            font=("Verdana", 20),
            justify="left",
            borderwidth=3,
            relief="solid")
    entry_label.focus_set()
    entry_label.insert(0," ")


    # BUTTONS
    ok_button = tk.Button(
            root,
            text = "Ok",
            font=("Verdana", 18),
            justify="left",
            command = perform_renaming,
            borderwidth = 2,
            relief = "groove",
            background = "#39D521")
    cancel_button = tk.Button(root,
            text = "Cancel",
            font=("Verdana", 18),
            justify="left",
            command = cancel_renaming,
            borderwidth = 2,
            relief = "groove",
            background = "#B22222")
    previous_image_button = tk.Button(root,
            text = "<",
            font=("Verdana", 18),
            justify="center",
            command = previous_image,
            borderwidth = 2,
            relief = "groove",
            background = "#E25822")
    next_image_button = tk.Button(root,
            text = ">",
            font=("Verdana", 18),
            justify="center",
            command = next_image,
            borderwidth = 2,
            relief = "groove",
            background = "#E25822")
    folder_open_button = tk.Button(root,
            text = "Browse",
            font=("Verdana", 18),
            justify="center",
            command = folder_dialog,
            borderwidth = 2,
            relief = "groove",
            background = "#E25822")

    # Global `widgets` dictionary to manipulate content later
    widgets = {
            "image_background":image_background,
            "left_frame":left_frame,
            "right_frame":right_frame,
            "control_panel_background":control_panel_background,
            "image_label":image_label,
            "image_name_label":image_name_label,
            "history_label":history_label,
            "entry_label":entry_label,
            "current_directory_label":current_directory_label,
            "ok_button":ok_button,
            "cancel_button":cancel_button,
            "previous_image_button":previous_image_button,
            "next_image_button":next_image_button,
            "folder_open_button":folder_open_button
            }

    # POSITIONING
    # max_height = 864, max_width = 1536

    left_frame.place(
            x = max_width*0.5625,
            y = 0,
            width = max_width*0.03125,
            height = max_height*1)

    right_frame.place(
            x = max_width*0.59375,
            y = 0,
            width = max_width*0.03125,
            height = max_height*1)

    control_panel_background.place(
            x = max_width*0.625,
            y = 0,
            width = max_width*0.375,
            height = max_height)

    image_label.place(
            x = 0,
            y = 0,
            width = desired_size,
            height = desired_size)

    image_name_label.place(
            x = max_width*0.661458,
            y = max_height*0.074074,
            width = max_width*0.278646,
            height = max_height*0.055556)

    history_label.place(
            x = max_width*0.653646,
            y = max_height*0.33912,
            width = max_width*0.301432,
            height = max_height*0.16088)

    entry_label.place(
            x = max_width*0.653646,
            y = max_height*0.143519,
            width = max_width*0.301432,
            height = max_height*0.074074)

    previous_image_button.place(
            x = max_width*0.653646,
            y = max_height*0.231481,
            width = max_width*0.041667,
            height = max_height*0.075231)

    next_image_button.place(
            x = max_width*0.913411,
            y = max_height*0.231481,
            width = max_width*0.041667,
            height = max_height*0.075231)

    ok_button.place(
            x = max_width*0.716146,
            y = max_height*0.231481,
            width = max_width*0.067057,
            height = max_height*0.074074)

    cancel_button.place(
            x = max_width*0.797526,
            y = max_height*0.231481,
            width = max_width*0.095052,
            height = max_height*0.074074)

    current_directory_label.place(
            x = max_width*0.714844,
            y = max_height*0.873843,
            width = max_width*0.240234,
            height = max_height*0.074653)

    folder_open_button.place(
            x = max_width*0.640625,
            y = max_height*0.873843,
            width = max_width*0.074219,
            height = max_height*0.049769)


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
