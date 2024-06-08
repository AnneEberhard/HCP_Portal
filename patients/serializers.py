from rest_framework import serializers
from .models import Patient
from users.models import CustomUser


class PatientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'username']