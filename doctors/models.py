from django.db import models
from users.models import CustomUser


class Doctor(models.Model):
    """
    Model representing a doctor.

    This model represents a doctor in the system. It extends the CustomUser model
    to include additional fields for doctor-specific information.

    Attributes:
        user (CustomUser): The associated user instance for the doctor.
        specialization (str): The specialization of the doctor chosen from a predefined list of choices.
        title (str): The title of the doctor chosen from a predefined list of choices.

    Methods:
        __str__(): Returns the string representation of the doctor instance.
    """

    SPECIALIZATION_CHOICES = [
        ('Allgemeinmedizin ', 'Allgemeinmedizin'),
        ('Innere Medizin', 'Innere Medizin'),
        ('Chirurgie', 'Chirurgie'),
        ('Anästhesiologie', 'Anästhesiologie'),
        ('Gynäkologie', 'Gynäkologie'),
        ('Pädiatrie', 'Pädiatrie'),
        ('Psychatrie', 'Psychatrie'),
        ('Radiologie', 'Radiologie'),
    ]

    TITLE_CHOICES = [
        ('Dr.med.', 'Dr.med.'),
        ('Prof. Dr.med.', 'Prof. Dr.med.'),
        ('PD Dr.med.', 'PD Dr.med.'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    title = models.CharField(max_length=20, choices=TITLE_CHOICES)

    def __str__(self):
        """
        Returns the string representation of the doctor instance.

        Returns:
            str: The full name of the associated user followed by the specialization.
        """
        return f"{self.user.get_full_name()} ({self.specialization})"
