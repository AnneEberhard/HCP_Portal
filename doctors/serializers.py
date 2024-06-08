from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Doctor
        fields = ['id', 'title', 'first_name', 'last_name', 'email', 'specialization', 'username']