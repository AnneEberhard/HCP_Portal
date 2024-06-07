from django.db import models
from users.models import CustomUser


class DoctorProfile(models.Model):
    SPECIALIZATION_CHOICES = [
        ('allgemeinmedizin ', 'Allgemeinmedizin'),
        ('innere medizin', 'Innere Medizin'),
        ('chirurgie', 'Chirurgie'),
        ('anästhesiologie','Anästhesiologie'),
        ('gynäkologie','Gynäkologie'),
        ('pädiatrie','Pädiatrie'),
        ('psychatrie','Psychatrie'),
        ('radiologie','Radiologie'),
    ]

    TITLE_CHOICES = [
        ('dr', 'Dr.med.'),
        ('prof', 'Prof. Dr.med.'),
        ('pd', 'PD Dr.med.'),
        # Weitere Titel hier hinzufügen
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    title = models.CharField(max_length=20, choices=TITLE_CHOICES)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.specialization})"

