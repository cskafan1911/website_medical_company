from django.urls import path

from appointments.apps import AppointmentsConfig
from appointments.views import AppointmentCreateView, AppointmentListView, TimetableCreateView, \
    AppointmentUpdateView, TimetableListView

app_name = AppointmentsConfig.name

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment_list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment_update'),
    path('timetable/create/', TimetableCreateView.as_view(), name='timetable_create'),
    path('timetable/', TimetableListView.as_view(), name='timetable_list')

]
