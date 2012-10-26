from django.db import models
from products.models import * 
import datetime

class Cart(models.Model):
    owner = models.CharField(max_length = 50, default='anonymous')
    def __unicode__(self):
        return 'Cart of %s' %self.owner
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    article = models.ForeignKey(Article, default=1)
    color = models.ForeignKey(Color, default=1)
    pattern = models.ForeignKey(Pattern, default=1)
    size = models.ForeignKey(Size, default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering=['date_added']
    
    def total(self):
        return self.quantity * self.article_id.price
    
    def name(self):
        return self.article.name
    
    def price(self):
        return self.article.price * self.quantity

    def __unicode__(self):
        return "%dx %s" % (self.quantity, self.article.name)
