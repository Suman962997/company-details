from rest_framework import serializers
from .models import Company

class serializersclass(serializers.ModelSerializer):
    class Meta:
        model=Company
        fields="__all__"