from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from patients.models import Patient
from users.models import CustomUser
from .models import Doctor


class DoctorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_doctor_url = reverse('doctor-list-create')
        self.doctor_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpassword',
            'is_doctor': True,
            'specialization': 'Allgemeinmedizin',
            'title': 'Dr.med.'
        }

    def test_create_doctor_success(self):
        response = self.client.post(self.create_doctor_url, self.doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Doctor.objects.filter(user__username=self.doctor_data['username']).exists())

    def test_create_doctor_existing_user(self):
        # Create a doctor with the same username as an existing user
        CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', is_doctor=True
        )
        response = self.client.post(self.create_doctor_url, self.doctor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A user with that username already exists.', response.data['username'])

    def test_delete_doctor_success(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', is_doctor=True
        )
        doctor = Doctor.objects.create(user=self.user, specialization='Allgemeinmedizin', title='Dr.med.')
        response = self.client.delete(reverse('doctor-destroy', kwargs={'pk': doctor.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(pk=doctor.pk).exists())
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())

    def test_delete_doctor_with_patient_association(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword', is_doctor=True
        )
        doctor = Doctor.objects.create(user=self.user, specialization='Allgemeinmedizin', title='Dr.med.')
        Patient.objects.create(user=self.user)
        delete_url = reverse('doctor-destroy', kwargs={'pk': doctor.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(CustomUser.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(Doctor.objects.filter(user=self.user).exists())
