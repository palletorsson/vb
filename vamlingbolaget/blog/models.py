import datetime

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

class PostManager(models.Manager):
    def get_visible(self):
        return self.get_query_set().filter(publish_at__lte=datetime.datetime.now(), active=True)

class TimeStampedActivate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False,
                                help_text="Controls whether or not this item (blog or posts) is visable on the site.")
    
    class Meta:
        abstract = True
	
class Blog(TimeStampedActivate):

    """
    A blog beloinging to a user.
    Blogs have multipul posts and on user can have many blogs

    >>> b = Blog()
    >>> b.name = 'Foo Blog'
    >>> b.user = User.objects.create(username='foo', password='test')
    >>> b.save()
    >>> print b
    Foo Blog
    >>> print b.user.username
    foo

    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name="blogs")

    
    def __unicode__(self):
        return self.name
	
class Post(TimeStampedActivate):
    """
    A post that belongs to a blog.
    
    >>> b = blog.objects.get(id=1)
    >>> p = Post()
    >>> p.title = "a test Post"
    >>> p.blog = b
    >>> p.body = "just a small blog"
    >>> p.slug = "a-test-blog"
    >>> p.save()
    >>> print p.blog.name
    Foo Blog
    >>> print p.active
    False
    
    """
    title = models.CharField(max_length=255, 
                            help_text="Title if the post. Can be anything up to 255 characters.")
    slug = models.SlugField()
    body = RichTextField()
    publish_at = models.DateTimeField(default=datetime.datetime.now(), 
                                     help_text="Date and time post should become visible")
    
    blog = models.ForeignKey(Blog, related_name="posts")
    tags = TaggableManager()   
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
	
    class Meta:
        ordering = ['-publish_at', '-modified', '-created']


class News(TimeStampedActivate):
    title = models.CharField(max_length=255,
        help_text="Title if the post. Can be anything up to 255 characters.")
    slug = models.SlugField()
    body = models.TextField()
    publish_at = models.DateTimeField(default=datetime.datetime.now(),
        help_text="Date and time post should become visible")
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-publish_at', '-modified', '-created']
        verbose_name_plural = 'news'

