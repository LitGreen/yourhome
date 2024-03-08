from .models import Property
from django import forms


class MultiselectFilterForm(forms.Form):
    advert_type = forms.ChoiceField(choices=(Property.AdvertType.choices), required=False)
    property_type = forms.ChoiceField(choices=[('Any', 'Any')] + list(Property.PropertyType.choices), required=False)
    price_gt = forms.IntegerField(min_value=0, required=False)
    price_lt = forms.IntegerField(min_value=0, required=False)
    total_floors = forms.MultipleChoiceField(choices=Property.TotalFloors.choices, required=False)
    bedrooms = forms.MultipleChoiceField(choices=Property.Bedrooms.choices, required=False)  
    bathrooms = forms.MultipleChoiceField(choices=Property.Bathrooms.choices, required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advert_type'].widget.attrs['class'] = 'select'
        self.fields['property_type'].widget.attrs['class'] = 'select'
        self.fields['price_gt'].widget.attrs['class'] = 'form-control'
        self.fields['price_lt'].widget.attrs['class'] = 'form-control'
        self.fields['total_floors'].widget.attrs['class'] = 'multiselect'
        self.fields['bedrooms'].widget.attrs['class'] = 'multiselect'
        self.fields['bathrooms'].widget.attrs['class'] = 'multiselect'

   