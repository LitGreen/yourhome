from django.shortcuts import get_object_or_404, render, redirect
from .models import Property
from .filters import PropertyFilter
from django.contrib import messages
from .forms import MultiselectFilterForm, PropertyForm, PropertyViewForm
from cities_light.models import City
from dal import autocomplete


def filter_properties(request, queryset, filters):
    price_min = filters.get('price_min', '')
    price_max = filters.get('price_max', '')
    
    for filter_name, filter_value in filters.items():
        if filter_value and filter_name not in ['price_min', 'price_max']:
            queryset = queryset.filter(**{filter_name: filter_value})

    if price_min.isdigit() and price_max.isdigit():
        if int(price_min) > int(price_max):
            messages.error(request, 'Please enter a valid price range.')
            queryset = queryset.none()
        else:
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
    
    return queryset


def home(request): 

    filters = {
        'city__id': request.GET.get('city'),
        'advert_type': request.GET.get('advert_type'),
        'property_type': request.GET.get('property_type') if request.GET.get('property_type') != 'Any' else None,
        'price_min': request.GET.get('price_min', ''),
        'price_max': request.GET.get('price_max', ''),
    }

    queryset = Property.objects.all()
    queryset = filter_properties(request, queryset, filters)
    
    filter_form = PropertyFilter(request.GET, queryset=queryset)
    properties = filter_form.qs

    context = {
        'form': MultiselectFilterForm(request.GET or None),
        'filter_form': filter_form,
        'properties': properties,
        'advert_type_choices': Property.AdvertType.choices,
        'property_type_choices': Property.PropertyType.choices,
        'cities': City.objects.all(),
        'price_min': filters['price_min'],
        'price_max': filters['price_max'],
    }

    return render(request, 'yourhome/home.html', context)
    

def multiselectFilter(request, advert_type_slug=None, property_type_slug=None):
    property_type_map = {
        'any': None,
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

    filters = {
        'city__id': request.GET.get('city'),
        'total_floors__in': request.GET.getlist('total_floors'),
        'bedrooms__in': request.GET.getlist('bedrooms'),
        'bathrooms__in': request.GET.getlist('bathrooms'),
        'price_min': request.GET.get('price_min', ''),
        'price_max': request.GET.get('price_max', ''),
    }

    property_type = property_type_map.get(property_type_slug, request.GET.get('property_type'))
    if property_type is not None and property_type != 'Any':
        filters['property_type'] = property_type

    advert_type = advert_type_map.get(advert_type_slug, request.GET.get('advert_type'))
    if advert_type is not None and advert_type != 'Any':
        filters['advert_type'] = advert_type

    queryset = Property.objects.all()
    queryset = filter_properties(request, queryset, filters)

    form = MultiselectFilterForm(request.GET or {'property_type': filters.get('property_type'), 'advert_type': filters.get('advert_type')})
    filter_form = PropertyFilter(request.GET, queryset=queryset)

    context = {
        'form': form,
        'filter_form': filter_form,
        'properties': queryset,
        'advert_type_choices': Property.AdvertType.choices,
        'property_type_choices': Property.PropertyType.choices,
        'cities': City.objects.all(),
        'total_floors': filters.get('total_floors__in'),
        'bedrooms': filters.get('bedrooms__in'),
        'bathrooms': filters.get('bathrooms__in'),
        'price_min':  filters.get('price_min'),
        'price_max': filters.get('price_max'),
    }
    
    return render(request, 'yourhome/filtered_properties.html', context)


def property_form(request, pk=None):
    if pk:
        property = Property.objects.get(pk=pk)
        action = 'Update'
    else:
        property = Property()
        action = 'List a'
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'yourhome/property_form.html', {'form': form, 'action': action, 'pk': pk})

def property_view(request, pk):
    property = get_object_or_404(Property, pk=pk)
    form = PropertyViewForm(instance=property)
    return render(request, 'yourhome/property_view.html', {'form': form})


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
    

