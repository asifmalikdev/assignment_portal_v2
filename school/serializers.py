from rest_framework import serializers
from .models import District, School, ClassRoom
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'is_active']