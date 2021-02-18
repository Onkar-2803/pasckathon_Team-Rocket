import time
import pytesseract
from pytesseract import Output
from django.shortcuts import render, redirect, get_object_or_404
import sys
import numpy as np
import cv2
from .models import *
from PIL import Image, ImageDraw
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import datetime
from django.utils import timezone

def home(request):
    return render(request, 'traffic_management_app/index.html')

def about(request):
    return render(request, 'traffic_management_app/about.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'traffic_management_app/login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'traffic_management_app/login.html',{'error': 'Username or password incorrect '})
        else:
            login(request,user)
            return redirect('home')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'traffic_management_app/signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.first_name = request.POST['fname']
                user.last_name = request.POST['lname']
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'traffic_management_app/signup.html',{'error' : 'Username already exists :/'})
        else:
            return render(request, 'traffic_management_app/signup.html',{'error' : 'Passwords do not match '})

def traffic_signal(request):
    return render(request, 'traffic_management_app/sig4.html')
def stolen_vehicle(request):
    if request.method == 'GET':
        detect_plate()
        return render(request, 'traffic_management_app/stolen.html')
    else:
        vehicles = NumPlate.objects.all()

        for i in vehicles:
            print('Checking Number Plate')
            print(i.num_plate)
            if i.num_plate == request.POST['number_plate']:
                print('check')
                sig_id = i.signal_id
                last_seen = i.last_seen
                print('signal id: ',sig_id , '\nLast Seen: ', last_seen)
            else:
                continue
        pass

def shortest_path(request):
    track_path_ans = ''
    if request.method == 'GET':

        return render(request, 'traffic_management_app/path.html',{ 'answer': track_path_ans})
    else:
        print('check')
        print(request.POST.get('id1',False))

        graph={
            'a':{'b':3,'c':4,'d':7},
            'b':{'c':1,'f':5,'a':3},
            'c':{'f':6,'d':2,'a':4,'b':1},
            'd':{'e':3,'g':6,'a':7,'c':2},
            'e':{'g':3,'h':4,'d':3,'f':1},
            'f':{'e':1,'h':8,'b':5,'c':6},
            'g':{'h':2,'d':6,'e':3},
            'h':{'g':2,'e':4,'f':8}
        }

        graph_den={
            'a':{'b':0.46,'c':0.14,'d':0.27},
            'b':{'c':0.86,'f':0.93,'a':0.46},
            'c':{'f':0.64,'d':0.81,'a':0.14,'b':0.86},
            'd':{'e':0.74,'g':0.5,'a':0.27,'c':0.81},
            'e':{'g':0.54,'h':0.46,'d':0.74,'f':0.52},
            'f':{'e':0.52,'h':0.33,'b':0.93,'c':0.64},
            'g':{'h':0.26,'d':0.5,'e':0.54},
            'h':{'g':0.26,'e':0.46,'f':0.33}

        }


        for id1,info in graph_den.items():

            #print("\nroad-id:",id1)

            for key in info:
                #print(key+':',info[key])
                if info[key]>0.75:
                    info[key]=int(info[key]*20)
                elif info[key]>0.30 and info[key]<0.30:
                    info[key]=int(info[key]*15)
                else:
                    info[key]=int(info[key]*10)

                #print(key+':',info[key])

            for id2,info2 in graph.items():
                for key in info:
                    for key1 in info2:
                        if id1==id2:
                            if key==key1:
                                info2[key1]=info2[key1]+info[key]


        def dijsktra(graph,start,goal):
            shortest_distance={}
            track_predecessor={}
            unseenNodes=graph
            infinity=sys.maxsize
            track_path=[]

            for node in unseenNodes:
                shortest_distance[node]=infinity
            shortest_distance[start]=0

            while unseenNodes:
                min_distance=None

                for node in unseenNodes:
                    if min_distance is None:
                        min_distance=node
                    elif shortest_distance[node]<shortest_distance[min_distance]:
                        min_distance=node

                path_options=graph[min_distance].items()

                for child,weight in path_options:
                    if weight+shortest_distance[min_distance]<shortest_distance[child]:
                        shortest_distance[child]=weight+shortest_distance[min_distance]
                        track_predecessor[child]=min_distance

                unseenNodes.pop(min_distance)

            currentNode=goal

            while currentNode!=start:
                try:
                    track_path.insert(0,currentNode)
                    currentNode=track_predecessor[currentNode]

                except KeyError:
                    print("path is not reachable")
                    break
            track_path.insert(0,start)

            if shortest_distance[goal]!=infinity:
                return str(track_path)
        #print(source, dest)

        track_path_ans = dijsktra(graph,request.POST['id1'],request.POST['id2'])
        #print(track_path_ans)
        return render(request, 'traffic_management_app/path.html',{ 'answer': track_path_ans})

def make_next_green(next_signal, time2):
    print('Inside make next green')
    i=next_signal
    prev_time = time2
    if(i.signal_id < 14):
        #signal_L_greentime[i+1] = prev_time
        #signal_L_state[i+1] = "G"

        next_turn = get_object_or_404(Signal, pk=(i.signal_id+1))
        next_turn.left_green_time = prev_time
        next_turn.left_state = True
        print(next_turn.signal_id)
        print('state: ', next_turn.left_state)

        #print("Next Signal Left " + signal_state[i])
    else:
        print('else')
        first_signal = get_object_or_404(Signal, pk=11)
        first_signal.left_green_time = prev_time
        first_signal.left_state = True
        #rint("Next Signal Left " + signal_state[1])

    time.sleep(prev_time)
def detection():
    signals = Signal.objects.filter(signal_id__startswith='1')
    car_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_cars.xml')
    bike_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_bike.xml')
    truck_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/cascade_truck.xml')
    i=1
    car_param1 = [1.2, 1.04, 1.00941, 1.014]
    car_param2 = [(74,74), (0,0), (50,50), (74,74)]

    bike_param1 = [1.04, 1.024, 1.04, 1.024]
    #bike_param2 = [1,2.3.4]

    truck_param1 = [1.05, 1.05, 1.05, 1.05]
    #truck_param2 = [1,2.3.4]
    for signal in signals:
        image_2 = cv2.imread("/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/take" + str(i) +".png",0)
        image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2RGB)
        image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)
        #image = cv2.imread("/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/example.jpg")

        cars_count = car_classifier.detectMultiScale(image_2, car_param1[i-1],minSize=car_param2[i-1])  # , maxSize=(100, 100))
        bike_count = bike_classifier.detectMultiScale(image_2, bike_param1[i-1])
        truck_count = truck_classifier.detectMultiScale(image_2, truck_param1[i-1])
        print(signal.signal_id)
        print('car: ', len(cars_count))
        print('bike: ', len(bike_count))
        print('truck: ', len(truck_count))

        signal.car_count = len(cars_count)
        signal.bike_count = len(bike_count)
        signal.truck_count = len(truck_count)
        i+=1
        car = 6.246
        bike = 1.51
        truck = 20.5#8.5 * 2.5
        #calculate widht manually & length specific, take from database
        length = 15
        width = 9

        density_Num = car*len(cars_count) + bike*len(bike_count) + truck * len(truck_count)
        density_Den = length * width
        density = density_Num/density_Den
        #print(signal.signal_id)
        print('DENSITY: ')
        print(density)
        signal.density = density
        if(density<=0.3):
            signal_green_time=20
        elif(density<=0.6 and density>0.3):
            signal_green_time= 40
        else:
            signal_green_time = 60

        print('TIME: ')
        print(signal_green_time)
        signal.left_green_time = signal.right_green_time = signal.front_green_time = signal_green_time
        signal.save()
    #return signal_green_time
    return redirect('status_of_signals')
def allocate_time():
    signals = Signal.objects.all()

    for i in signals:
        #print(i.signal_id)
        print('Inside main for loop')
        print('Signal Id under consideration: ', i.signal_id)

        prev_time = i.front_green_time
        i.left_state = i.right_state = i.front_state = True

        time1 = i.front_green_time - i.front_green_time/4
        print('Calculated Time: ', time1)
        #timer = Timer(time1, make_next_green(i,prev_time/4))
        #timer.start()
        time.sleep(time1)
        make_next_green(i,prev_time/4)
        i.left_state = i.right_state = i.front_state = False

    print('Function Ends here')

def detect_plate():

    numplate_classifier = cv2.CascadeClassifier('/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/indian_license_plate.xml')
    #image_2 = cv2.imread("/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/example.jpg",0)
    #plates = numplate_classifier.detectMultiScale(grey, 5.99)3
    scale = [2.2,1.6,1.6]
    scale2 = [(74,74),(0,0),(0,0)]
    num_plates = NumPlate.objects.all()
    #print(num_plates)
    for i in range(3):
        image = cv2.imread("/home/batsy/pasckathon_Team-Rocket/traffic-management-project/cascades/num" + str(i+1)+".jpg",0)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image)
        drawing = ImageDraw.Draw(image_pil)
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        plates = numplate_classifier.detectMultiScale(grey, scale[i],minSize=scale2[i])

        for x, y, w, h in plates:
            #print(x,y,w,h)
            #print(len(plates))
            drawing.rectangle((x, y, x + w, y + h), outline='yellow', width=3)
            #image_pil.show()
            cv2.rectangle(grey, (x, y), (x + w, y + h), (255, 0, 158), thickness=3)
            extract = image[y:y + h, x:x + w]
            extract_pil = Image.fromarray(extract)
            #extract_pil.show()
            extract_pil = extract_pil.resize((338, 84))
            text = pytesseract.image_to_string(extract_pil, lang='eng')
            #print(text)

            if '-' in text:
                lst = text.split('-')
                text = ''.join(lst)
            elif ' ' in text:
                lst = text.split()

    #print(lst)

            #print(text)
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
            plate = NumPlate(signal_id=Signal(pk=11),num_plate=r_text,last_seen=timezone.now())
            plate.save()
