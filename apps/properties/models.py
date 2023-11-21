import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.common.models import TimeStampedModel
from .managers import PropertyPublishedManager


User = get_user_model()


class Property(TimeStampedModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")
        AUCTION = "Auction", _("Auction")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("House")
        APARTMENT = "Apartment", _("Apartment")
        OFFICE = "Office", _("Office")
        WAREHOUSE = "Warehouse", _("Warehouse")
        STUDIO = "Studio", _("Studio")
        STORE = "Store", _("Store")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(
        User,
        verbose_name=_("Agent, Seller or Buyer"),
        on_delete=models.DO_NOTHING,
        related_name=_("property_client"),
    )
    title = models.CharField(verbose_name=_("Property Title"), max_length=150)
    slug = AutoSlugField(populate_from="title", unique=True)
    reference_code = models.CharField(
        verbose_name=_("Property Reference Code"),
        max_length=150,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Describe the property."),
        default=_("Update this field"),
    )
    country = CountryField(
        verbose_name=_("Country"),
        default=_("GH"),
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=100,
        default=_("Accra"),
    )
    digital_address = models.TextField(
        verbose_name=_("Digital Address"), blank=True, null=True
    )
    price = models.DecimalField(
        verbose_name=_("Property Price"), max_digits=10, decimal_places=2, default=0.00
    )
    property_dimensions = models.TextField(
        verbose_name=_("Property Size"),
        help_text=_("Provide the dimensions of the property."),
    )
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=20,
        choices=AdvertType.choices,
        default=AdvertType.FOR_RENT,
    )
    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
    )
    cover_image = models.ImageField(
        verbose_name=_("Primary Picture"),
        default="/property.jpeg",
        blank=True,
        null=True,
    )
    secondary_image1 = models.ImageField(
        verbose_name=_("Secondary Picture 1"),
        default="/property.jpeg",
        blank=True,
        null=True,
    )
    secondary_image2 = models.ImageField(
        verbose_name=_("Secondary Picture 2"),
        default="/property.jpeg",
        blank=True,
        null=True,
    )
    secondary_image3 = models.ImageField(
        verbose_name=_("Secondary Picture 3"),
        default="/property.jpeg",
        blank=True,
        null=True,
    )
    secondary_image4 = models.ImageField(
        verbose_name=_("Secondary Picture 4"),
        default="/property.jpeg",
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(
        verbose_name=_("Published status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Property Views"), default=0)
    published = PropertyPublishedManager()

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.title.title()

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.reference_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=15)
        )
        super().save(*args, **kwargs)


class PropertyViews(TimeStampedModel):
    ip = models.CharField(
        verbose_name=_('IP Address'),
        max_length=300
    )
    property = models.ForeignKey(
        Property,
        related_name='property_views',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Property View'
        verbose_name_plural = 'Property Views'

    def __str__(self) -> str:
        return f'Total views on {self.property} currently is {self.property.views}'
