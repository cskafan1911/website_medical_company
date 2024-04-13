from django.urls import path

from speciality.apps import SpecialityConfig
from speciality.views import SpecialityListView, SpecialityDetailView, SpecialityCreateView, SpecialityUpdateView, \
    SpecialityDeleteView

app_name = SpecialityConfig.name

urlpatterns = [
    path('', SpecialityListView.as_view(), name='speciality_list'),
    path('info/<int:pk>/', SpecialityDetailView.as_view(), name='speciality_info'),
    path('create/', SpecialityCreateView.as_view(), name='speciality_create'),
    path('update/<int:pk>/', SpecialityUpdateView.as_view(), name='speciality_update'),
    path('delete/<int:pk>/', SpecialityDeleteView.as_view(), name='speciality_delete'),

]
