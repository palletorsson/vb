from django.db import models

"""
Kattens Modeller
"""

class Variation(models.Model):
    name = models.CharField(max_length=40)
    color = models.ForeignKey('Color')
    pattern = models.ForeignKey('Pattern')    
    file = models.ImageField("Image", upload_to="variations")
    active = models.BooleanField("Active")

class Size(models.Model):
    """
    Size used in Product Model         
    """
    name = models.CharField(max_length=10)
    
    def __unicode__(self):
        return unicode(self.name)


class Color(models.Model):
    """
    Color used in Product Model         
    """
    name = models.CharField(max_length=20)
    quality = models.ForeignKey('Quality')
    file = models.ImageField("Image", upload_to="colors")
    active = models.BooleanField("Active")
    
    def __unicode__(self):
        return unicode(self.name)


class Pattern(models.Model):
    """
    Pattern used in Product Model         
    """
    name = models.CharField(max_length=20)
    quality = models.ForeignKey('Quality')
    file = models.ImageField("Image", upload_to="patterns")
    active = models.BooleanField("Active")
    
    def __unicode__(self):
        return unicode(self.name)


class Quality(models.Model):
    """
    Quality used in Article Model         
    """
    name = models.CharField(max_length=100)
    active = models.BooleanField("Active")

    def __unicode__(self):
        return unicode(self.name)


class Type(models.Model):
    """
    Type used in Article Model         
    """
    name = models.CharField(max_length=100)
    quality = models.ForeignKey('Quality')
    active = models.BooleanField("Active")
    
    def __unicode__(self):
        return unicode(self.name)


class Article(models.Model):
    """
    Article are related to Product.         
    """
    name = models.CharField(max_length=100)
    sku_number = models.CharField(max_length=10)
    quality = models.ForeignKey('Quality')
    type = models.ForeignKey('Type')
    price = models.IntegerField()
    file = models.ImageField("Image", upload_to="articles")
    active = models.BooleanField("Active")
    
    def __unicode__(self):
        return unicode(self.name)
