from django.db import transaction
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer
from doctors.models import Doctor
from users.serializers import CustomUserSerializer


class PatientListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve a list of patients or create a new patient.

    This view supports GET and POST requests:
    - GET: Returns a list of all patients.
    - POST: Creates a new patient along with the associated user.

    The POST request expects the following fields in the request data:
    - username: The username of the user.
    - first_name: The first name of the user.
    - last_name: The last name of the user.
    - email: The email address of the user.
    - is_doctor: Boolean indicating if the user is a doctor (should be true).
    - is_patient: Boolean indicating if the user is a patient.

    The method performs the following steps:
    1. Validates and creates a `CustomUser` instance from the provided user data.
    2. Checks if a `Patient` instance already exists for the created user.
    3. If not, creates a new `Patient` instance.
    4. Serializes and returns the newly created patient data.
    5. If any step fails, rolls back the transaction and returns an error response.

    Raises:
        ValidationError: If the provided data is not valid.
        Exception: If any error occurs during the creation process.

    Returns:
        Response: A Response object containing the serialized patient data or error messages.
    """
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
    """
    API view to delete a patient.

    This view supports DELETE requests to delete a patient from the database.
    If the associated user with the patient is not associated with any doctor,
    it will also be deleted from the database.

    Raises:
        Http404: If the patient instance does not exist.

    Returns:
        Response: A Response object with a status code indicating the success of the deletion.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    # if user is supposed to be deleted from the database, add this
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a patient instance from the database.

        If the associated user with the patient is not associated with any doctor,
        it will also be deleted from the database.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A Response object with a status code indicating the success of the deletion.
        """
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        if not Doctor.objects.filter(user=user).exists():
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
