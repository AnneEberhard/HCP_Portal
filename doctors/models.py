from django.db import models
from users.models import CustomUser


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('Allgemeinmedizin ', 'Allgemeinmedizin'),
        ('Innere Medizin', 'Innere Medizin'),
        ('Chirurgie', 'Chirurgie'),
        ('Anästhesiologie','Anästhesiologie'),
        ('Gynäkologie','Gynäkologie'),
        ('Pädiatrie','Pädiatrie'),
        ('Psychatrie','Psychatrie'),
        ('Radiologie','Radiologie'),
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
        return f"{self.user.get_full_name()} ({self.specialization})"

