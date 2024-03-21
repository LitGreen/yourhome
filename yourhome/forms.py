from django import forms
from .models import Property
from cities_light.models import Country, City
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _


class MultiselectFilterForm(forms.ModelForm):
    advert_type = forms.ChoiceField(choices=(Property.AdvertType.choices), required=False)
    city = forms.ModelChoiceField(queryset=City.objects.none(), required=False,)
    property_type = forms.ChoiceField(choices=[('Any', 'Any')] + list(Property.PropertyType.choices), required=False)
    price_min = forms.IntegerField(min_value=0, required=False)
    price_max = forms.IntegerField(min_value=0, required=False)
    total_floors = forms.MultipleChoiceField(choices=Property.TotalFloors.choices, widget=forms.CheckboxSelectMultiple, required=False)
    bedrooms = forms.MultipleChoiceField(choices=Property.Bedrooms.choices, widget=forms.CheckboxSelectMultiple, required=False)
    bathrooms = forms.MultipleChoiceField(choices=Property.Bathrooms.choices, widget=forms.CheckboxSelectMultiple, required=False)
    
    class Meta:
        model = Property
        fields = ['city', 'advert_type', 'property_type', 'price_min', 'price_max', 'total_floors', 'bedrooms', 'bathrooms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advert_type'].widget.attrs['class'] = 'select'
        self.fields['property_type'].widget.attrs['class'] = 'select'
        self.fields['price_min'].widget.attrs['class'] = 'form-control'
        self.fields['price_max'].widget.attrs['class'] = 'form-control'
        self.fields['total_floors'].widget.attrs['class'] = 'multiselect'
        self.fields['bedrooms'].widget.attrs['class'] = 'multiselect'
        self.fields['bathrooms'].widget.attrs['class'] = 'multiselect'
        uk = Country.objects.get(name='United Kingdom')
        self.fields['city'].queryset = City.objects.filter(country=uk)
        self.fields['city'].label = _("City / Town")
        
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'form-check-input'
                field.widget.attrs['is_checkbox'] = True
            else:
                field.widget.attrs['class'] = 'form-control'

        

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
    
