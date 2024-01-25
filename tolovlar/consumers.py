from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import *
from .serializers import *

class TolovConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("tolov_group", self.channel_name)
        await self.send_all_payments()

    async def send_all_payments(self):
        tolovlar = await self.tolovlar_list()
        await self.send(text_data=json.dumps(tolovlar))

    @sync_to_async
    def tolovlar_list(self):
        tolovlar = Tolov.objects.all()
        serializer = TolovSerializer(tolovlar, many=True)
        return serializer.data

    async def bizda_update_bor(self, event):
        await self.send_all_payments()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("tolov_group", self.channel_name)