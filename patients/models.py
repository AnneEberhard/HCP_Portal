from django.db import models
from users.models import CustomUser


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.get_full_name()

