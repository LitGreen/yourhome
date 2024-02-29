from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('multiselect_filter/', views.multiselectFilter, name="multiselect_filter"),
    path('filtered_properties/<str:property_type_slug>/<str:advert_type_slug>/', views.multiselectFilter, name="filtered_properties"),
    ]
