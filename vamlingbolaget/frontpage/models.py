from django.db import models
from ckeditor.fields import RichTextField
from filebrowser.fields import FileBrowseField


class Frontpage(models.Model):
    body = RichTextField(help_text="This is the major part frontpage")
    extra_head = models.CharField(max_length=255,
    help_text="This is a extra message to be added in top of the page. Can be anything up to 255 characters.", blank=True)
    show_extra_head = models.BooleanField("Active", help_text="Check this i you want to show the extra head")

    def __unicode__(self):
        return unicode("Edit the single Frontpage")


STATUS = (
    ('A', 'Active'),
    ('I', 'Inactive')
    )

MEDIATYPE = (
    ('I', 'Imagepost'),
    ('V', 'Videopost')
    )

class FrontpageTheme(models.Model):
    title = models.CharField(max_length=255)
    title_extra = models.CharField(max_length=255, blank=True, help_text="as tagline")
    order = models.IntegerField(help_text="Set the order if more then one")
    status = models.CharField(max_length=1, choices=STATUS)
    
    def __unicode__(self):
        return "%s" % (self.title)

class FrontpageExtended(models.Model):
    heading  = models.CharField(max_length=255, help_text="The title")
    theme = models.ForeignKey('FrontpageTheme')
    heading_extra = models.CharField(max_length=255, blank=True, help_text="as tagline")
    link_to = models.CharField(max_length=255, help_text="use relative link")
    feature_image = FileBrowseField("Image", max_length=200, directory="frontpage/", extensions=[".jpg"], blank=True, null=True)
    body = models.TextField(blank=True, help_text="This could be used for sweden")
    order = models.IntegerField(help_text="Set the order")
    status = models.CharField(max_length=1, choices=STATUS)
    mediatype = models.CharField(max_length=1, choices=MEDIATYPE)
    extramedia = models.TextField(blank=True, help_text="This could be the iframe of a video, gif or other html")

    def __unicode__(self):
        return "%s" % (self.heading)


