from django.views.generic import TemplateView

from main.utils import get_random_choice
from services.models import Service
from speciality.models import Speciality
from users.models import Doctor


class IndexView(TemplateView):
    """
    Класс для главной страницы сайта.
    """

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        """
        Метод для вывода информации на главную страницу.
        """

        context_data = super().get_context_data(**kwargs)
        context_data['speciality_list'] = Speciality.objects.all()
        context_data['doctors'] = get_random_choice(Doctor.objects.all())
        context_data['service_list'] = get_random_choice(Service.objects.all())

        return context_data
