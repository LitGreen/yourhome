from django.urls import path
from .views import CityAutocomplete
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('filtered_properties/<str:property_type_slug>/<str:advert_type_slug>', views.multiselectFilter, name='filtered_properties'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),
    path('property_form', views.property_form, name="property_form"),
    path('property_form/<uuid:pk>/', views.property_form, name='property_form'),
    path('property_view/<uuid:pk>/', views.property_view, name='property_view'),
    path('property_delete/<uuid:pk>/', views.property_delete, name='property_delete'),
    path('logout/', views.logoutUser, name="logout"),
    path('user_profile/<str:pk>', views.user_profile, name="user_profile"),

]


