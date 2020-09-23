from django.db import models

# Create your models here.
class Chowk(models.Model):
    chowk_id = models.AutoField(primary_key=True)
    chowk_name = models.CharField(max_length=50)

    def __str__(self):
        return self.chowk_name

class Signal(models.Model):
    #signal_id = models.CharField(max_length=2, primary_key=True)
    signal_id = models.PositiveSmallIntegerField(primary_key=True)
    chowk = models.ForeignKey(Chowk, on_delete=models.CASCADE)

    left_state = models.BooleanField(default=False)
    right_state = models.BooleanField(default=False)
    front_state = models.BooleanField(default=False)

    car_count = models.PositiveSmallIntegerField(blank=True, default=0)
    bike_count = models.PositiveSmallIntegerField(blank=True, default=0)
    truck_count = models.PositiveSmallIntegerField(blank=True, default=0)

    density = models.DecimalField(max_digits=4, decimal_places=4, blank=True,default=0.0)

    left_green_time = models.PositiveSmallIntegerField(blank=True, default=0)
    right_green_time = models.PositiveSmallIntegerField(blank=True, default=0)
    front_green_time = models.PositiveSmallIntegerField(blank=True, default=0)

class NumPlate(models.Model):
    signal_id = models.ForeignKey(Signal, on_delete=models.CASCADE)
    num_plate = models.CharField(max_length=10, blank=True)
    last_seen = models.DateTimeField(auto_now=True,blank=True)
