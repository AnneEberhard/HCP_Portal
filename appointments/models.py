from django.db import models
from doctors.models import DoctorProfile
from patients.models import PatientProfile
from django.utils import timezone


class Appointment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.doctor.user.get_full_name()} - {self.date}"
