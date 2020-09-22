import cv2
from os import listdir,makedirs
from os.path import isfile,join

i=1
path = r'D:/dataset_hackathon/number_plate_train/p' # Source Folder
dstpath = r'D:/dataset_hackathon/number_plate_train/p1/' # Destination Folder

try:
    makedirs(dstpath)
except:
    print ("Directory already exist, images will be written in asme folder")

# Folder won't used
files = [f for f in listdir(path) if isfile(join(path,f))]

for image in files:
    try:
        print(image)
        #img = cv2.imread(os.path.join(path,image))
        img = cv2.imread(path + "/" + str(image))

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        dstPath = join(dstpath,image)
        #cv2.imwrite(dstPath,gray)
        #cv2.imshow("check", img)

        #cv2.imshow("check", img)
        #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        cv2.imwrite(dstpath + 'grey'+str(i) +".jpg",gray)
        i+=1
    except:
        #print ("{} is not converted".format(image))
        pass
"""
img = cv2.imread('D:/dataset_hackathon/kahi/badshah.jpg')
#cv2.imshow("check", img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

cv2.imwrite('D:/dataset_hackathon/kahi'  +"/positive_car.jpg",gray)
"""
