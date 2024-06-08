from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer
from doctors.models import Doctor


class PatientListAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


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
