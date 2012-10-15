from django.db import models
from products.models import * 
import datetime

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    article_id  = models.ForeignKey(Article)
    color = models.ForeignKey(Color)
    pattern = models.ForeignKey(Pattern)
    size = models.ForeignKey(Size)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering=['date_added']
    
    def total(self):
        return self.quantiy * self.article.price
    
    def name(self):
        return self.article.name
    
    def price(self):
        return self.article.price * self.quantity

    def __unicode__(self):
        return "%dx %s" % (self.quantity, self.article.name)