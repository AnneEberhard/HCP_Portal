from django.urls import path
from .views import PatientListAPIView, PatientDestroyAPIView


urlpatterns = [
    path('api/patients/', PatientListAPIView.as_view(), name='patient-list'),
    path('api/patients/<int:pk>/', PatientDestroyAPIView.as_view(), name='patient-destroy'),
]