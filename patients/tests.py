from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Patient
from users.models import CustomUser
from doctors.models import Doctor


class PatientAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_patient_url = reverse('patient-list-create')
        self.patient_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassword',
            'is_patient': True
        }

    def test_create_patient_success(self):
        response = self.client.post(self.create_patient_url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Patient.objects.filter(user__username=self.patient_data['username']).exists())

    def test_create_patient_existing_user(self):
        # Create a patient with the same username as an existing user
        CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', is_patient=True
        )
        response = self.client.post(self.create_patient_url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A user with that username already exists.', response.data['username'])

    def test_delete_patient_success(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', is_patient=True
        )
        patient = Patient.objects.create(user=self.user)
        response = self.client.delete(reverse('patient-destroy', kwargs={'pk': patient.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(pk=patient.pk).exists())
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())

    def test_delete_patient_with_doctor_association(self):

        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', is_patient=True
        )
        patient = Patient.objects.create(user=self.user)
        Doctor.objects.create(user=self.user, specialization='Allgemeinmedizin', title='Dr.med.')
        delete_url = reverse('patient-destroy', kwargs={'pk': patient.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(CustomUser.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(Patient.objects.filter(user=self.user).exists())
