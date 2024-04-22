from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from services.forms import ServiceForm
from services.models import Service
from speciality.models import Speciality
from users.models import Doctor


class ServiceListView(ListView):
    """
    Класс для вывода списка медицинских услуг.
    """

    model = Service
    extra_context = {
        'title': 'Медицинские услуги'
    }

    def get_context_data(self, **kwargs):
        """
        Метод для получения списка объектов услуга.
        """
        context_data = super().get_context_data(**kwargs)
        context_data['service_list'] = Service.objects.all()

        return context_data


class ServiceDetailView(DetailView):
    """
    Класс для просмотра медицинской услуги.
    """

    model = Service

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['doctors'] = Doctor.objects.filter(speciality=self.kwargs.get('pk'))

        return context_data


class SpecialityServiceListView(ListView):
    """
    Класс просмотра списка услуг специализации.
    """

    model = Service
    extra_context = {
        'title': 'Специализации'
    }

    def get_queryset(self):
        """
        Метод для получения объектов Специализации.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(speciality=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, *args, **kwargs):
        """
        Метод для получения списка объектов услуги.
        """
        context_data = super().get_context_data(*args, **kwargs)

        speciality_item = Speciality.objects.get(pk=self.kwargs.get('pk'))
        context_data['speciality_pk'] = speciality_item.pk

        return context_data


class ServiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс для создания объекта Услуга.
    """

    model = Service
    permission_required = 'services.add_service'
    form_class = ServiceForm
    success_url = reverse_lazy('services:service_list')
    extra_context = {
        'title': 'Заполните форму для создания медицинской услуги'
    }


class ServiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс для редактирования объекта услуга.
    """

    model = Service
    permission_required = 'services.change_service'
    form_class = ServiceForm
    success_url = reverse_lazy('services:service_list')
    extra_context = {
        'title': 'Заполните форму для редактирования медицинской услуги.'
    }


class ServiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Класс для удаления объекта услуга.
    """

    model = Service
    permission_required = 'services.delete_service'
    success_url = reverse_lazy('services:service_list')
