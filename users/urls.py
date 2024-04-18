from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import RegisterView, UserConfirmEmailView, EmailConfirmationSentView, EmailConfirmedView, \
    EmailConfirmationFailedView, UserUpdateView, ProfileDoctorView, DoctorListView, DoctorDetailView, \
    DoctorUpdateView, DoctorDeleteView, DoctorCreateView, DoctorAppointmentsView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/doctor/', ProfileDoctorView.as_view(), name='profile_doctor'),
    path('profile/doctor/appointments/<int:pk>/', DoctorAppointmentsView.as_view(), name='appointments'),
    path('doctor/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/info/<int:pk>/', DoctorDetailView.as_view(), name='doctor_info'),
    path('doctor/update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctor/delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('confirm-email/<str:uidb64>/<str:token>', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email-confirmation-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                                      email_template_name='users/password_reset_email.html',
                                                      from_email=settings.EMAIL_HOST_USER,
                                                      success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete')

]
