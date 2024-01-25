from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from django.db.models import Sum
# Create your views here.

class TolovApiView(APIView):
    def get(self, request):
        tolovlar = Tolov.objects.order_by('-id')
        turi = request.query_params.get('turi')
        ism = request.query_params.get('ism')
        sana = request.query_params.get('sana')
        if ism:
            tolovlar = tolovlar.filter(bemor__ism__icontains=ism)
        if sana:
            tolovlar = tolovlar.filter(created_sana__icontains=sana) | tolovlar.filter(tolangan_sana__icontains=sana)
        if turi == 'yollanma':
            tolovlar = tolovlar.filter(joylashtihs__isnull=True)
        elif turi == 'joylashtish':
            tolovlar = tolovlar.filter(yollanma__isnull=True)
        serializer = TolovSerializer(tolovlar, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = TolovSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                tolandi = serializer.validated_data.get('summa') == serializer.validated_data.get('tolangan_summa')
            )
            channel = get_channel_layer()
            async_to_sync(channel.group_send)(
                "person_group", {
                    "type": "bizda_update_bor"
                },
            )
            return Response(serializer.data)
        return Response(serializer.errors)

    def update(self, request, pk):
        data = request.data
        tolov = Tolov.objects.get(id=pk)
        serializer = TolovSerializer(tolov, data=data)
        if serializer.is_valid():
            serializer.save()
            channel = get_channel_layer()
            async_to_sync(channel.group_send)(
                "person_group", {
                    "type": "bizda_update_bor"
                },
            )
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        tolov = Tolov.objects.filter(id=pk).delete()
        channel = get_channel_layer()
        async_to_sync(channel.group_send)(
            "person_group", {
                "type": "bizda_update_bor"
            },
        )
        return Response({"ochirildi": "True"})

class TolavAdminAPIView(APIView):
    def get(self, request):
        tolovlar = Tolov.objects.order_by('-id')
        turi = request.query_params.get('turi')
        sana = request.query_params.get('sana')
        bosh_sana = request.query_params.get('bosh_sana')
        yakuniy_sana = request.query_params.get('yakuniy_sana')
        if sana:
            tolovlar = tolovlar.filter(created_sana__icontains=sana) | tolovlar.filter(tolangan_sana__icontains=sana)
        if bosh_sana and yakuniy_sana:
            tolovlar = tolovlar.filter(created_sana__range=[bosh_sana, yakuniy_sana]) | tolovlar.filter(tolangan_sana__range=[bosh_sana, yakuniy_sana])
        if turi == 'yollanma':
            tolovlar = tolovlar.filter(joylashtihs__isnull=True)
        elif turi == 'joylashtish':
            tolovlar = tolovlar.filter(yollanma__isnull=True)
        summa = tolovlar.aggregate(s = Sum("summa")).get("s")
        if summa is None:
            summa = 0
        t_summa = tolovlar.aggregate(s=Sum("summa")).get("s")
        if summa is None:
            t_summa = 0
        serializer = TolovSerializer(tolovlar, many=True)
        result = {
            "tolovlar": serializer.data,
            "kutilgan_summa": summa,
            "tolangan_summa": t_summa,
            "qarzdorlik": summa - t_summa
        }
        return Response(result)


class QoshimchaTolovAPIView(APIView):
    def get(self, request):
        q_tolovar = QoshimchaTolov.objects.all()
        serializer = QoshimchaTolovSerializer(q_tolovar, many=True)
        return Response(serializer.data)

    def post(self, request):
        tolovlar = Tolov.objects.order_by('-id')
        summa = tolovlar.aggregate(s=Sum("summa")).get("s")
        data = request.data
        serializer = QoshimchaTolovSerializer(data=data)
        if serializer.is_valid():
            tolov = Tolov.objects.get(id=data.tolov.id)
            s = tolov.tolangan_summa + data.summa
            tolov.tolandi = s == tolov.summa
            tolov.save()
            serializer.save()
        return Response(serializer.data)


