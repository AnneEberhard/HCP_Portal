from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Doctor model.

    This serializer includes the following fields from the Doctor model:
    - id: The unique identifier for the doctor.
    - title: The title of the doctor.
    - first_name: The first name of the user associated with the doctor.
    - last_name: The last name of the user associated with the doctor.
    - email: The email address of the user associated with the doctor.
    - specialization: The specialization of the doctor.
    - username: The username of the user associated with the doctor.

    The 'id' field is sourced from the associated user's ID, and other fields are sourced
    from the corresponding fields of the associated user and the Doctor model.

    Raises:
        ValidationError: If the serialization data is not valid.

    Returns:
        dict: A dictionary containing the serialized doctor data.
    """

    id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Doctor
        fields = ['id', 'title', 'first_name', 'last_name', 'email', 'specialization', 'username']
