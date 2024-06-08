from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Model representing a custom user in the system.

    This model extends the built-in AbstractUser model provided by Django
    to include additional fields for custom user types.

    Attributes:
        username (str): The unique username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        is_doctor (bool): Indicates whether the user is a doctor.
        is_patient (bool): Indicates whether the user is a patient.

    Methods:
        __str__(): Returns the string representation of the user instance.
    """

    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the string representation of the user instance.

        Returns:
            str: The username of the user.
        """
        return self.username
