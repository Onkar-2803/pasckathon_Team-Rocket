import time
import numpy as np
import cv2

def detection(signal_number):

    car_count=0
    bike_count=0
    truck_count=0

    car_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_car.xml')
    bike_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_bike.xml')
    truck_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_truck.xml')

    cap = cv2.VideoCapture('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/truck.mp4')

    while cap.isOpened():

        time.sleep(.05)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cars = car_classifier.detectMultiScale(gray, 1.15, 6)
        bikes = bike_classifier.detectMultiScale(gray, 1.15, 6)
        trucks = truck_classifier.detectMultiScale(gray, 1.15, 6)

        for (x,y,w,h) in cars:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            car_count += 1
            #cv2.imshow('Cars', frame)
        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break

        for (x,y,w,h) in bikes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            bike_count += 1
            #cv2.imshow('Bikes', frame)
        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break

        for (x,y,w,h) in trucks:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            truck_count += 1
            #cv2.imshow('Trucks', frame)
        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break


    cap.release()
    #cv2.destroyAllWindows()

    #return car_count, bike_count, truck_count
    print( 'Car Count: ',car_count, ' Bike Count: ',bike_count,' Truck count: ' ,truck_count)
