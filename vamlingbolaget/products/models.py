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
#from products.fortnox import get_headers, get_art_temp, get_articles, get_article, create_article, update_article

SIZES = (
        ('XS', 'XS'), 
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XLL', 'XLL'),
        )

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
        return "%s %s %s %s" % (self.article.sku_number, self.article.name, self.color, self.pattern)

    class Meta:
        unique_together = ('article', 'pattern', 'color',)


class FullVariation(TimeStampedActivate):
    variation = models.ForeignKey('Variation')
    size  = models.CharField(max_length=10)
    stock = models.IntegerField(default=1)
    order = models.IntegerField("order items", default=100)
    
    def get_art_num(self):
        return "%s_%s_%s_%s" % (self.variation.article.sku_number, self.variation.color.order, self.variation.pattern.order, self.size)

    def get_sizes(self): 
        return SIZES

    def get_sku(self): 
        return str(self.variation.article.sku_number) + "_" +  str(self.variation.color) + "_" + str(self.variation.pattern) + "_" + str(self.size)

    def __unicode__(self):
        return "%s %s %s %s" % (self.variation.article.sku_number, self.variation.color, self.variation.pattern, self.size)

    class Meta:
        unique_together = ('variation', 'size',)

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
    
    def __unicode__(self):
        return unicode(self.name)

class Category(ChoiceBase):
    """
    Type used in Article Model
    """
    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return unicode(self.name)


class Color(ChoiceBase):
    """
    Color used in Product Model         
    """
    quality = models.ForeignKey('Quality', default=1)

    def __unicode__(self):
        return unicode(self.name)


class Pattern(ChoiceBase):
    """
    Pattern used in Product Model         
    """
    quality = models.ForeignKey('Quality', default=1)

    def __unicode__(self):
        return unicode(self.name)


class Quality(ChoiceBase):
    """
    Quality used in Article Model         
    """
    description = models.TextField()
    class Meta:
        verbose_name_plural = 'Qualies'

    def __unicode__(self):
        return unicode(self.name)

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

class ArticleCost(models.Model):
    article = models.ForeignKey('Article')
    fabric_m = models.IntegerField("fabric required in cemtimeters")
    cuttime = models.IntegerField("cutting time")
    sawtime = models.IntegerField("sawing time")
    addtime = models.IntegerField("time for thread cutting and iron")
    attachment = models.IntegerField("additional attachments in SEK")

    def get_final_cost(self):
        kg_price = 20 # also adding shipment 0.5
        unit_meter = 3.1
        euro = 9.8  
        meter_cost_sek = int((kg_price / unit_meter) * euro) 
        meter_cost = meter_cost_sek * 0.01 
        minutes_cost = 3.5
        minutes_added = self.cuttime + self.sawtime + self.addtime 
        product_cost = (self.fabric_m * meter_cost) + (minutes_added * minutes_cost) + (self.attachment)
        return product_cost

    def get_gross_cost(self):
        cost = self.get_final_cost()
        gross_pris = cost * 2
        return gross_pris

    def get_out_cost(self):
        cost = self.get_final_cost()
        out_pris = ((cost * 2) * 25) / 10
        return out_pris    

    def get_current_price(self):
        return self.article.price    

    def __unicode__(self):
        return "%s %s" % (self.article.sku_number, self.article.name)


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

    
class ReaArticle(models.Model):
    article = models.ForeignKey('Article')
    pattern = models.ForeignKey('Pattern')
    color = models.ForeignKey('Color')
    quality = models.ForeignKey('Quality')
    category = models.ForeignKey('Category')
    size = models.ForeignKey('Size')
    description = models.TextField()
    json = models.TextField(blank=True, null=True)
    rea_price = models.IntegerField()
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=2, choices = STATUS)
    stockquantity = models.IntegerField()
    image = FileBrowseField("Image", max_length=200, directory="bargains/", extensions=[".jpg", ".jpeg", ".gif", ".png"], blank=True, null=True)
  
    def __unicode__(self):
        return unicode(self.article)
 
    class Meta:
        ordering = ['-created', ]

class PatternAndColor(models.Model):
    """
    Need to build active colors and pattern combination
    """
    name = models.CharField(max_length=160)
    color = models.ForeignKey('Color')
    pattern = models.ForeignKey('Pattern')
    quality = models.ForeignKey('Quality')
    order = models.IntegerField("order items", unique=True)
    active = models.BooleanField("Active", default=True)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['-color', '-pattern',]

