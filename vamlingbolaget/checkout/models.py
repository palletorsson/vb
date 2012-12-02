from django.db import models

ORDER_STATUS = (
    ('O', 'Ordered'),
    ('C', 'Cancelled'),
    ('S', 'Sent'),
    ('P', 'Payed')
    )

class Checkout(models.Model):
    # billing
    first_name = models.CharField("First name", max_length=80)
    last_name = models.CharField("Last name", max_length=80)
    email = models.EmailField("Email")
    phone = models.CharField("Phone", max_length=20)
    street = models.CharField("Street", max_length=80)
    city = models.CharField("City", max_length=80)
    postcode = models.CharField("Postcode", max_length=10)
    country = models.CharField("Country", max_length=80,blank=True)
    message = models.TextField(blank=True)
    ip = models.CharField("Ip", max_length=255,blank=True)
    order = models.TextField(blank=True)
    post = models.BooleanField()
    order_number = models.IntegerField(blank=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, blank=True)
    session_key = models.CharField("Session key", max_length=50, blank=True)
