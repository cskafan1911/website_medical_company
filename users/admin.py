from django.contrib import admin

from users.models import User, Doctor

admin.site.register(User)
admin.site.register(Doctor)
