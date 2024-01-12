from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bemor/', include('rigistr.urls')),
    path('xona/', include('xonalar.urls'))
]
