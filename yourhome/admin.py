from django.contrib import admin

from .models import Property


class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title", "city", "advert_type", "property_type"]
    list_filter = ["advert_type", "property_type", "city"]


admin.site.register(Property, PropertyAdmin)




