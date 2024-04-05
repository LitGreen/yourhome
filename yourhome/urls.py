from django.urls import path
from .views import CityAutocomplete
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('filtered_properties/<str:property_type_slug>/<str:advert_type_slug>', views.multiselectFilter, name='filtered_properties'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),
    path('property_form', views.property_form, name="property_form"),
    path('property_form/<uuid:pk>/', views.property_form, name='property_form'),
    path('property_view/<uuid:pk>/', views.property_view, name='property_view'),
    path('property_delete/<uuid:pk>/', views.property_delete, name='property_delete'),
]
