from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Property, Avatar
from .filters import PropertyFilter
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.decorators import login_required
from .forms import MultiselectFilterForm, PropertyForm, PropertyViewForm, RegistrationForm, CustomUserChangeForm, AvatarForm
from cities_light.models import City
from dal import autocomplete
from django.contrib.auth import get_user_model
from django.apps import apps
from django.contrib.auth.decorators import login_required



User = get_user_model()

def login_register(request):
    show_login_form = request.GET.get('form') != 'register'
    login_form = AuthenticationForm()
    register_form = RegistrationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            show_login_form = True
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return redirect('home')
        elif 'register' in request.POST:
            show_login_form = False
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('two_factor:setup')
            else:
                for field in form:
                    for error in field.errors:
                        messages.error(request, f"{field.label}: {error}")

    context = {
        'show_login_form': show_login_form,
        'register_form': register_form,
        'login_form': login_form,
    }
    
    return render(request, 'yourhome/login_register.html', context)


def user_profile(request, pk):
    User = get_user_model()
    user = User.objects.get(pk=pk)
    properties = Property.objects.filter(creator=user)
    show_user_edit = request.GET.get('form') == 'edit'
    form = CustomUserChangeForm(instance=user)
    
    avatar, created = Avatar.objects.get_or_create(user=user)
    avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar) if request.method == 'POST' else AvatarForm(instance=avatar)

    if request.method == 'POST' and show_user_edit:
        form = CustomUserChangeForm(request.POST, instance=user)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid() and avatar_form.is_valid():
            form.save()
            avatar_form.save() 
            return redirect(reverse('user_profile', args=[user.pk]) + '?form=view')
        else:
            print(form.errors)
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")

    context = {
        'user': user,
        'form': form,
        'avatar_form': avatar_form,
        'show_user_edit': show_user_edit,
        'properties': properties,
    }
    return render(request, 'yourhome/user_profile.html', context)


def logoutUser(request):
    logout(request)

    return redirect('home')


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
    User = get_user_model()
    if pk:
        property = Property.objects.get(pk=pk)
        action = 'Update'
    else:
        property = Property()
        action = 'List a'
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            property = form.save(commit=False)
            if not pk: 
                property.creator = User.objects.get(id=request.user.id)
                success_message = f'{property} created successfully.'
            else:
                success_message = f'{property} updated successfully.'
            property.save()
            messages.success(request, success_message)
            return redirect('home')
    else:
        form = PropertyForm(instance=property)

    context = {
        'form': form, 
        'action': action,
        'property': property,
        'pk': pk
    }

    return render(request, 'yourhome/property_form.html', context)


def property_view(request, pk):
    property = get_object_or_404(Property, pk=pk)
    properties = Property.objects.all()
    form = PropertyViewForm(instance=property)
    action = 'Update'

    if property.pk is None:
        property.save()

    context = {
        'url': 'property_delete',
        'form': form,
        'action': action,
        'property': property,
         'properties': properties,
    }

    return render(request, 'yourhome/property_view.html', context)

def delete_modal(request, model_name, pk):
    if model_name.lower() == 'user':
        Model = get_user_model()
    else:
        Model = apps.get_model('yourhome', model_name)

    instance = get_object_or_404(Model, pk=pk)

    if request.method == 'POST':
        instance.delete()
        messages.success(request, f'{model_name} deleted successfully.')
        return redirect('home')
    
    context = {
        'model_name': model_name,
        'instance': instance,
    }
    
    return render(request, 'yourhome/delete_modal.html', context)


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
    

    

