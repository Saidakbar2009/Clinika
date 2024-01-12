from django.db import models
from rigistr.models import *

# Create your models here.
class Xona(models.Model):
    qavat = models.CharField(max_length=30)
    raqam = models.PositiveIntegerField()
    sigim = models.PositiveIntegerField(default=0)
    tur = models.CharField(max_length=30)
    narx = models.PositiveIntegerField()
    bosh_joy_soni = models.PositiveIntegerField()

class Joylashtirish(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE)
    xona = models.ForeignKey(Xona, on_delete=models.CASCADE)
    izoh = models.CharField(max_length=500)
    kelgan_sana = models.DateField()
    ketish_sana = models.DateField()
    yotgan_kuni = models.DateField()
    bosh_joy = models.IntegerField()
    qarovchi = models.BooleanField(default=False)

