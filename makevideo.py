import os
import moviepy.video.io.ImageSequenceClip
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

fps = 20

for folder in os.listdir('.'):
    if os.path.isdir(folder) and folder.isdigit():
        image_folder = folder
        image_files = sorted([os.path.join(image_folder, img)
                              for img in os.listdir(image_folder)
                              if img.endswith(".jpg")], key=lambda i: i.split('_')[2])
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(
            image_files, fps=fps)
        clip.write_videofile(image_folder+'.mp4')
