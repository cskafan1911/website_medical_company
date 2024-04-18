from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from speciality.forms import SpecialityForm
from speciality.models import Speciality


class SpecialityListView(ListView):
    """
    Класс для вывода списка специализаций.
    """

    model = Speciality
    extra_context = {
        'title': 'Специализации'
    }
    
    def get_queryset(self):
        """
        Метод для получения объектов Специализации.
        """
        queryset = super().get_queryset()
        queryset = queryset.all()

        return queryset

    def get_context_data(self, **kwargs):
        """
        Метод для получения списка объектов специализации.
        """
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Speciality.objects.all()

        return context_data


class SpecialityDetailView(DetailView):
    """
    Класс для просмотра специализации.
    """

    model = Speciality


class SpecialityCreateView(CreateView):
    """
    Класс для создания объекта специализация.
    """

    model = Speciality
    form_class = SpecialityForm
    success_url = reverse_lazy('speciality:speciality_list')
    extra_context = {
        'title': 'Заполните форму для создания специализации'
    }


class SpecialityUpdateView(UpdateView):
    """
    Класс для редактирования объекта специализация.
    """

    model = Speciality
    form_class = SpecialityForm
    success_url = reverse_lazy('speciality:speciality_list')
    extra_context = {
        'title': 'Заполните форму для редактирования специализации'
    }


class SpecialityDeleteView(DeleteView):
    """
    Класс для удаления объекта специализации.
    """

    model = Speciality
    success_url = reverse_lazy('speciality:speciality_list')
