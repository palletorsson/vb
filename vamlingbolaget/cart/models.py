from django.db import models
from products.models import * 
import datetime
import random


class Cart(models.Model):
    key = models.CharField(max_length = 50)

    def __unicode__(self):
        return '%s' %self.pk


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, default=1)
    article = models.ForeignKey(Article, default=1)
    color = models.ForeignKey(Color, default=1)
    color_2 = models.ForeignKey(Color, null=True)
    pattern = models.ForeignKey(Pattern, default=1)
    pattern_2 = models.ForeignKey(Pattern, null=True)
    size = models.ForeignKey(Size, default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering=['date_added']

    def __unicode__(self):
        return "%s %s" % (self.quantity, self.article.name)

