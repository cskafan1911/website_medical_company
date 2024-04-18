from django.contrib import admin

from speciality.models import Speciality


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    """
    Класс для настройки панели администратора модели Специализация.
    """

    list_display = ('pk', 'speciality_name')
