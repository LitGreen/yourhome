from .models import Property
from django import forms



# class MultiselectFilterForm(forms.Form):

#     class Meta:
#         model = Property
#         fields = ('advert_type', 'property_type', 'price_gt', 'price_lt')

class MultiselectFilterForm(forms.Form):
    advert_type = forms.ChoiceField(choices=Property.AdvertType.choices, required=False, widget=forms.Select(attrs={'class': 'select'}))
    property_type = forms.MultipleChoiceField(choices=Property.PropertyType.choices, required=False, widget=forms.Select(attrs={'class': 'select'}))
    price_gt = forms.IntegerField(required=False)
    price_lt = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advert_type'].widget.attrs['class'] = 'select'
        self.fields['property_type'].widget.attrs['class'] = 'select'
        self.fields['price_gt'].widget.attrs['class'] = 'form-control'
        self.fields['price_lt'].widget.attrs['class'] = 'form-control'