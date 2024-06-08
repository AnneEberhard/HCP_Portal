from django.urls import path
from .views import DoctorListAPIView, DoctorDestroyAPIView

urlpatterns = [
    path('api/doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('api/doctors/<int:pk>/', DoctorDestroyAPIView.as_view(), name='doctor-destroy'),
]