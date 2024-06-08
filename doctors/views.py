from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Doctor
from .serializers import DoctorSerializer
from patients.models import Patient
from users.serializers import CustomUserSerializer


class DoctorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = CustomUserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            try:
                with transaction.atomic():
                    user = user_serializer.save()
                    print(f"User created with ID: {user.id}")

                    if Doctor.objects.filter(user=user).exists():
                        print(f"Doctor already exists for user ID: {user.id}")
                        return Response({"error": "Doctor with this user already exists."}, status=status.HTTP_400_BAD_REQUEST)

                    doctor = Doctor.objects.create(user=user)
                    
                    doctor.specialization = request.data.get('specialization')
                    doctor.title = request.data.get('title')
                    doctor.save()

                    doctor_serializer = self.get_serializer(doctor)
                    return Response(doctor_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                print(f"Error occurred: {str(e)}")
                user.delete()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
        print("User data is not valid")
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDestroyAPIView(generics.DestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

   # if user is supposed to be deleted from the database, add this
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        if not Patient.objects.filter(user=user).exists():
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
