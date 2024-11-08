from django.urls import path
from .views import CityAutocomplete, generate_pdf
from . import views
from django.conf import settings



urlpatterns = [
    path('', views.home, name="home"),
    path('filtered_properties/<str:property_type_slug>/<str:advert_type_slug>', views.multiselectFilter, name='filtered_properties'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),
    path('property_form', views.property_form, name="property_form"),
    path('property_form/<uuid:pk>/', views.property_form, name='property_form'),
    path('property_view/<uuid:pk>/', views.property_view, name='property_view'),
    path('delete_modal/<str:model_name>/<path:pk>/', views.delete_modal, name='delete_modal'),
    path('logout/', views.logout_user, name="logout"),
    path('user_profile/<str:pk>', views.user_profile, name="user_profile"),
    path('images_gallery', views.images_gallery, name="images_gallery"),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),

]


