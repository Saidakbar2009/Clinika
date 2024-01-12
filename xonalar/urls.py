from django.urls import path
from .views import *

urlpatterns = [
    path('', XonaAPIView.as_view())
]