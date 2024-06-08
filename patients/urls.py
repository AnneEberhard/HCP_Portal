from django.urls import path
from .views import PatientDestroyAPIView, PatientListCreateAPIView


urlpatterns = [
    path('api/patients/', PatientListCreateAPIView.as_view(), name='patient-list-create'),
    path('api/patients/<int:pk>/', PatientDestroyAPIView.as_view(), name='patient-destroy'),
]