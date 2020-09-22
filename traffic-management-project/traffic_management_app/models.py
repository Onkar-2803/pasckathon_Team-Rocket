from django.db import models

# Create your models here.
class Chowk(models.Model):
    chowk_id = models.AutoField(primary_key=True)
    chowk_name = models.CharField(max_length=50)

    def __str__(self):
        return self.chowk_name

class Signal(models.Model):
    signal_id = models.CharField(max_length=2, primary_key=True)
    chowk = models.ForeignKey(Chowk, on_delete=models.CASCADE)

    left_state = models.BooleanField(default=False)
    right_state = models.BooleanField(default=False)
    front_state = models.BooleanField(default=False)

    car_count = models.PositiveSmallIntegerField(blank=True, default=0)
    bike_count = models.PositiveSmallIntegerField(blank=True, default=0)
    truck_count = models.PositiveSmallIntegerField(blank=True, default=0)

    def __str__(self):
        return self.signal_id

class Density(models.Model):
    signal_id = models.ForeignKey(Signal, on_delete=models.CASCADE)
    density = models.DecimalField(max_digits=1, decimal_places=1, blank=True)

    def __str__(self):
        return self.signal_id
