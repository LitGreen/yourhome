from django.contrib import admin
from cities_light.models import Country
from .models import Property, Avatar
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


admin.autodiscover()

User = get_user_model()

class PropertyAdmin(admin.ModelAdmin):
    list_display = ["title", "city", "advert_type", "property_type", 'formatted_price', 'creator']
    list_filter = ["advert_type", "property_type"]
    search_fields = ['creator__username']
    autocomplete_fields = ["city"]
    readonly_fields = ('created', 'updated', 'country', 'creator')

    def get_city(self, obj):
        return obj.city.city if obj.address else None
    get_city.short_description = 'City'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['creator'].required = False
        return form

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'creator' in form.base_fields:
            form.base_fields['creator'].disabled = True
        return form
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'creator':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        get_data = super().get_changeform_initial_data(request)
        get_data['country'] = Country.objects.get(name='United Kingdom').pk
        return get_data

    def formatted_price(self, obj):
        price = "{:,}".format(int(obj.price))
        return "£{}".format(price)
    formatted_price.short_description = 'Price'

admin.site.register(Property, PropertyAdmin)


class AvatarInline(admin.StackedInline):
    model = Avatar
    can_delete = False
    verbose_name = 'User profile picture'

class UserAdmin(DefaultUserAdmin):
    inlines = (AvatarInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)