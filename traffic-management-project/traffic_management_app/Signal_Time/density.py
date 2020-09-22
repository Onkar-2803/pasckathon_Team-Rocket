def density(count_car, count_bike, count_truck):

    #areas of respective vehicles
    car = 40
    bike = 10
    truck = 80
    #calculate widht manually & length specific, take from database
    length = 100
    width = 60
    car_count = count_car
    bike_count = count_bike
    truck_count = count_truck

    density_Num = car*car_count + bike*bike_count + truck * truck_count
    density_Den = length * width
    density = density_Num/density_Den

    return density
