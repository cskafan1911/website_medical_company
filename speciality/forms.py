from django import forms

from speciality.models import Speciality
from users.forms import StyleFormMixin


class SpecialityForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для форм объекта специализация.
    """

    class Meta:
        model = Speciality
        fields = ('image', 'speciality_name', 'description',)
