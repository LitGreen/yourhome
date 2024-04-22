from django.db import models
from django.utils.translation import gettext_lazy as _
from cities_light.models import Country, City
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import random
import string
import uuid
 

class TimeStampedUUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Avatar(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField( verbose_name=_("Profile Picture"), upload_to='static/images/avatars/', null=True, blank=True)


class Address(models.Model):
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True) 
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)


class UKCountryDefault:
    def __call__(self):
        return Country.objects.get(name='United Kingdom')
    

class Property(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        TO_RENT = "To Rent", _("To Rent")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("House")
        FLAT = "Flat / Apartment", _("Flat / Apartment")
        OFFICE = "Office", _("Office")
        BUNGALOW = "Bungalow", _("Bungalow")
        WAREHOUSE = "Warehouse", _("Warehouse")
        COMMERCIAL = "Commercial", _("Commercial")
        OTHER = "Other", _("Other")



    title = models.CharField(verbose_name=_("Property Title"), max_length=250)
    slug = models.SlugField(allow_unicode=True, default='slug')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, verbose_name=_("City / Town"), on_delete=models.CASCADE, related_name='properties', null=True)
    
    postcode = models.CharField(
        verbose_name=_("Postcode"), max_length=100, default="140"
    )

    price = models.IntegerField(
        verbose_name=_("Price")
    )



    class TotalFloors(models.TextChoices):
        ONE = "1", _("1")
        TWO = "2", _("2")
        THREE = "3", _("3")
        FOUR = "4", _("4")
        FIVE_PLUS = "5+", _("5+")

    class Bedrooms(models.TextChoices):
        STUDIO = "Studio",  _("Studio")
        ONE = "1", _("1")
        TWO = "2", _("2")
        THREE = "3", _("3")
        FOUR = "4", _("4")
        FIVE_PLUS = "5+", _("5+")

    class Bathrooms(models.TextChoices):
        ONE = "1", _("1")
        TWO = "2", _("2")
        THREE = "3", _("3")
        FOUR = "4", _("4")
        FIVE_PLUS = "5+", _("5+")

    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
    )

    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=50,
        choices=PropertyType.choices,
         default=PropertyType.HOUSE,
    )

    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"), max_digits=8, decimal_places=2, default=0.0
    )

    total_floors = models.CharField(
        verbose_name=_("Total Floors"),
        max_length=50,
        choices=TotalFloors.choices,
        default=TotalFloors.ONE,
    )

    bedrooms = models.CharField(
        verbose_name=_("Bedrooms"),
        max_length=50,
        choices=Bedrooms.choices,
        default=Bedrooms.ONE,
    )

    bathrooms = models.CharField(
        verbose_name=_("bathrooms"),
        max_length=50,
        choices=Bathrooms.choices,
        default=Bathrooms.ONE,
    )

    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), upload_to='static/images/properties/', null=True, blank=True
    )
    photo1 = models.ImageField(
        default="",
        null=True,
        blank=True,
    )
    photo2 = models.ImageField(
        default="",
        null=True,
        blank=True,
    )
    photo3 = models.ImageField(
        default="",
        null=True,
        blank=True,
    )
    photo4 = models.ImageField(
        default="",
        null=True,
        blank=True,
    )
    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )

    ref_code = models.CharField(
        verbose_name=_("Property Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )

    views = models.IntegerField(verbose_name=_("Total Views"), default=0)

    description = models.TextField(
        verbose_name=_("Description"),
        default="Add description here...",
    )

    creator = models.ForeignKey(get_user_model(), verbose_name=_("Listed by"), on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        app_label = "yourhome" 
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)
