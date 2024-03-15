from django import forms
from django.db import IntegrityError
from .models import Property, Address
from cities_light.models import Country, City
from django.core.exceptions import ObjectDoesNotExist


class MultiselectFilterForm(forms.ModelForm):
    advert_type = forms.ChoiceField(choices=(Property.AdvertType.choices), required=False)
    city = forms.ModelChoiceField(queryset=City.objects.none(), required=False,)
    property_type = forms.ChoiceField(choices=[('Any', 'Any')] + list(Property.PropertyType.choices), required=False)
    price_gt = forms.IntegerField(min_value=0, required=False)
    price_lt = forms.IntegerField(min_value=0, required=False)
    total_floors = forms.MultipleChoiceField(choices=Property.TotalFloors.choices, widget=forms.CheckboxSelectMultiple, required=False)
    bedrooms = forms.MultipleChoiceField(choices=Property.Bedrooms.choices, widget=forms.CheckboxSelectMultiple, required=False)
    bathrooms = forms.MultipleChoiceField(choices=Property.Bathrooms.choices, widget=forms.CheckboxSelectMultiple, required=False)
    
    class Meta:
        model = Property
        fields =  '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advert_type'].widget.attrs['class'] = 'select'
        self.fields['property_type'].widget.attrs['class'] = 'select'
        self.fields['price_gt'].widget.attrs['class'] = 'form-control'
        self.fields['price_lt'].widget.attrs['class'] = 'form-control'
        self.fields['total_floors'].widget.attrs['class'] = 'multiselect'
        self.fields['bedrooms'].widget.attrs['class'] = 'multiselect'
        self.fields['bathrooms'].widget.attrs['class'] = 'multiselect'
        uk = Country.objects.get(name='United Kingdom')
        self.fields['country'].initial = uk
        self.fields['city'].queryset = City.objects.filter(country=uk)

    def save(self, commit=True):
        instance = super().save(commit=False)
        city = self.cleaned_data.get('city')
        country = self.cleaned_data.get('country')
        if city and country:
            try:
                city_name = city.name.split(',')[0].strip() 
                city_instance = City.objects.get(name=city_name, country=country)
                instance.city = city_instance
                instance.country = country
            except ObjectDoesNotExist:
                raise ValueError(f"City with name {city_name} in country {country} does not exist.")
        elif not instance.country:
            uk = Country.objects.get(name='United Kingdom')
            instance.country = uk
        if commit:
            instance.save()
        return instance
