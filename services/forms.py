from django import forms

from services.models import Service
from users.forms import StyleFormMixin


class ServiceForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для форм объекта услуга.
    """

    class Meta:
        model = Service
        fields = ('image', 'title', 'price', 'description', 'speciality',)
