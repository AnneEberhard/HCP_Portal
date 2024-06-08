from django.db import models
from users.models import CustomUser


class Patient(models.Model):
    """
    Model representing a patient.

    This model extends the CustomUser model to represent patients in the system.
    It contains a one-to-one relationship with the CustomUser model, which serves
    as the primary key for the patient.

    Attributes:
        user (CustomUser): The associated user instance for the patient.

    Methods:
        __str__(): Returns the full name of the associated user as the string representation
                   of the patient instance.
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        """
        Returns the full name of the associated user as the string representation
        of the patient instance.

        Returns:
            str: The full name of the associated user.
        """
        return self.user.get_full_name()
