import os
from PIL import Image, ImageDraw, ImageFont
import datetime

font = ImageFont.truetype("JBM.ttf", 20)

# filter out corrupted images
for folder in os.listdir('.'):
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if os.path.getsize(os.path.join(folder, file)) < 20000:
                os.remove(os.path.join(folder, file))
                print('Deleted', file)

# filter out duplicate images
for folder in os.listdir('.'):
    if os.path.isdir(folder):
        files = {}
        for file in os.listdir(folder):
            _, time, date, *_ = file.split('_')
            date = date[:8]

            if '_'.join([date, time]) in files:
                files['_'.join([date, time])].append(file)
            else:
                files['_'.join([date, time])] = [file]

        for key, value in files.items():
            if len(value) > 1:
                compares = [(os.path.getsize(os.path.join(folder, file)), file)
                            for file in value]
                max_size = max(compares)[0]
                [os.remove(os.path.join(folder, file))
                 for size, file in compares if size != max_size]

# add timestamp to images
for folder in os.listdir('.'):
    if os.path.isdir(folder) and folder.isdigit():
        for file in os.listdir(folder):
            if not file.startswith("."):
                try:
                    _, time, date, *_ = file.split('_')
                    date = date[:8]
                    hour, minute = int(time[:2]), int(time[2:4])
                    year, month, date = int(date[:4]), int(
                        date[4:6]), int(date[6:])
                    time = datetime.datetime(year, month, date, hour, minute)
                    im = Image.open(os.path.join(folder, file))
                    draw = ImageDraw.Draw(im)
                    draw.text((im.width-250, im.height-50), datetime.datetime.strftime(
                        time, "%Y-%m-%d %H:%M"), (255, 255, 255), font=font)
                    im.save(os.path.join(folder, file))
                    print(file)
                except:
                    os.remove(os.path.join(folder, file))

# remove hidden files
for folder in os.listdir('.'):
    if os.path.isdir(folder) and folder.isdigit():
        for file in os.listdir(folder):
            if file.startswith("."):
                os.remove(os.path.join(folder, file))
