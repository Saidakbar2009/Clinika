from rest_framework import serializers
from .models import *

class TolovSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tolov
        fields = '__all__'

class QoshimchaTolovSerializer(serializers.ModelSerializer):
    class Meta:
        models = QoshimchaTolov
        fields = '__all__'