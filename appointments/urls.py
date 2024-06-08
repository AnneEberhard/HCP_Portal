from django.urls import path
from .views import AppointmentDestroyAPIView, AppointmentListCreateAPIView


urlpatterns = [
    path('api/appointments/', AppointmentListCreateAPIView.as_view(), name='appointment-list-create'),
    path('api/appointments/<int:pk>/', AppointmentDestroyAPIView.as_view(), name='appointment-destroy'),
]
