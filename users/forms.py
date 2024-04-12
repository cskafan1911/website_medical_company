from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User, Patient, Doctor


class StyleFormMixin:
    """
    Класс Mixin для стилизации форм.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация класса StyleFormMixin.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Класс для формы регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ('avatar', 'phone', 'email', 'first_name', 'last_name', 'password1', 'password2')


class PatientProfileForm(StyleFormMixin, UserChangeForm):
    """
    Класс для формы просмотра профиля пациента.
    """

    class Meta:
        model = User
        fields = ('email', 'phone', 'avatar', 'first_name', 'last_name', 'date_of_birth')


class DoctorProfileForm(StyleFormMixin, UserChangeForm):
    """
    Класс для формы просмотра профиля врача.
    """

    class Meta:
        model = Doctor
        fields = ('description', 'speciality',)
