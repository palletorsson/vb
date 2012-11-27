

from django.utils.translation import ugettext as _
from django.db import models
from filebrowser.fields import FileBrowseField
from products.models import Variation as v
from flatpages.models import Flatpage

GALLERY_STATUS = (
    ('A', 'Active'),
    ('F', 'Featured'),
    ('H', 'History'),
    ('I', 'Indexpage')
    )

class Gallery(models.Model):
    name= models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=GALLERY_STATUS)
    feature_image = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg"], blank=True, null=True)
    flatpage = models.ForeignKey(Flatpage)
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name_plural = 'galleries'

class Image(models.Model):
    name= models.CharField(max_length=50, default="default",)
    image = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg"], blank=True, null=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True)
    variation = models.ForeignKey(v, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.name)
