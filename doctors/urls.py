from django.urls import path
from .views import DoctorDestroyAPIView, DoctorListCreateAPIView

urlpatterns = [
    path('api/doctors/', DoctorListCreateAPIView.as_view(), name='doctor-list'),
    path('api/doctors/<int:pk>/', DoctorDestroyAPIView.as_view(), name='doctor-destroy'),
]
