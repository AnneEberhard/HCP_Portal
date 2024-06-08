from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorSerializer
from patients.models import Patient


class DoctorListAPIView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


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
