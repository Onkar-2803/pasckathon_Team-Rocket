import cv2 as cv
from PIL import Image, ImageDraw
import numpy
import os
import pytesseract
# import tesseract
from pytesseract import Output


img = cv.imread('D:/Traffic Project/Number Plates/d3.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
number_cascade = cv.CascadeClassifier('D:/Traffic Project/Cascades/indian_license_plate.xml')

"""
nm14 image sathi (2.2, minSize(60,13)

d3 ani download image sathi 1.6   #minSize nahie tyala

"""




temp = 'MH12DE1433'

image_pil = Image.fromarray(img)
drawing = ImageDraw.Draw(image_pil)
grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
plates = number_cascade.detectMultiScale(grey, 1.6)#,minSize=(136,13))
for x, y, w, h in plates:
    #print(x,y,w,h)
    #print(len(plates))
    drawing.rectangle((x, y, x + w, y + h), outline='yellow', width=3)
    image_pil.show()
    cv.rectangle(grey, (x, y), (x + w, y + h), (255, 0, 158), thickness=3)
    extract = img[y:y + h, x:x + w]
    extract_pil = Image.fromarray(extract)
    #extract_pil.show()
    extract_pil = extract_pil.resize((338, 84))
    text = pytesseract.image_to_string(extract_pil, lang='eng')
    print(text)
    if '-' in text:
        lst = text.split('-')
        text = ''.join(lst)
    elif ' ' in text:
        lst = text.split()

    #print(lst)

    print(text)
    r_text = ''
    if not text[0].isalpha():
        i=0
        while not text[i].isalpha():
            i+=1
        i+=1
        while text[i-1].isalnum() and i<len(text):
            #print("HERE")
            r_text += text[i-1]
            i+=1
    else:
        i=0
        while text[i].isalnum() and i<len(text)+1:
            r_text += text[i]
            i+=1
    print(r_text)
    if r_text == temp:
        print("Thief Found!!")

