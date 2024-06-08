from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Doctor
from .serializers import DoctorSerializer
from patients.models import Patient
from users.serializers import CustomUserSerializer


class DoctorListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve a list of doctors or create a new doctor.

    This view supports GET and POST requests:
    - GET: Returns a list of all doctors.
    - POST: Creates a new doctor along with the associated user.

    The POST request expects the following fields in the request data:
    - username: The username of the user.
    - first_name: The first name of the user.
    - last_name: The last name of the user.
    - email: The email address of the user.
    - is_doctor: Boolean indicating if the user is a doctor (should be true).
    - is_patient: Boolean indicating if the user is a patient.
    - specialization: The specialization of the doctor.
    - title: The title of the doctor.

    The method performs the following steps:
    1. Validates and creates a `CustomUser` instance from the provided user data.
    2. Checks if a `Doctor` instance already exists for the created user.
    3. If not, creates a new `Doctor` instance and sets the `specialization` and `title` fields.
    4. Serializes and returns the newly created doctor data.
    5. If any step fails, rolls back the transaction and returns an error response.

    Raises:
        ValidationError: If the provided data is not valid.
        Exception: If any error occurs during the creation process.

    Returns:
        Response: A Response object containing the serialized doctor data or error messages.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def create(self, request, *args, **kwargs):
        user_serializer = CustomUserSerializer(data=request.data)

        if user_serializer.is_valid():
            try:
                with transaction.atomic():
                    user = user_serializer.save()

                    if Doctor.objects.filter(user=user).exists():
                        return Response({"error": "Doctor with this user already exists."}, status=status.HTTP_400_BAD_REQUEST)

                    doctor = Doctor.objects.create(user=user)

                    doctor.specialization = request.data.get('specialization')
                    doctor.title = request.data.get('title')
                    doctor.save()

                    doctor_serializer = self.get_serializer(doctor)
                    return Response(doctor_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                user.delete()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDestroyAPIView(generics.DestroyAPIView):
    """
    API view to delete a doctor.

    This view supports DELETE requests to delete a doctor from the database.
    If the associated user with the doctor is not associated with any patient,
    it will also be deleted from the database.

    Raises:
        Http404: If the doctor instance does not exist.

    Returns:
        Response: A Response object with a status code indicating the success of the deletion.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    # if user is supposed to be deleted from the database, add this
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a doctor instance from the database.

        If the associated user with the doctor is not associated with any patient,
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
        if not Patient.objects.filter(user=user).exists():
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
