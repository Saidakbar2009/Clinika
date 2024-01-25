from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rigistr.models import *
from tolovlar.models import *
from .models import *
from .serializers import *
from datetime import datetime
# Create your views here.

class XonaAPIView(APIView):
    def get(self, request):
        xonalar = Xona.objects.all()
        qarovchi = request.query_params.get("qarovchi")
        if qarovchi == 'true':
            xonalar = xonalar.filter(bosh_joy__gt=1)
        elif qarovchi == 'false':
            xonalar = xonalar.filter(bosh_joy__gt=0)
        serializer = XonaSerializer(xonalar, many=True)
        return Response(serializer.data)

class JoylashtrishAPIView(APIView):
    def get(self, request):
        joylashtirishlar = Joylashtrish.objects.order_by('-id')
        holat = request.query_params.get("holat")
        if holat == "ketgan":
            joylashtirishlar = joylashtirishlar.filter(ketish_sana__isnull=False)
        elif holat == 'ketmagan':
            joylashtirishlar = joylashtirishlar.filter(ketish_sana__isnull=True)
        serializer = JoylashtirishSerializer(joylashtirishlar, many=True)
        return Response(serializer.data)
    @transaction.atomic
    def post(self, request):
        data = request.data
        serializer = JoylashtirishSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            bemor = Bemor.objects.get(id=data.bemor.id)
            bemor.data = True
            bemor.save()
            xona = Xona.objects.get(id=data)
            if data.qarovchi == True:
                xona.data -= 2
            else:
                xona.data -= 1
            xona.save()
            Tolov.objects.create(
                bermor = bemor,
                joylashtirish = data,
                summa = 0
            )
            return Response(serializer.data)
        return Response(serializer.errors)

class JoylashtirishAPIView(APIView):
    @transaction.atomic
    def update(self, request, pk):
        joylashtirsh = Joylashtirish.objects.get(id=pk)
        serializer = JoylashtirishSerializer(joylashtirsh, data=request.data)
        if serializer.is_valid():
            serializer.save()
            bemor = Bemor.objects.get(id=request.data.bemor.id)
            bemor.data = False
            bemor.save()
            xona = Xona.objects.get(id=request.data)
            if request.data.qarovchi == True:
                xona.data += 2
            else:
                xona.data += 1
            xona.save()
            tolov = Tolov.objects.get(id=request.data)
            d1 = datetime.strptime(datetime.today(), __format="%Y-%m-%d")
            d2 = datetime.strptime(joylashtirsh.kelgan_sana, "%Y-%m-%d")
            farqi = d1.day - d2.day
            joylashtirsh.yotgan_kuni_soni = farqi
            joylashtirsh.save()
            summa = xona.narx * farqi
            tolov.summa = summa
            return Response(serializer.data)
        return Response(serializer.errors)