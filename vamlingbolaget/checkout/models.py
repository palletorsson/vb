
from django.db import models
from django.utils.translation import ugettext as _

ORDER_STATUS = (
    ('I', 'Initialized'),
    ('O', 'Ordered'),
    ('M', 'Make'),
    ('H', 'Handling'),
    ('C', 'Cancelled'),
    ('S', 'Shipping'),
    ('P', 'Payed'),
    ('F', 'Finalized')
    )

PAYMENT_METHOD = (
    ('P', 'On_delivery'),
    ('C', 'By_card'),
    ('K', 'Klarna')
    )


class Checkout(models.Model):
    # billing
    first_name = models.CharField(_("Namn"), max_length=80)
    last_name = models.CharField(_("Efternamn"), max_length=80)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Telefonnummer"), max_length=20)
    street = models.CharField(_("Gatuadress"), max_length=80)
    city = models.CharField(_("Postort"), max_length=80)
    postcode = models.CharField(_("Postnummer"), max_length=10)
    country = models.CharField(_("Land"), max_length=80, blank=True)
    message = models.TextField(_("Meddelande"), blank=True)
    ip = models.CharField(_("Ip"), max_length=255, blank=True)
    order = models.TextField(blank=True)
    payment_log = models.TextField(blank=True)
    payex_key = models.CharField(_("Payex key"), max_length=34, blank=True)
    post = models.BooleanField(default="True")
    paymentmethod = models.CharField(_("Betalning"), max_length=1, choices=PAYMENT_METHOD)
    order_number = models.IntegerField(blank=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, blank=True)
    session_key = models.CharField(_("Session key"), max_length=50, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(_("Gatuadress2"), max_length=80, blank=True)
    shipping_city = models.CharField(_("Postort2"), max_length=80, blank=True)
    shipping_postcode = models.CharField(_("Postnummer2"), max_length=10, blank=True)
    shipping_country = models.CharField(_("Land2"), max_length=80, blank=True)
    fortnox_obj = models.TextField(blank=True)
    unifaun_obj = models.TextField(blank=True) 

    def __unicode__(self):
        return "%s %s %s %s" % (self.first_name, self.last_name, self.order_number, self.date_added)
