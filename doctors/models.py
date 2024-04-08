from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from speciality.models import Speciality
from users.models import User, NULLABLE


class Doctor(models.Model):
    """
    Класс модели врача.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание')
    speciality = models.ManyToManyField(Speciality, verbose_name='Специализация')

    def __str__(self):
        """
        Строковое представление модели врач.
        """
        return f'{self.user.first_name} {self.user.last_name}'


@receiver(post_save, sender=User)
def create_user_doctor(sender, instance, created, **kwargs):
    if created:
        Doctor.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_doctor(sender, instance, **kwargs):
    instance.doctor.save()
