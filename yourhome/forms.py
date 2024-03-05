from .models import Property
from django import forms


class MultiselectFilterForm(forms.ModelForm):
    price_gt = forms.IntegerField(min_value=0, required=False)
    price_lt = forms.IntegerField(min_value=0, required=False)
    total_floors = forms.MultipleChoiceField(choices=Property.TotalFloors.choices, required=False)
    bedrooms = forms.MultipleChoiceField(choices=Property.Bedrooms.choices, required=False)  
    bathrooms = forms.MultipleChoiceField(choices=Property.Bathrooms.choices, required=False)
    


    class Meta:
        model = Property
        fields = ('advert_type', 'property_type')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advert_type'].widget.attrs['class'] = 'select'
        self.fields['property_type'].widget.attrs['class'] = 'select'
        self.fields['price_gt'].widget.attrs['class'] = 'form-control'
        self.fields['price_lt'].widget.attrs['class'] = 'form-control'
        self.fields['total_floors'].widget.attrs['class'] = 'multiselect'
        self.fields['bedrooms'].widget.attrs['class'] = 'multiselect'
        self.fields['bathrooms'].widget.attrs['class'] = 'multiselect'

   