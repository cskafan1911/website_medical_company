from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

from appointments.forms import AppointmentForm, TimetableForm
from appointments.models import Appointment, Timetable
from appointments.services import send_email_for_patient, send_email_for_patient_update
from services.models import Service
from users.models import Doctor


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания записи к врачу.
    """

    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('services:service_list')
    extra_context = {
        'title': 'Заполните форму для записи к врачу'
    }

    def get_context_data(self, **kwargs):
        """
        Метод для получения объекта услуга и врач.
        """
        context_data = super().get_context_data(**kwargs)
        context_data['service_pk'] = self.request.GET.get('service_pk')
        context_data['doctor_pk'] = self.request.GET.get('doctor_pk')

        return context_data

    def get_initial(self):
        """
        Метод для настройки полей ввода.
        """
        initial = super(AppointmentCreateView, self).get_initial()
        if self.request.GET.get('service_pk'):
            service = Service.objects.get(pk=self.request.GET.get('service_pk'))
            initial['service'] = service
            initial['doctor'] = Doctor.objects.filter(speciality=service.speciality)
        if self.request.GET.get('doctor_pk'):
            doctor = Doctor.objects.get(pk=self.request.GET.get('doctor_pk'))
            initial['doctor'] = doctor
            initial['service'] = Service.objects.filter(speciality=doctor.speciality)

        return initial

    def form_valid(self, form):
        """
        Метод объединяет пользователя и созданную запись.
        """
        if form.is_valid():
            fields = form.save(commit=False)
            fields.user = self.request.user
            email_list = [self.request.user.email]
            send_email_for_patient(email_list, fields)

        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс для редактирования записи к врачу.
    """

    model = Appointment
    form_class = AppointmentForm
    extra_context = {
        'title': 'Редактировать запись'
    }

    def get_object(self, queryset=None):
        """
        Метод для ограничения прав доступа к объекту запись к врачу.
        """
        self.object = super().get_object(queryset)
        if self.object.user == self.request.user:
            return self.object
        if self.request.user.is_superuser or self.object.doctor == self.request.user.doctor:
            return self.object
        if self.object.user != self.request.user or self.object.doctor != self.request.user:
            raise Http404('Нет прав доступа')

    def get_success_url(self):
        return reverse('main:index', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        if form.is_valid():
            fields = form.save(commit=False)
            email_list = [self.request.user.email]
            send_email_for_patient_update(email_list, fields)
        return super().form_valid(form)


class AppointmentListView(ListView):
    """
    Класс просмотра объектов модели Запись к врачу.
    """

    model = Appointment
    
    def get_queryset(self):
        """
        Получение объектов модели Запись к врачу.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset


class TimetableCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс для создания расписания врача.
    """

    model = Timetable
    permission_required = 'appointments.add_timetable'
    form_class = TimetableForm
    success_url = reverse_lazy('services:service_list')


class TimetableListView(ListView):
    """
    Класс для просмотра расписания врача.
    """

    model = Timetable

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['doctors_list'] = Doctor.objects.all()
        context_data['timetable_list'] = Timetable.objects.all().order_by('day_of_visit')

        return context_data
