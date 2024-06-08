from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Patient model.

    This serializer includes the following fields from the Patient model:
    - id: The unique identifier for the patient.
    - first_name: The first name of the user associated with the patient.
    - last_name: The last name of the user associated with the patient.
    - email: The email address of the user associated with the patient.
    - username: The username of the user associated with the patient.

    The 'id' field is sourced from the associated user's ID, and other fields are sourced
    from the corresponding fields of the associated user.

    Raises:
        ValidationError: If the serialization data is not valid.

    Returns:
        dict: A dictionary containing the serialized patient data.
    """
    id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'email', 'username']
