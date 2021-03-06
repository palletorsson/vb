from django.utils.translation import ugettext as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from django.db import models
from filebrowser.fields import FileBrowseField
from filebrowser.settings import ADMIN_THUMBNAIL
from gallery.models import *

import datetime


class TimeStampedActivate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField("Active")
    
    class Meta:
        abstract = True


class Variation(TimeStampedActivate):
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.ForeignKey('Article')
    pattern = models.ForeignKey('Pattern')
    color = models.ForeignKey('Color')

    def get_images(self, name):
        images = Image.objects.get(variation=name)
        return images
    
    def get_index_images(self):
        images = Image.objects.all()
        return images

    def get_image(self, pk):
        images = Image.objects.filter(variation__pk=pk)
        print images
        return '<img src="../../../media/%s" width="60"/>' % self.images

    get_image.allow_tags = True
    
    def __unicode__(self):
        return unicode(self.name)


class Size(models.Model):
    """
    Size used in Product Model         
    """
    name = models.CharField(max_length=10)
    
    def __unicode__(self):
        return unicode(self.name)



class ChoiceBase(models.Model):
    """
    use as common base model for Color, pattern and Quality
    """
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=160)
    order = models.IntegerField("order items")
    active = models.BooleanField("Active")

    def __unicode__(self):
        return unicode(self.name)


class Type(ChoiceBase):
    """
    Type used in Article Model
    """
    pass


class Color(ChoiceBase):
    """
    Color used in Product Model         
    """
    pass



class Pattern(ChoiceBase):
    """
    Pattern used in Product Model         
    """
    pass


class Quality(ChoiceBase):
    """
    Quality used in Article Model         
    """
    description = models.TextField()
    class Meta:
        verbose_name_plural = 'Qualies'


class Article(TimeStampedActivate):
    """
    Article are related to Product.         
    """
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=255, blank=True)
    sku_number = models.CharField(max_length=10)
    description = models.TextField()
    quality = models.ForeignKey('Quality')
    type = models.ForeignKey('Type')
    price = models.IntegerField()
    file = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg", ".gif", ".png"], blank=True, null=True)

    """
    def image_thumbnail(self, article):
        if article.image and article.image.filetype == "Image":
            return '<img src="%s" />' % article.image.version_generate(ADMIN_THUMBNAIL).url
        else:
            return ""
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"
    """

    def save(self, *args, **kwargs):
        if self.slug is None:
             self.slug = slugify(self.name)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.name) + " (" + unicode(self.sku_number)+ ")"
    