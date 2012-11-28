from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=255,
        help_text="Title if the page. Can be anything up to 255 characters.")
    url = models.SlugField()
    body = models.TextField()
    active = models.BooleanField("Active", default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-title']

