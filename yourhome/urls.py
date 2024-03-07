from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('filtered_properties/<str:property_type_slug>/<str:advert_type_slug>', views.multiselectFilter, name='filtered_properties'),
    
    ]
