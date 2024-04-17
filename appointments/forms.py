import datetime

from django import forms
from django.forms import NumberInput

from appointments.models import Appointment, Timetable
from services.models import Service
from users.forms import StyleFormMixin
from users.models import User, Doctor


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
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if kwargs['initial']:
            if isinstance(kwargs['initial'].get('service'), Service):
                self.fields['service'].queryset = Service.objects.filter(pk=kwargs['initial'].get('service').pk)
                self.fields['doctor'].queryset = kwargs['initial'].get('doctor')
            if isinstance(kwargs['initial'].get('doctor'), Doctor):
                self.fields['doctor'].queryset = Doctor.objects.filter(pk=kwargs['initial'].get('doctor').pk)
                self.fields['service'].queryset = kwargs['initial'].get('service')

    def clean(self):
        if not self._errors:
            cleaned_data = super(AppointmentForm, self).clean()
            doctor = cleaned_data.get('doctor')
            service = cleaned_data.get('service')
            date = cleaned_data.get('date')
            time = cleaned_data.get('time')
            appointments = Appointment.objects.filter(date=date, doctor=doctor, status_of_appointment='WAITING').order_by('date')
            timetable = [day.day_of_visit for day in Timetable.objects.filter(doctor=doctor).order_by('day_of_visit')]
            start_work = datetime.time(9)
            end_work = datetime.time(21)

            # # проверка полей doctor и service на совместимость
            # if doctor.direction != service.direction:
            #     raise forms.ValidationError('Выбранная услуга не оказывается врачом')
            #
            # # проверка даты - дата должна быть не раньше чем завтрашний день
            # if date < datetime.date.today() + datetime.timedelta(days=1):
            #     raise forms.ValidationError('Запись доступна только на завтра')
            #
            # # проверка расписания врача
            # if date.weekday() not in timetable:
            #     raise forms.ValidationError(f'Рабочие дни врача - {get_week_days(timetable)}')
            #
            # # проверка поле time - время должно укладываться в рабочие часы
            # # и быть свободным (время существующей записи + час)
            # all_time = [cursor.time for cursor in appointments.exclude(status='CN')]
            # if start_work <= time <= end_work:
            #     if not all_time or min(all_time) >= datetime.time(start_work.hour + 1):
            #         next_free_time = start_work
            #     else:
            #         next_free_time = datetime.time(start_work.hour + 1)
            #         for cur_time in all_time:
            #             if datetime.time(cur_time.hour - 1, cur_time.minute) < next_free_time:
            #                 next_free_time = datetime.time(cur_time.hour + 1, cur_time.minute)
            #     if next_free_time >= end_work:
            #         raise forms.ValidationError('Записи на этот день нет. Выберите другую дату')
            #     for cur_time in all_time:
            #         if cur_time <= time < datetime.time(cur_time.hour + 1, cur_time.minute):
            #             raise forms.ValidationError(f'Время {time.strftime("%H:%M")} '
            #                                         f'уже занято.Ближайшее свободное время '
            #                                         f'{next_free_time.strftime("%H:%M")}')
            # else:
            #     raise forms.ValidationError(f'Время работы клиники '
            #                                 f'с {start_work.strftime("%H:%M")} до {end_work.strftime("%H:%M")}')
            return cleaned_data


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ('doctor', 'day_of_visit',)
