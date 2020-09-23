import PIL
import os
import os.path
from PIL import Image

f = r'D:/dataset_hackathon/number_plate_train/p'
for file in os.listdir(f):
    f_img = f+"/"+file
    img = Image.open(f_img)
    img = img.resize((100,100))
    img.save(f_img)
