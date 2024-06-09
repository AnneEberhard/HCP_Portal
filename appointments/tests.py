from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status

from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment

CustomUser = get_user_model()

class AppointmentAPITests(TestCase):
    
    def setUp(self):
        self.user_patient = CustomUser.objects.create_user(username='patient', password='password123')
        self.user_doctor = CustomUser.objects.create_user(username='doctor', password='password123')
        self.doctor = Doctor.objects.create(user=self.user_doctor)
        self.patient = Patient.objects.create(user=self.user_patient)
        self.client.login(username='patient', password='password123')

    def test_create_appointment(self):
        appointment_data = {
            'title': 'Checkup',
            'description': 'Regular checkup',
            'date': '2024-06-10T08:00:00Z',
            'doctor': self.user_doctor.id,
            'patient': self.user_patient.id
        }
        response = self.client.post('/api/appointments/', appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.get().title, 'Checkup')

    def test_retrieve_appointments_as_patient(self):
        response = self.client.get('/api/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No appointments yet for this patient

    def test_retrieve_appointments_as_doctor(self):
        self.client.logout()
        self.client.login(username='doctor', password='password123')
        response = self.client.get('/api/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No appointments yet for this doctor

    def test_delete_appointment(self):
        appointment = Appointment.objects.create(title='Test Appointment', description='Test Description', date='2024-06-10T08:00:00Z', doctor=self.doctor, patient=self.patient)
        response = self.client.delete(f'/api/appointments/{appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)
