from django.urls import path

from services.views import ServiceListView, ServiceDetailView, SpecialityServiceListView
from services.apps import ServicesConfig

app_name = ServicesConfig.name

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('info/<int:pk>', ServiceDetailView.as_view(), name='service_info'),
    path('speciality/services/<int:pk>/', SpecialityServiceListView.as_view(), name='speciality_service')

]
