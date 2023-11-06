import math
import tkinter

import PIL
import extcolors
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from matplotlib import gridspec

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure


def study_image(image_path):
    img = fetch_image(image_path)
    colors = extract_colors(img)
    color_palette = render_color_platte(colors)
    overlay_palette(img, color_palette)


def fetch_image(image_path):
    urllib.request.urlretrieve(image_path, "image")
    img = PIL.Image.open("image")
    return img


def extract_colors(img):
    tolerance = 32
    limit = 24
    colors, pixel_count = extcolors.extract_from_image(img, tolerance, limit)
    return colors


def render_color_platte(colors):
    size = 100
    columns = 6
    width = int(min(len(colors), columns) * size)
    height = int((math.floor(len(colors) / columns) + 1) * size)
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(result)
    for idx, color in enumerate(colors):
        x = int((idx % columns) * size)
        y = int(math.floor(idx / columns) * size)
        canvas.rectangle([(x, y), (x + size - 1, y + size - 1)], fill=color[0])
    return result


def overlay_palette(img, color_palette):
    nrow = 2
    ncol = 1
    f = plt.figure(figsize=(10, 10), facecolor='None', edgecolor='k', dpi=55, num=None)
    gs = gridspec.GridSpec(nrow, ncol, wspace=0.0, hspace=0.0)
    f.add_subplot(2, 1, 1)
    plt.imshow(img, interpolation='nearest')
    plt.axis('off')
    f.add_subplot(1, 2, 2)
    plt.imshow(color_palette, interpolation='nearest')
    plt.axis('off')
    plt.subplots_adjust(wspace=0, hspace=0, bottom=0)
    plt.show(block=True)
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")

    canvas = FigureCanvasTkAgg(f, master=root)  # A tk.DrawingArea.
    canvas.draw()
    # pack_toolbar=False will make it easier to use a layout manager later on.
    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()
    canvas.mpl_connect(
        "key_press_event", lambda event: print(f"you pressed {event.key}"))
    canvas.mpl_connect("key_press_event", key_press_handler)

    button_quit = tkinter.Button(master=root, text="Quit", command=root.destroy)

    # Packing order is important. Widgets are processed sequentially and if there
    # is no space left, because the window is too small, they are not displayed.
    # The canvas is rather flexible in its size, so we pack it last which makes
    # sure the UI controls are displayed as long as possible.
    button_quit.pack(side=tkinter.BOTTOM)
    toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    tkinter.mainloop()


image_url = 'https://tinyurl.com/unsplash-painted-flowers'
study_image(image_url)
