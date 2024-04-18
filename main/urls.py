from django.urls import path

from main.apps import MainConfig
from main.views import IndexView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

]
