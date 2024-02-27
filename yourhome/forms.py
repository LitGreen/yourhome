
from django.forms import ModelForm
from .models import Property
from django import forms
from django.core import validators


class MultiselectFilterForm(ModelForm):
    class Meta:
        model = Property
        fields = '__all__'