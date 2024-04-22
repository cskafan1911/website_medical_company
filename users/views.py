from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView, DeleteView

from appointments.models import Appointment
from users.forms import UserRegisterForm, DoctorForm, UserUpdateForm, DoctorProfileForm
from users.models import User, Doctor


class RegisterView(CreateView):
    """
    Класс регистрации пользователя.
    """

    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Метод для проверки валидации почты пользователя.
        Генерирует ссылку для валидации и отправляет на электронную почту пользователя.
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = get_current_site(self.request)
        send_mail(
            'Подтвердите электронный адрес',
            f'Ссылка для подтверждения: http://{current_site.domain}{activation_url}',
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):
    """
    Класс активации пользователя, после проверки электронной почты.
    """

    @staticmethod
    def get(request, uidb64, token):
        """
        Метод сравнивает сгенерированный код для проверки электронной почты и активирует пользователя
        после успешной проверки.
        """
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verify = True
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваша почта активирована'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваша почта не активирована'
        return context


class UserDeleteView(DeleteView):
    """
    Класс для удаления объекта пользователь.
    """

    model = User
    success_url = reverse_lazy('main:index')


class UserUpdateView(UpdateView):
    """
    Класс для редактирования профиля пользователя.
    """

    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile')
    extra_context = {
        'title': 'Личный кабинет пользователя'
    }

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDoctorView(UpdateView):
    """
    Класс для редактирования профиля врача.
    """

    model = Doctor
    form_class = DoctorProfileForm
    success_url = reverse_lazy('users:profile_doctor')
    extra_context = {
        'title': 'Личный кабинет врача'
    }

    def get_object(self, queryset=None):
        return self.request.user


class DoctorAppointmentsView(TemplateView):
    """
    Класс для просмотра записей врача.
    """

    template_name = 'users/doctor_appointments.html'

    def get_context_data(self, **kwargs):
        """
        Метод для вывода информации о записях врача.
        """
        context_data = super().get_context_data(**kwargs)
        doctor = self.request.user
        doctor_app = Doctor.objects.get(user=doctor.pk)
        context_data['appointments_list'] = Appointment.objects.filter(doctor=doctor_app.pk)

        return context_data


class DoctorListView(ListView):
    """
    Класс для вывода списка врачей.
    """

    model = Doctor

    def get_context_data(self, *args, **kwargs):
        """
        Метод для получения списка врачей.
        """
        context_data = super().get_context_data(*args, **kwargs)

        context_data['doctors_list'] = Doctor.objects.all()

        return context_data


class DoctorDetailView(DetailView):
    """
    Класс для получения информации о враче.
    """

    model = Doctor


class DoctorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс для редактирования объекта врач.
    """

    model = Doctor
    form_class = DoctorForm
    permission_required = 'users.change_doctor'
    success_url = reverse_lazy('users:doctor_list')
    extra_context = {
        'title': 'Заполните форму для редактирования информации о враче'
    }


class DoctorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс для добавления зарегистрированного пользователя в объект врач.
    """

    model = Doctor
    form_class = DoctorForm
    permission_required = 'users.add_doctor'
    success_url = reverse_lazy('users:doctor_list')
    extra_context = {
        'title': 'Заполните форму для добавления врача'
    }


class DoctorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Класс для удаления объекта врач.
    """

    model = Doctor
    permission_required = 'users.delete_doctor'
    success_url = reverse_lazy('users:doctor_list')
