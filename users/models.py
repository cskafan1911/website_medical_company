from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    Класс для Пользователя.
    """
    
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users_avatar/', verbose_name='аватар пользователя', **NULLABLE)
    first_name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия пользователя')
    date_of_birth = models.DateField(verbose_name='дата рождения', **NULLABLE)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Строковое представление модели пользователя.
        """
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
