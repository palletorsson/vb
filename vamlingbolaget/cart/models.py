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
    color = models.SmallIntegerField(default=1)
    color_2 = models.SmallIntegerField(default=0)
    pattern = models.SmallIntegerField(default=1)
    pattern_2 = models.SmallIntegerField(default=0)
    size = models.SmallIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering=['date_added']

    def __unicode__(self):
        return "%s %s" % (self.quantity, self.article.name)


class BargainCartItem(models.Model):
    cart = models.ForeignKey(Cart)
    bargain = models.ForeignKey(Bargainbox)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['date_added']

    def __unicode__(self):
        return "%s" % self.bargain.title