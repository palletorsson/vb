from django.db import models
from products.models import * 
import datetime
import random


class Cart(models.Model):
    key = models.CharField(max_length = 50)
    def __unicode__(self):
        return '%s' %self.key


class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, default=1)
    article = models.ForeignKey(Article, default=1)
    color = models.ForeignKey(Color, default=1)
    pattern = models.ForeignKey(Pattern, default=1)
    size = models.ForeignKey(Size, default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering=['date_added']

    def total(self):
        return self.quantity * self.article.price
    print total

    def name(self):
        return self.article.name
    
    def price(self):
        return self.article.price * self.quantity

    def __unicode__(self):
        return "%s %s" % (self.quantity, self.article.name)

