from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
        unique=True,
        verbose_name=_('user'),
        related_name='my_profile')

    # billing
    billing_adress_first_name = models.CharField("First name", max_length=80)
    billing_adress_last_name = models.CharField("Last name", max_length=80)
    billing_adress_email = models.EmailField("Email")
    billing_adress_phone = models.CharField("Phone", max_length=20)

    billing_adress_street = models.CharField("Street", max_length=80)
    billing_adress_city = models.CharField("City", max_length=80)
    billing_adress_postcode = models.CharField("Postcode", max_length=10)
    billing_adress_country = models.CharField("Country", max_length=80)

    # shipping
    alternativ_shipping_adress = models.BooleanField()
    shipping_adress_first_name = models.CharField("First name", max_length=80, blank=True)
    shipping_adress_last_name = models.CharField("Last name", max_length=80, blank=True)
    shipping_adress_street = models.CharField("Street", max_length=80, blank=True)
    shipping_adress_city = models.CharField("City", max_length=80, blank=True)
    shipping_adress_postcode = models.CharField("Postcode", max_length=10, blank=True)
    shipping_adress_country = models.CharField("Country", max_length=80, blank=True)
    additional_instructions = models.TextField("Additional instructions", blank=True)

    alternativ_shipping_adress = models.BooleanField()

    def __unicode__(self):
        return unicode(self.user)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, **kwargs):
        MyProfile.objects.get_or_create(user=instance)
