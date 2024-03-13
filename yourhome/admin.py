from django.contrib import admin
from .forms import MultiselectFilterForm
from cities_light.models import Country, City
from .models import Property, Address

from django.contrib.admin import SimpleListFilter


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

class PropertyAdmin(admin.ModelAdmin):
    form = MultiselectFilterForm
    list_display = ["title", "city", "advert_type", "property_type"]
    list_filter = ["advert_type", "property_type"]

    def get_city(self, obj):
        return obj.city.city if obj.address else None
    get_city.short_description = 'City'

admin.site.register(Property, PropertyAdmin)




