from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedModel


class Enquiry(TimeStampedModel):
    name = models.CharField(
        verbose_name=_('Your Name'),
        max_length=100
    )
    phone_number = PhoneNumberField(
        verbose_name=_('Contact'),
        max_length=20,
        default=_('+233244000000')
    )
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()

    class Meta:
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'
    
    def __str__(self) -> str:
        return self.email
    
    