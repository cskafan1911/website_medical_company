from django.db import models

from doctors.models import Doctor
from services.models import Service
from users.models import User, NULLABLE


class Appointment(models.Model):
    """
    Класс модели записи на обследование.
    """

    WAITING = 'WAITING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    NO_APPOINTMENT = 'NO_APPOINTMENT'

    STATUS_CHOICES = [
        (WAITING, 'ожидание приема'),
        (COMPLETED, 'прием оказан'),
        (WAITING, 'прием отменен'),
        (NO_APPOINTMENT, 'записи нет')
    ]

    date_of_appointment = models.DateTimeField(verbose_name='Дата и время приема')
    status_of_appointment = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NO_APPOINTMENT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='пациент', **NULLABLE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor', verbose_name='врач')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='услуга')

    def __str__(self):
        """
        Строковое представление модели запись.
        """
        return f'{self.service} ({self.doctor}): {self.date_of_appointment}({self.status_of_appointment}) - {self.user}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
