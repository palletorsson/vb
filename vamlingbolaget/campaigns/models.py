from django.db import models
from filebrowser.fields import FileBrowseField

STATUS = (
    ('A', 'Active'),
    ('E', 'Expired'),
    ('P', 'Public'),
    )

MEDIA_TYPE = (
    ('I', 'Image'),
    ('V', 'Video'),
    ('P', 'Pdf'),
    )


class Campaign(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    drop_boxfolder = models.CharField(max_length=40)
    status = models.CharField(max_length=2, choices = STATUS)
    prio = models.IntegerField("prio", unique=True)
    active = models.BooleanField("Active", default=True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    when = models.CharField(max_length=40)

    def __unicode__(self):
        return unicode(self.title)

class File(models.Model):
    campaign = models.ForeignKey('Campaign')
    title = models.CharField(max_length=40)
    link = models.CharField(max_length=220)
    status = models.CharField(max_length=2, choices = STATUS)
    def __unicode__(self):
        return unicode(self.title)

class Media(models.Model):
    campaign = models.ForeignKey('Campaign')
    title = models.CharField(max_length=40)
    link = models.CharField(max_length=220)
    type = models.CharField(max_length=2, choices = MEDIA_TYPE)

    def __unicode__(self):
        return unicode(self.title)



class Kanban(models.Model):
    campaign = models.ForeignKey('Campaign')
    title = models.CharField(max_length=40)
    link = models.CharField(max_length=220)
    
    def __unicode__(self):
        return unicode(self.title)
