from django.db import models

from services.models import Service
from users.models import NULLABLE, User, Doctor


class Appointment(models.Model):
    """
    Класс модели запись на обследование.
    """

    WAITING = 'WAITING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

    STATUS_CHOICES = [
        (WAITING, 'ожидание приема'),
        (COMPLETED, 'прием оказан'),
        (CANCELLED, 'прием отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пациент')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, verbose_name='врач',  **NULLABLE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='услуга')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время', **NULLABLE)
    status_of_appointment = models.CharField(max_length=20, choices=STATUS_CHOICES, default=WAITING)
    date_created = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(verbose_name='Цена', **NULLABLE)

    def __str__(self):
        """
        Строковое представление модели запись.
        """
        return f'{self.service} ({self.doctor}): ({self.status_of_appointment}) - {self.user}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def delete(self, *args, **kwargs):
        self.status_of_appointment = 'CANCELLED'


class Timetable(models.Model):
    """
    Класс для расписания.
    """

    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    doctor = models.ManyToManyField(Doctor, verbose_name='Врач')
    day_of_visit = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK, unique=True, verbose_name='День приема')

    def __str__(self):
        """
        Строковое представление модели расписание.
        """
        return f'{self.day_of_visit} {self.doctor}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
