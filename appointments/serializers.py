from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Appointment model.

    Serializes all fields of the Appointment model.
    """
    class Meta:
        model = Appointment
        fields = '__all__'
