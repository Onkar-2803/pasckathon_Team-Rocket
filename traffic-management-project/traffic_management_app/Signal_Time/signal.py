from object_detection import detection
from density import density
from number_plate import plate
from green_signal_time import green_time

signal_id = 1  #get from database

#take dimensions,signal_id from database

car_count, bike_count, truck_count = detection(signal_id)
final_density = density(car_count, bike_count, truck_count)     #store density in database
final_green = green_time(final_density)                         #pass to frontend
