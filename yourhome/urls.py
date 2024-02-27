from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('multiselect_filter/', views.multiselectFilter, name="multiselect_filter"),
]