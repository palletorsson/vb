from django.utils.translation import ugettext as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from django.db import models

"""
Kattens Modeller
"""

class Variation(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    article = models.ForeignKey('Article')
    mainimage = models.ForeignKey('Mainimage')
    color = models.ForeignKey('Color')
    pattern = models.ForeignKey('Pattern')    
    active = models.BooleanField("Active")
    
    def __unicode__(self):
        return unicode(self.name)

class Image(models.Model):
    variation = models.ForeignKey('Variation')
    file = models.ImageField("Image", upload_to="variations")
    image_1200 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(1200)], image_field='file', format='JPEG', 
            options={'quality': 100}, )
    image_900 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(900)], image_field='file', format='JPEG', 
            options={'quality': 90}, )
    image_600 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(600)], image_field='file', format='JPEG', 
            options={'quality': 90}, )
    image_460 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(460)], image_field='file', format='JPEG', 
            options={'quality': 90}, )    
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
        ResizeToFill(150)], image_field='file',
        format='JPEG', options={'quality': 90})

class Mainimage(models.Model):
    file = models.ImageField("Image", upload_to="variations")
    image_1200 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(1200)], image_field='file', format='JPEG', 
            options={'quality': 100}, )
    image_900 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(900)], image_field='file', format='JPEG', 
            options={'quality': 90}, )
    image_600 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(600)], image_field='file', format='JPEG', 
            options={'quality': 90}, )
    image_460 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(460)], image_field='file', format='JPEG', 
            options={'quality': 90}, )    
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
        ResizeToFill(150)], image_field='file',
        format='JPEG', options={'quality': 90})


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
    slug = models.SlugField(max_length=255)
    sku_number = models.CharField(max_length=10)
    description = models.TextField()
    quality = models.ForeignKey('Quality')
    type = models.ForeignKey('Type')
    price = models.IntegerField()
    file = models.ImageField("Image", upload_to="articles")
    active = models.BooleanField("Active")
    
    def __unicode__(self):
        return unicode(self.name)
