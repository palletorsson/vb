from django.db import models
class checkout(models.Model):
    # billing
    first_name = models.CharField("First name", max_length=80)
    last_name = models.CharField("Last name", max_length=80)
    email = models.EmailField("Email")
    phone = models.CharField("Phone", max_length=20)

    street = models.CharField("Street", max_length=80)
    city = models.CharField("City", max_length=80)
    postcode = models.CharField("Postcode", max_length=10)
    country = models.CharField("Country", max_length=80)
    message = models.TextField()

    def get_order(request, key):
        pass
