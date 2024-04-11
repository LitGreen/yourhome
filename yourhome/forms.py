from django import forms
from .models import Property
from cities_light.models import Country, City
from django.utils.translation import gettext as _
from dal import autocomplete
from django.shortcuts import get_object_or_404
from collections import OrderedDict
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'bio', 'avatar', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class MultiselectFilterForm(forms.ModelForm):
    advert_type = forms.ChoiceField(choices=(Property.AdvertType.choices), required=False)
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='city-autocomplete', attrs={'data-placeholder': 'Enter a city or town name'}),
        required=False
    )
    property_type = forms.ChoiceField(choices=[('Any', 'Any')] + list(Property.PropertyType.choices), required=False)
    price_min = forms.IntegerField(min_value=0, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Min Price'}))
    price_max = forms.IntegerField(min_value=0, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Max Price'}))
    total_floors = forms.MultipleChoiceField(choices=Property.TotalFloors.choices, widget=forms.CheckboxSelectMultiple, required=False)
    bedrooms = forms.MultipleChoiceField(choices=Property.Bedrooms.choices, widget=forms.CheckboxSelectMultiple, required=False)
    bathrooms = forms.MultipleChoiceField(choices=Property.Bathrooms.choices, widget=forms.CheckboxSelectMultiple, required=False)
    
    class Meta:
        model = Property
        fields = ['city', 'advert_type', 'property_type', 'total_floors', 'bedrooms', 'bathrooms']
         
    def clean_city(self):
        city = self.cleaned_data.get('city')
        return city

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
        if city:
            instance.city = city
            instance.country = city.country 
        elif not instance.country:
            uk = Country.objects.get(name='United Kingdom')
            instance.country = uk
        if commit:
            instance.save()
        return instance
    
    
    def form_valid(self, form):
        city_name = form.cleaned_data.get('city')
        city = get_object_or_404(City, name=city_name)
        form.instance.city = city
        return super().form_valid(form)
    

class PropertyForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='city-autocomplete', attrs={'data-placeholder': 'Enter a city or town name'}),
        required=False
    )
  
    class Meta:
        model = Property
        exclude = [ 'slug', 'country' ]
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        return city

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uk = Country.objects.get(name='United Kingdom')
        self.fields['city'].queryset = City.objects.filter(country=uk)
        self.fields['city'].label = _("City / Town")

    def save(self, commit=True):
        instance = super().save(commit=False)
        city = self.cleaned_data.get('city')
        if city:
            instance.city = city
            instance.country = city.country 
        elif not instance.country:
            uk = Country.objects.get(name='United Kingdom')
            instance.country = uk
        if commit:
            instance.save()
        return instance

class PropertyViewForm(forms.ModelForm):
    city = forms.CharField(disabled=True)

    class Meta:
        model = Property
        exclude = ['slug', 'country', 'city', 'published_status', 'photo1', 'photo2', 'photo3', 'photo4']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.city:
            self.fields['city'].initial = self.instance.city.name
        if self.instance.description == "Add description here...":
            self.fields['description'].initial = ""
        self.fields['city'].label = "City / Town"
        self.fields = OrderedDict([
            ('cover_photo', self.fields['cover_photo']),
            ('title', self.fields['title']),
            ('city', self.fields['city']),
        ] + [item for item in self.fields.items() if item[0] not in ['cover_photo', 'city']])
        for field in self.fields.values():
            if field.label:
                field.label += ': '
            field.disabled = True
        
