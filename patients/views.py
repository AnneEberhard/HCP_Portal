from django.db import transaction, IntegrityError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer
from doctors.models import Doctor
from users.serializers import CustomUserSerializer


class PatientListCreateAPIView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = CustomUserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            try:
                with transaction.atomic():
                    user = user_serializer.save()

                    if Patient.objects.filter(user=user).exists():
                        return Response({"error": "Patient with this user already exists."}, status=status.HTTP_400_BAD_REQUEST)

                    patient = Patient.objects.create(user=user)

                    patient_serializer = self.get_serializer(patient)
                    return Response(patient_serializer.data, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                user.delete()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PatientDestroyAPIView(generics.DestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    # if user is supposed to be deleted from the database, add this
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        if not Doctor.objects.filter(user=user).exists():
          user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
