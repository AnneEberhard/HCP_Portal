from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from doctors.models import Doctor
from patients.models import Patient

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_doctor:
            Doctor.objects.create(user=instance)
        if instance.is_patient:
            Patient.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_doctor and hasattr(instance, 'doctorprofile'):
        instance.doctor.save()
    if instance.is_patient and hasattr(instance, 'patientprofile'):
        instance.patient.save()
