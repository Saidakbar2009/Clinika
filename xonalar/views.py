from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rigistr.models import *
from tolovlar.models import *
from .serializers import *
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