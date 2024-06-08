from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    This serializer includes the following fields from the CustomUser model:
    - id: The unique identifier for the user.
    - username: The username of the user.
    - first_name: The first name of the user.
    - last_name: The last name of the user.
    - email: The email address of the user.
    - is_doctor: A boolean indicating whether the user is a doctor.
    - is_patient: A boolean indicating whether the user is a patient.

    Raises:
        ValidationError: If the serialization data is not valid.

    Returns:
        dict: A dictionary containing the serialized user data.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_doctor', 'is_patient']
