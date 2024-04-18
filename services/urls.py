from django.urls import path

from services.views import ServiceListView, ServiceDetailView, SpecialityServiceListView, ServiceCreateView, \
    ServiceUpdateView, ServiceDeleteView
from services.apps import ServicesConfig

app_name = ServicesConfig.name

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('info/<int:pk>/', ServiceDetailView.as_view(), name='service_info'),
    path('speciality/<int:pk>/', SpecialityServiceListView.as_view(), name='speciality_service'),
    path('create/', ServiceCreateView.as_view(), name='service_create'),
    path('update/<int:pk>/', ServiceUpdateView.as_view(), name='service_update'),
    path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete')

]
