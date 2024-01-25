from .views import *
from django.urls import path

urlpatterns = [
    path('', TolovApiView.as_view()),
    path('admin/', TolavAdminAPIView.as_view())
]