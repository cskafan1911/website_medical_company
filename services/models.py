from django.db import models

from doctors.models import Doctor
from speciality.models import Speciality
from users.models import NULLABLE


class Service(models.Model):
    """
    Класс модели услуг.
    """

    title = models.CharField(max_length=100, verbose_name='Название услуги')
    price = models.PositiveIntegerField(verbose_name='Цена услуги')
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, verbose_name='Специализация', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    doctor = models.ManyToManyField(Doctor, verbose_name='Врач')

    def __str__(self):
        """
        Строковое представление модели услуга.
        """
        return f'{self.title} - {self.price}'

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
