from django.shortcuts import render
import django_filters
from .models import Property
from .filters import PropertyFilter



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    advert_type = request.GET.get('advert_type')
    property_type = request.GET.get('property_type')
    queryset = Property.objects.all()
    if advert_type:
        queryset = queryset.filter(advert_type=advert_type)
    if property_type:
        queryset = queryset.filter(property_type=property_type)
    filter_form = PropertyFilter(request.GET, queryset=queryset)
    properties = filter_form.qs

    context = {
        'filter_form': filter_form,
        'properties': properties,
        'advert_type_choices': Property.AdvertType.choices,
        'property_type_choices': Property.PropertyType.choices,
    }
    return render(request, 'yourhome/home.html', context)
