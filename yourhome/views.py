from django.shortcuts import render
import django_filters
from .models import Property
from .filters import PropertyFilter
from django.contrib import messages
from .forms import MultiselectFilterForm
from cities_light.models import City



def home(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    advert_type = request.GET.get('advert_type')
    property_type = request.GET.get('property_type')
    cities = City.objects.all()
    city_id = request.GET.get('city')
    form = MultiselectFilterForm(request.GET or None)
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    queryset = Property.objects.all()
    
    if city_id:
        queryset = queryset.filter(city__id=city_id)
    if advert_type:
        queryset = queryset.filter(advert_type=advert_type)
    if property_type and property_type != 'Any':
        queryset = queryset.filter(property_type=property_type)
    if price_min.isdigit() and price_max.isdigit():
        if int(price_min) <= int(price_max):
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
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
        'cities': cities,
        'price_min': price_min,
        'price_max': price_max,
    }

    return render(request, 'yourhome/home.html', context)



def multiselectFilter(request, advert_type_slug=None, property_type_slug=None):
    
    property_type_map = {
        'any': 'Any',
        'house': 'House', 
        'flat-apartment': 'Flat / Apartment', 
        'office': 'Office', 
        'bungalow': 'Bungalow',
        'warehouse': 'Warehouse', 
        'commercial': 'Commercial', 
        'other': 'Other', 
    }

    advert_type_map = {
        'for-sale': 'For Sale',
        'to-rent': 'To Rent',
    }

    property_type = property_type_map.get(property_type_slug, request.GET.get('property_type'))
    advert_type = advert_type_map.get(advert_type_slug, request.GET.get('advert_type'))
    
    cities = City.objects.all()
    city_id = request.GET.get('city')
    total_floors = request.GET.getlist('total_floors')
    bedrooms = request.GET.getlist('bedrooms')
    bathrooms = request.GET.getlist('bathrooms')
    price_gt = request.GET.get('price_gt', '')
    price_lt = request.GET.get('price_lt', '')

    queryset = Property.objects.all()
    
    if city_id:
        queryset = queryset.filter(city__id=city_id)
    if total_floors:
        queryset = queryset.filter(total_floors__in=total_floors)
    if bedrooms:
        queryset = queryset.filter(bedrooms__in=bedrooms)
    if bathrooms:
        queryset = queryset.filter(bathrooms__in=bathrooms)
    if property_type and property_type != 'Any':
        queryset = queryset.filter(property_type=property_type)
    if advert_type:
        queryset = queryset.filter(advert_type=advert_type)
    if price_gt.isdigit() and price_lt.isdigit():
        if int(price_gt) > int(price_lt):
            messages.error(request, 'Minimum price should not be greater than maximum price.')
            queryset = Property.objects.none()
        else:
            queryset = queryset.filter(price__gte=price_gt, price__lte=price_lt)

    form = MultiselectFilterForm(request.GET or {'property_type': property_type, 'advert_type': advert_type})
    filter_form = PropertyFilter(request.GET, queryset=queryset)


    context = {
        'form': form,
        'filter_form': filter_form,
        'properties': queryset,
        'advert_type_choices': Property.AdvertType.choices,
        'property_type_choices': Property.PropertyType.choices,
        'cities': cities,
        'total_floors': total_floors,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'price_gt':  price_gt,
        'price_lt': price_lt,
    }

    return render(request, 'yourhome/filtered_properties.html', context)
