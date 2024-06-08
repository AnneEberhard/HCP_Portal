from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint to retrieve appointments for authenticated doctors and patients.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_doctor:
            # Filter appointments for authenticated doctors
            return Appointment.objects.filter(doctor__user=user)
        elif user.is_patient:
            # Filter appointments for authenticated patients
            return Appointment.objects.filter(patient__user=user)
        else:
            # Return empty queryset for other user types
            return Appointment.objects.none()


class AppointmentDestroyAPIView(generics.DestroyAPIView):
    """
    API endpoint to delete an appointment.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj.doctor.user == user or (obj.patient and obj.patient.user == user):
            return obj
        else:
            self.permission_denied(
                self.request, message="You do not have permission to delete this appointment."
            )

    def perform_destroy(self, instance):
        instance.delete()
