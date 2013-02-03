from django.utils.translation import ugettext as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from django.db import models
from filebrowser.fields import FileBrowseField
from filebrowser.settings import ADMIN_THUMBNAIL
from gallery.models import *
import datetime
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust


class TimeStampedActivate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField("Active", default=True)
    
    class Meta:
        abstract = True

class Variation(TimeStampedActivate):
    article = models.ForeignKey('Article')
    pattern = models.ForeignKey('Pattern')
    color = models.ForeignKey('Color')

    order = models.IntegerField("order items", default=100)

    def get_images(self, pk):
        images = Image.objects.get(variation__pk=pk)
        return images
    
    def get_index_images(self):
        images = Image.objects.all()
        return images

    def get_image(self, pk):
        images = Image.objects.filter(variation__pk=pk)
        return '<img src="../../../media/%s" width="60"/>' % self.images

    get_image.allow_tags = True
    
    def __unicode__(self):
        return unicode(self.article)


class Size(models.Model):
    """
    Size used in Product Model         
    """
    name = models.CharField(max_length=10)
    quality = models.ForeignKey('Quality', default=1)
    def __unicode__(self):
        return unicode(self.name)


class ChoiceBase(models.Model):
    """
    use as common base model for Color, pattern and Quality
    """
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=160)
    order = models.IntegerField("order items")
    active = models.BooleanField("Active", default=True)

    def __unicode__(self):
        return unicode(self.name)


class Type(ChoiceBase):
    """
    Type used in Article Model
    """
    pass

class Category(ChoiceBase):
    """
    Type used in Article Model
    """
    class Meta:
        verbose_name_plural = 'Categories'

class Color(ChoiceBase):
    """
    Color used in Product Model         
    """
    quality = models.ForeignKey('Quality', default=1)


class Pattern(ChoiceBase):
    """
    Pattern used in Product Model         
    """
    quality = models.ForeignKey('Quality', default=1)

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
    sku_number = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    quality = models.ForeignKey('Quality')
    category = models.ForeignKey('Category')
    type = models.ForeignKey('Type')
    price = models.IntegerField()
    file = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg", ".gif", ".png"], blank=True, null=True)
    discount = models.ForeignKey('Discount', blank=True, null=True)

    def f_discount(self):
        if (self.discount.type == 'P'):
            f_discount = (self.price * (100-self.discount.discount)) / 100
        else:
            f_discount = self.price - self.discount.discount

        return f_discount


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

TYPE_CHOICES = (
    ('P', 'Percent'),
    ('A', 'Amount')
    )

class Discount(models.Model):
    title = models.CharField(max_length = 50)
    reason = models.CharField(max_length = 255)
    discount = models.IntegerField()
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, blank=True)
    active = models.BooleanField("Active", default=True)

    def __unicode__(self):
        return unicode(self.title)



STATUS = (
    ('A', 'Active'),
    ('E', 'Expired'),
    )

class Bargainbox(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=2, choices = STATUS)
    image = models.ImageField(upload_to = 'bargains/')

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        ordering = ['-created', ]
