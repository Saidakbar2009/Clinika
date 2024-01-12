from django.urls import path
from .views import *

urlpatterns = [
    path('', BemorlarAPIView.as_view()),
    path('yollanma/', YollanmaAPIView.as_view())
]