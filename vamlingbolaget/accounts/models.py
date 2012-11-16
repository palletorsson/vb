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
    adress_name = models.CharField(max_length=50)
    post_code = models.IntegerField()
    phone_number = models.IntegerField()

    alternativ_shipping_adress = models.BooleanField()


    def __unicode__(self):
        return unicode(self.user)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, **kwargs):
        MyProfile.objects.get_or_create(user=instance)
