from django.utils.translation import ugettext as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from django.db import models
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
    combo = models.ForeignKey('Combo', help_text="A combination of pattern, color and quality")
    
    def get_images(self, name):
        images = ImageVariation.objects.get(variation=name)
        return images
    
    def get_index_images(self):
        images = ImageVariation.objects.all()
        return images

    def image(self):
        images = ImageVariation.objects.filter(variation__pk=1)
        print images
        return '<img src="../../../media/%s" width="60"/>' % self.images
    
    image.allow_tags = True
    
    def __unicode__(self):
        return unicode(self.name)

 
class Image(models.Model):
    file = models.ImageField("Image", upload_to="variations")
    image_1200 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(900, 1350)], image_field='file', format='JPEG', 
            options={'quality': 100}, )
    image_900 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(600, 900)], image_field='file', format='JPEG', 
            options={'quality': 90}, )
    image_600 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(400, 600)], image_field='file', format='JPEG', 
            options={'quality': 90}, )
    image_460 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(300, 450)], image_field='file', format='JPEG', 
            options={'quality': 90}, )    
    image_300 = ImageSpecField([Adjust(contrast=1, sharpness=1),
        ResizeToFill(200, 300)], image_field='file', format='JPEG', 
            options={'quality': 90}, )  
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
        ResizeToFill(100, 150)], image_field='file',
        format='JPEG', options={'quality': 90})

    class Meta:
        abstract = True

class ImageVariation(Image):
    variation = models.ForeignKey('Variation')
    is_featured = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.variation)


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
    order = models.IntegerField("If you need to other these items")
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
    quality = models.ForeignKey('Quality')


class Pattern(ChoiceBase):
    """
    Pattern used in Product Model         
    """
    quality = models.ForeignKey('Quality')



class Quality(ChoiceBase):
    """
    Quality used in Article Model         
    """
    description = models.TextField()


class Combo(models.Model):
    file = models.ImageField("Image", upload_to="combo")
    quality = models.ForeignKey('Quality')
    pattern = models.ForeignKey('Pattern')
    color = models.ForeignKey('Color')
    active = models.BooleanField("Active")
    
    def image(self):
        return '<img src="../../../media/%s" width="60"/>' % self.file
    image.allow_tags = True

    def __unicode__(self):
        return unicode(self.file)


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
    file = models.ImageField("Image", upload_to="articles")

    def image(self):
        return '<img src="../../../media/%s" width="60"/>' % self.file
    image.allow_tags = True

    
    def save(self, *args, **kwargs):
        if self.slug is None:
             self.slug = slugify(self.name)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.name) + " (" + unicode(self.sku_number)+ ")"
    