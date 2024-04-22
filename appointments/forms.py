import datetime

from django import forms
from django.forms import NumberInput

from appointments.models import Appointment, Timetable
from appointments.services import check_doctor_service, check_timetable_date, check_doctor_timetable_date, \
    check_appointment_time
from services.models import Service
from users.forms import StyleFormMixin
from users.models import Doctor


class AppointmentForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для формы записи к врачу.
    """

    class Meta:
        model = Appointment
        fields = ('doctor', 'service', 'date', 'time',)
        widgets = {
            'date': NumberInput(attrs={'type': 'date'}),
            'time': NumberInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация класса AppointmentForm.
        """
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if kwargs['initial']:
            if isinstance(kwargs['initial'].get('service'), Service):
                self.fields['service'].queryset = Service.objects.filter(pk=kwargs['initial'].get('service').pk)
                self.fields['doctor'].queryset = kwargs['initial'].get('doctor')
            if isinstance(kwargs['initial'].get('doctor'), Doctor):
                self.fields['doctor'].queryset = Doctor.objects.filter(pk=kwargs['initial'].get('doctor').pk)
                self.fields['service'].queryset = kwargs['initial'].get('service')

    def clean(self):
        """
        Метод для проверки заполнения формы.
        """
        if not self._errors:
            cleaned_data = super(AppointmentForm, self).clean()
            doctor = cleaned_data.get('doctor')
            service = cleaned_data.get('service')
            date = cleaned_data.get('date')
            time = cleaned_data.get('time')
            appointments = Appointment.objects.filter(date=date, doctor=doctor,
                                                      status_of_appointment='WAITING').order_by('date')
            timetable = [day.day_of_visit for day in Timetable.objects.filter(doctor=doctor).order_by('day_of_visit')]
            start_work = datetime.time(10)
            end_work = datetime.time(19)
            all_time = [cursor.time for cursor in appointments.exclude(status_of_appointment='CANCELLED')]

            check_doctor_service(doctor, service)
            check_timetable_date(date)
            check_doctor_timetable_date(date, timetable)
            check_appointment_time(all_time, time, start_work, end_work)

            return cleaned_data


class TimetableForm(forms.ModelForm):
    """
    Класс формы для создания модели расписания врача.
    """

    class Meta:
        model = Timetable
        fields = ('doctor', 'day_of_visit',)
