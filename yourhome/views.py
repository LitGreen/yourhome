from django.shortcuts import render
import django_filters
from .models import Property
from .filters import PropertyFilter
from django.contrib import messages
from .forms import MultiselectFilterForm



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    advert_type = request.GET.get('advert_type')
    property_type = request.GET.get('property_type')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    queryset = Property.objects.all()

    if advert_type:
        queryset = queryset.filter(advert_type=advert_type)
    if property_type:
        queryset = queryset.filter(property_type=property_type)
    if price_min.isdigit() and price_max.isdigit():
        if int(price_min) <= int(price_max):
            queryset = queryset.filter(price__gt=price_min, price__lt=price_max)
        else:
            messages.error(request, 'Please enter a valid price.')
            
    
    filter_form = PropertyFilter(request.GET, queryset=queryset)
    properties = filter_form.qs



    context = {
        'filter_form': filter_form,
        'properties': properties,
        'advert_type_choices': Property.AdvertType.choices,
        'property_type_choices': Property.PropertyType.choices,
        'price_min': price_min,
        'price_max': price_max,
    }

    return render(request, 'yourhome/home.html', context)

def multiselectFilter(request, advert_type_slug=None, property_type_slug=None):
    advert_type = request.GET.get('advert_type')
    property_type = request.GET.get('property_type')
    form = MultiselectFilterForm(request.GET or None)
    price_gt = request.GET.get('price_gt', '')
    price_lt = request.GET.get('price_lt', '')
    queryset = Property.objects.all()

    advert_type_map = {
        'to-rent': 'To Rent', 
        'for-sale': 'For Sale', 
    }

    if advert_type_slug:
        advert_type = advert_type_map.get(advert_type_slug)
        if advert_type:
            queryset = queryset.filter(advert_type=advert_type)

    elif 'advert_type' in request.GET:
        advert_type = request.GET.get('advert_type')
        if advert_type:
            queryset = queryset.filter(advert_type=advert_type)

    property_type_map = {
        'house': 'House', 
        'apartment': 'Apartment', 
        'office': 'Office', 
        'warehouse': 'Warehouse', 
        'commercial': 'Commercial', 
        'other': 'Other', 
    }

    if property_type_slug:
        property_type = property_type_map.get(property_type_slug)
        if property_type:
            queryset = queryset.filter(property_type=property_type)


    elif 'property_type' in request.GET:
        property_type = request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type=property_type)

    initial_data = {}
    if property_type_slug:
        initial_data['property_type'] = property_type
    if advert_type:
        initial_data['advert_type'] = advert_type

    form = MultiselectFilterForm(request.GET or initial_data)

    if price_gt.isdigit() and price_lt.isdigit():
        if int(price_gt) <= int(price_lt):
            queryset = queryset.filter(price__gt=price_gt, price__lt=price_lt)
        else:
            messages.error(request, 'Please enter a valid price.')

    filter_form = PropertyFilter(request.GET, queryset=queryset)
    properties = filter_form.qs
  

    context = {
        'form': form,
        'filter_form': filter_form,
        'properties': properties,
        'advert_type_choices': Property.AdvertType.choices,
        'property_type_choices': Property.PropertyType.choices,
        'price_gt':  price_gt,
        'price_lt': price_lt,
    }

    return render(request, 'yourhome/multiselect_filter.html', context)
