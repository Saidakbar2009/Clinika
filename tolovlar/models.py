from django.db import models
from rigistr.models import *
from xonalar.models import *
# Create your models here.
class Tolov(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE)
    yollanma = models.ForeignKey(Yollanma, on_delete=models.CASCADE, null=True)
    joylashtirhs = models.ForeignKey(Joylashtirish, on_delete=models.CASCADE, null=True)
    summa = models.IntegerField()
    tolangan_summa = models.IntegerField()
    tolandi = models.BooleanField()
    created_sana = models.DateField()
    tolangan_sana = models.DateField()
    turi = models.CharField(max_length=20)
    izoh = models.TextField(blank=True)