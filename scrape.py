import requests
from bs4 import BeautifulSoup as bs
import os
import tkinter
from PIL import Image, ImageTk
import threading
from time import sleep

TARGET = [
    "4703",
    "4713",
    "2701",
    "2702",
]


def infinite_loop():
    while True:
        try:
            fetch_image()
            sleep(20)
        except:
            sleep(3)
            infinite_loop()


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols*w, i//cols*h))
    return grid


def fetch_image():
    response = requests.get(
        "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/woodlands.html")
    soup = bs(response.text, "lxml")
    images = ["https:"+i['src'] for i in soup.select(".road-snapshots img")]
    imgs = []
    for image in images:
        if not 'nocamera' in image:
            res = requests.get(image)
            folder = image.split("/")[-1].split("_")[0]
            if not os.path.exists(folder):
                os.mkdir(folder)
            file = folder+"/"+os.path.basename(image.split("?")[0])
            with open(file, "wb") as f:
                f.write(res.content)

            imgs.append(Image.open(file))

    grid = image_grid(imgs, rows=2, cols=2)

    updateCanvas(grid)


def updateCanvas(pilImage):
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)

    canvas.imgref = image
    canvas.itemconfig(imagesprite, image=image)


root = tkinter.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()
root.bind("<Escape>", lambda e: root.withdraw())
canvas = tkinter.Canvas(root, width=w, height=h)
canvas.pack()
canvas.configure(background='black')
imagesprite = canvas.create_image(w/2, h/2, image=None)
loop = threading.Thread(target=infinite_loop)
loop.start()
root.mainloop()
