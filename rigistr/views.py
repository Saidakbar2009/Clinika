from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from .serializers import *
# Create your views here.

class BemorlarAPIView(APIView):
    def get(self, request):
        qidiruv = request.query_params.get("qidiruv")
        bemorlar = Bemor.objects.order_by('-id')
        if qidiruv is not None:
            bemorlar = bemorlar.filter(ism=qidiruv) | bemorlar.filter(tel=qidiruv)
        serializer = BemorSerializer(bemorlar, many=True)
        return Response(serializer.data)

class YollanmaAPIView(APIView):
    def get(self, request):
        yollanmalar = Yollanma.objects.all()
        serializer = YollanmaSerializer(yollanmalar, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = YollanmaSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)