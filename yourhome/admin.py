from django.contrib import admin
from .forms import MultiselectFilterForm
from cities_light.models import Country, City
from .models import Property, Address
from django.contrib.humanize.templatetags.humanize import intcomma

from django.contrib.admin import SimpleListFilter


# admin.site.register(Address)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title", "city", "advert_type", "property_type", 'formatted_price']
    list_filter = ["advert_type", "property_type"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        uk = Country.objects.get(name='United Kingdom')
        form.base_fields['country'].initial = uk
        form.base_fields['country'].disabled = True
        return form

    def get_city(self, obj):
        return obj.city.city if obj.address else None
    get_city.short_description = 'City'

    def formatted_price(self, obj):
        price = "{:,}".format(int(obj.price))
        return "£{}".format(price)
    formatted_price.short_description = 'Price'

admin.site.register(Property, PropertyAdmin)