

from django.utils.translation import ugettext as _
from django.db import models
from filebrowser.fields import FileBrowseField
from products.models import Variation as v
from django.contrib.flatpages.models import FlatPage

GALLERY_STATUS = (
    ('A', 'Active'),
    ('F', 'Featured'),
    ('H', 'History'),
    ('I', 'Indexpage')
    )

class GalleryStatus(models.Model):
    name = models.CharField(max_length=30)
    order = models.IntegerField()
    display_on_gallery_page = models.BooleanField(default = True)
    display_on_index_page = models.BooleanField(default = False)
    order = models.SmallIntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'gallery statuses'

class Gallery(models.Model):
    name= models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(GalleryStatus, help_text='Group galleries that belong together', verbose_name='Belongs to group')
    feature_image = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg"], blank=True, null=True)
    flatpage = models.ForeignKey(FlatPage, null=True, blank=True)
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'galleries'

class Photographer(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)

class Image(models.Model):
    name= models.CharField(max_length=255, default=" ",)
    image = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg"], blank=True, null=True)
    photographer = models.ForeignKey(Photographer, blank=True, null=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True)
    variation = models.ForeignKey(v, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return unicode(self.name)


    
