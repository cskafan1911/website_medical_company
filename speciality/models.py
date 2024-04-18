from django.db import models


class Speciality(models.Model):
    """
    Класс модели специализации.
    """

    speciality_name = models.CharField(max_length=300, verbose_name='Специальность')
    description = models.TextField(verbose_name='Описание специализации')
    image = models.ImageField(upload_to='image_speciality/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        """
        Строковое представление класса специализация.
        """
        return f'{self.speciality_name}'

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
