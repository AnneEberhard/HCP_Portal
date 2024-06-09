from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint to retrieve and create appointments for authenticated doctors and patients.

    - GET: Returns a list of appointments for the authenticated user.
      - If the user is a doctor, returns appointments where the user is the doctor.
      - If the user is a patient, returns appointments where the user is the patient.
      - If the user is neither a doctor nor a patient, returns an empty list.

    - POST: Creates a new appointment.
      - Requires both doctor and patient to be specified in the request data.
      - Validates that the specified doctor and patient exist.
      - Associates the appointment with the specified doctor and patient.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the queryset of appointments based on the authenticated user.
        """
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

    def create(self, request, *args, **kwargs):
        """
        Creates a new appointment.

        - Validates the user is authenticated.
        - Extracts doctor and patient IDs from the request data.
        - Validates that the specified doctor and patient exist.
        - Associates the appointment with the specified doctor and patient.
        - Saves and returns the new appointment data.
        """
        data = request.data.copy()

        doctor_user_id = data.get('doctor')
        patient_user_id = data.get('patient')

        if not doctor_user_id or not patient_user_id:
            return Response({"error": "Both doctor and patient must be specified."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(user__id=doctor_user_id)
            patient = Patient.objects.get(user__id=patient_user_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_400_BAD_REQUEST)

        data['doctor'] = doctor.user.id
        data['patient'] = patient.user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDestroyAPIView(generics.DestroyAPIView):
    """
    API endpoint to delete an appointment.

    - DELETE: Deletes an appointment.
      - Only allows deletion if the authenticated user is either the doctor or patient associated with the appointment.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Deletes an appointment if the authenticated user is involved (either as doctor or patient).

        - Validates that the user is authenticated and involved in the appointment.
        - Deletes the appointment if validation passes.
        """
        user = request.user
        appointment = self.get_object()

        if appointment.doctor.user == user or appointment.patient.user == user:
            self.perform_destroy(appointment)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to delete this appointment."}, status=status.HTTP_403_FORBIDDEN)
