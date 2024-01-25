from django.urls import path
from tolovlar.consumers import *

websocket_urlpatterns = [
    path('ws/tolovlar/', TolovConsumer.as_asgi()),
]