import cv2
from os import listdir,makedirs
from os.path import isfile,join

i=1
path = r'D:/dataset_hackathon/car_train/to_be_renamed' # Source Folder
dstpath = r'D:/dataset_hackathon/car_train/p' # Destination Folder
#D:\dataset_hackathon\Datasets_car_truck

files = [f for f in listdir(path) if isfile(join(path,f))]

for image in files:
    img = cv2.imread(path + "/" + str(image))


    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    dstPath = join(dstpath,image)
    #cv2.imwrite(dstPath,gray)
    #cv2.imshow("check", img)

    #cv2.imshow("check", img)
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    cv2.imwrite(dstpath +'/' + 'car_new_2' + str(i) +".jpg",img)
    i+=1
