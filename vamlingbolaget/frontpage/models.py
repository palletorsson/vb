from django.db import models
from ckeditor.fields import RichTextField

class Frontpage(models.Model):
    body = RichTextField(help_text="This is the major part frontpage")
    extra_head = models.CharField(max_length=255,
    help_text="This is a extra message to be added in top of the page. Can be anything up to 255 characters.", blank=True)
    show_extra_head = models.BooleanField("Active", help_text="Check this i you want to show the extra head")

    def __unicode__(self):
        return unicode("Edit the single Frontpage")
