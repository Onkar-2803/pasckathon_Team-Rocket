from django.shortcuts import render
import time
import numpy as np
import cv2
from .models import *
from django.shortcuts import render, redirect, get_object_or_404

def status_of_signals(request):
    #signals = get_object_or_404()
    signals = Signal.objects.all()
    return render(request, 'traffic_management_app/home.html', {'signals' : signals})

def detection(request, Signal_pk):

    #car_count=0
    #bike_count=0
    #truck_count=0

    car_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_car.xml')
    bike_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_bike.xml')
    truck_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_truck.xml')

    image_2 = cv2.imread("/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/example.jpg",0)

    image = cv2.imread("/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/example.jpg")

    #car_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_car.xml')
    cars_count = car_classifier.detectMultiScale(image_2, 1.0485258, 6)
    bike_count = bike_classifier.detectMultiScale(image_2, 1.0485258, 6)
    truck_count = truck_classifier.detectMultiScale(image_2, 1.0485258, 6)

    """
    for (x,y,w,h) in cars:
        cv2.rectangle(image, (x,y), (x+w,y+h), (127,0,255), 2)
        cv2.imshow('car Detection', image)

    for (x,y,w,h) in bike:
        cv2.rectangle(image, (x,y), (x+w,y+h), (127,0,255), 2)
        #cv2.imshow('car Detection', image)

    for (x,y,w,h) in truck:
        cv2.rectangle(image, (x,y), (x+w,y+h), (127,0,255), 2)
        #cv2.imshow('car Detection', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        """
    print('Cars:')
    print(len(cars_count))

    print('Bike:')
    print(len(bike_count))

    print('Truck:')
    print(len(truck_count))
    
    signal = get_object_or_404(Signal, pk=Signal_pk)
    signal.car_count = len(cars_count)
    signal.bike_count = len(bike_count)
    signal.truck_count = len(truck_count)
    signal.save()

    car = 40
    bike = 10
    truck = 80
    #calculate widht manually & length specific, take from database
    length = 1000
    width = 400

    density_Num = car*len(cars_count) + bike*len(bike_count) + truck * len(truck_count)
    density_Den = length * width
    density = density_Num/density_Den

    print('DENSITY: ')
    print(density)
    if(density<=0.3):
        signal_green_time=20
    elif(final_density<=0.6 & final_density>0.3):
        signal_green_time= 40
    else:
        signal_green_time = 60

    print('TIME: ')
    print(signal_green_time)
    #return signal_green_time
