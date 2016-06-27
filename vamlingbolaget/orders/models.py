
from django.db import models
from django.utils.translation import ugettext as _
from products.models import *
from checkout.models import Checkout

class OrderItem(models.Model):
    checkout = models.ForeignKey(Checkout, default=1)
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

class ReaOrderItem(models.Model):
    checkout = models.ForeignKey(Checkout, default=1)
    reaArticle = models.ForeignKey(ReaArticle)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['date_added']

    def __unicode__(self):
        return "%s" % self.checkout 

  
def ShowOrders(request): 
    checkouts = Checkout.objects.filter(status='I')
    cartitems = checkouts.cartitem_set.all()
    reaitems = checkouts.reacartitem_set.all()
    print checkouts

    return HttpResponse(status=200)