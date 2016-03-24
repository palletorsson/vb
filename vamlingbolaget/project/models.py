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

PRO_TYPE = (
    ('I', 'Campaign'),
    ('V', 'Internal'),
    ('P', 'Short'),
    )

class Project(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    folder = models.CharField(max_length=40)
    type = models.CharField(max_length=2, choices = PRO_TYPE)
    status = models.CharField(max_length=2, choices = STATUS)
    prio = models.IntegerField("prio", unique=True)
    active = models.BooleanField("Active", default=True)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    when = models.CharField(max_length=40)


    def __unicode__(self):
        return unicode(self.title)

class File(models.Model):
    project = models.ForeignKey('Project')
    title = models.CharField(max_length=40)
    link = models.CharField(max_length=220)
    status = models.CharField(max_length=2, choices = STATUS)
    def __unicode__(self):
        return unicode(self.title)

class Media(models.Model):
    project = models.ForeignKey('Project')
    title = models.CharField(max_length=40)
    link = models.CharField(max_length=220)
    type = models.CharField(max_length=2, choices = MEDIA_TYPE)

    def __unicode__(self):
        return unicode(self.title)



class Kanban(models.Model):
    project = models.ForeignKey('Project')
    title = models.CharField(max_length=40)
    link = models.CharField(max_length=220)
    
    def __unicode__(self):
        return unicode(self.title)
